"""November model additions retain exact identities, evidence scope and prices."""
import copy
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
import zipfile
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'skills/promptharbor/scripts'))
import harbor
import price

NOW = date(2026, 11, 13)
MODELS = ('gemini-4-carbon', 'gemini-4-hydrogen', 'claude-fable-5-2')


def decisions(result):
    return (result['primary'], result['decision'], result['switch'], result['excluded'],
            [(r['rank'], r['model_id']) for r in result['recommendations']],
            [(c['model_id'], c['ranking'], c['covered_tasks'], c['missing_tasks'])
             for c in result['candidates']])


class NovemberModelsTests(unittest.TestCase):
    def setUp(self):
        self.data = harbor.load_data()
        self.models = {m['id']: m for m in self.data['models']['models']}
        self.sources = {s['id']: s for s in self.data['sources']['sources']}

    def route(self, model, **extra):
        return harbor.route({'tasks': ['agent.workflow'], 'available_models': [model], **extra},
                            self.data, NOW)

    def test_exact_resource_selection_does_not_substitute_predecessors(self):
        for model in MODELS:
            with self.subTest(model=model):
                result = self.route(model, current_model=model, language='zh-CN')
                self.assertEqual([r['model_id'] for r in result['recommendations']], [model])
                self.assertEqual(result['recommendations'][0]['resources']['access'], 'user_listed')
        self.assertFalse(harbor.route({'tasks': ['agent.workflow'], 'available_models': []}, self.data, NOW)['recommendations'])
        self.assertTrue({'gemini-4-argon', 'claude-fable-5-1'} <= set(self.models))

    def test_later_checks_cannot_support_historical_model_queries(self):
        for model in MODELS:
            with self.subTest(model=model):
                result = harbor.route({'tasks': ['agent.workflow'], 'available_models': [model]},
                                      self.data, date(2026, 11, 12))
                self.assertFalse(result['recommendations'])
                reason = next(e for e in result['excluded'] if e['model_id'] == model)
                self.assertIn('metadata_needs_refresh', reason['reasons'])

    def test_native_modalities_and_tools_remain_model_specific(self):
        for model in MODELS:
            with self.subTest(model=model):
                self.assertTrue(self.route(model, input_modalities=['text', 'image'], tools_required=True)['recommendations'])
                result = self.route(model, input_modalities=['text', 'audio', 'video'], tools_required=True)
                if model.startswith('gemini-'):
                    self.assertEqual([r['model_id'] for r in result['recommendations']], [model])
                else:
                    self.assertFalse(result['recommendations'])
                    reason = next(e for e in result['excluded'] if e['model_id'] == model)
                    self.assertIn('input_modality_not_verified', reason['reasons'])

    def test_hosted_models_are_not_local_weight_candidates(self):
        for model in MODELS:
            with self.subTest(model=model):
                result = self.route(model, open_weights_only=True)
                self.assertFalse(result['recommendations'])
                reason = next(e for e in result['excluded'] if e['model_id'] == model)
                self.assertIn('closed_weights', reason['reasons'])

    def test_context_and_price_ranges_do_not_extend_the_verified_window(self):
        for model, limit in [('gemini-4-carbon', 1_048_576), ('gemini-4-hydrogen', 1_048_576), ('claude-fable-5-2', 1_000_000)]:
            with self.subTest(model=model):
                self.assertEqual(self.models[model]['context_tokens'], limit)
                self.assertTrue(self.route(model, context_tokens=limit)['recommendations'])
                self.assertFalse(self.route(model, context_tokens=limit + 1)['recommendations'])
                ref = price.price_reference(self.models[model], self.sources, self.data['policy'], NOW, context_tokens=limit + 1)
                self.assertEqual(ref['status'], 'unknown')

    def test_standard_quotes_support_explicit_budget_caps(self):
        for model, inp, out in [('gemini-4-hydrogen', 1.5, 7.5), ('claude-fable-5-2', 8, 40)]:
            with self.subTest(model=model):
                self.assertTrue(self.route(model, max_input_price=inp, max_output_price=out)['recommendations'])
                result = self.route(model, max_input_price=inp - 0.01)
                self.assertFalse(result['recommendations'])
                reason = next(e for e in result['excluded'] if e['model_id'] == model)
                self.assertIn('input_price_over_budget', reason['reasons'])

    def test_carbon_introductory_reference_expires_without_activating_a_future_quote(self):
        model = self.models['gemini-4-carbon']
        self.assertIsNone(model['price_usd_per_million'])
        self.assertEqual(model['price_reference']['valid_until'], '2026-11-30')
        last = price.price_reference(model, self.sources, self.data['policy'], date(2026, 11, 30))
        after = price.price_reference(model, self.sources, self.data['policy'], date(2026, 12, 1))
        self.assertEqual(last['status'], 'available')
        self.assertEqual((last['tiers'][0]['input'], last['tiers'][0]['output']), (2, 10))
        self.assertEqual(after['status'], 'unknown')
        self.assertFalse(after['tiers'])
        capped = self.route('gemini-4-carbon', max_input_price=2)
        self.assertFalse(capped['recommendations'])

    def test_reference_price_mutations_preserve_rank_switching_and_cost_decisions(self):
        for caps in [{}, {'max_input_price': 10, 'max_output_price': 50}]:
            job = {'tasks': ['agent.workflow'], 'available_models': list(MODELS),
                   'current_model': 'gemini-4-hydrogen', 'priority': 'cost', **caps}
            expected = decisions(harbor.route(job, self.data, NOW))
            for quote in [None, {'currency': 'USD', 'unit': 'per_million_tokens',
                                 'verified_on': str(NOW), 'tiers': [{'max_input_tokens': 1_048_576, 'input': 0, 'output': 0}]}]:
                changed = copy.deepcopy(self.data)
                for model in changed['models']['models']:
                    if model['id'] in MODELS:
                        model['price_reference'] = ({**quote, 'source_id': model['source_id']} if quote else None)
                self.assertEqual(expected, decisions(harbor.route(job, changed, NOW)))

    def test_chinese_top_three_has_matching_prices_without_automatic_model_changes(self):
        result = harbor.route({'tasks': ['agent.workflow'], 'available_models': list(MODELS),
                               'language': 'zh-CN'}, self.data, NOW)
        self.assertEqual({r['model_id'] for r in result['recommendations']}, set(MODELS))
        text = harbor.markdown(result, self.data)
        for choice in result['recommendations']:
            row = next(line for line in text.splitlines() if line.startswith('| ') and f"`{choice['model_id']}`" in line)
            self.assertIn(price.price_cell(choice['price_reference'], 'zh-CN'), row)
        self.assertIn('价格参考', text)
        self.assertEqual(result['language'], 'zh-CN')

    def test_each_version_has_its_own_research_and_localized_task_evidence(self):
        for model in MODELS:
            with self.subTest(model=model):
                research = next(r for r in self.data['community_research']['models'] if r['id'] == model)
                rows = [e for e in self.data['evidence']['evidence'] if e['model_id'] == model]
                reports = [e for e in rows if e['kind'] == 'community_test']
                self.assertTrue(research['queries'])
                self.assertEqual(research['searched_on'], str(NOW))
                self.assertEqual(set(research['evidence_ids']), {e['id'] for e in reports})
                self.assertEqual(research['status'], 'reviewed' if reports else 'no_specific_reports')
                self.assertTrue(self.data['locale_zh']['models'][model]['notes'])
                for row in rows:
                    self.assertEqual(row['reviewed_on'], str(NOW))
                    self.assertEqual(self.sources[row['source_id']]['checked_on'], str(NOW))
                    self.assertTrue(self.sources[row['source_id']]['url'].startswith('https://'))
                    translated = self.data['locale_zh']['evidence'][row['id']]
                    self.assertTrue(all(translated[k] for k in ['claim', 'setting', 'limitations']))
                    if row['kind'] == 'community_test':
                        self.assertTrue(translated['rating_rationale'])
                        self.assertTrue(0 <= row['community']['rating']['value'] <= 10)

    def test_new_records_do_not_inherit_old_maintenance_dates(self):
        report = harbor.audit(self.data, NOW)
        for field in ['models_needing_refresh', 'community_searches_due', 'prices_needing_refresh']:
            self.assertFalse(set(MODELS) & set(report[field]))
        new_rows = {e['id'] for e in self.data['evidence']['evidence'] if e['model_id'] in MODELS}
        self.assertFalse(new_rows & set(report['stale_evidence']))

    def test_carbon_scores_keep_original_publication_age(self):
        original = {'gemini-4-carbon-terminal', 'gemini-4-carbon-computer',
                    'gemini-4-carbon-graphwalks', 'gemini-4-carbon-charts',
                    'gemini-4-carbon-riemann'}
        rows = [e for e in self.data['evidence']['evidence'] if e['id'] in original]
        self.assertEqual(len(rows), len(original))
        for row in rows:
            self.assertEqual(row['reported_on'], '2026-10-28')
            self.assertEqual(row['reviewed_on'], '2026-11-13')
            self.assertTrue(harbor.evidence_fresh(row, self.data, date(2026, 12, 12)))
            self.assertFalse(harbor.evidence_fresh(row, self.data, date(2026, 12, 13)))

    def test_scientific_terminal_results_use_consistent_task_mapping(self):
        ids = {'fable-5-2-science', 'gemini-4-hydrogen-science-terminal', 'opus-science'}
        rows = [e for e in self.data['evidence']['evidence'] if e['id'] in ids]
        self.assertEqual(len(rows), len(ids))
        for row in rows:
            self.assertIn('science.compute', row['direct_tasks'])
            self.assertNotIn('science.reasoning', row['direct_tasks'])
            self.assertIn('science.reasoning', row['proxy_tasks'])
        self.assertFalse(harbor.comparable_pairs([rows[0]], rows[1:]))

    def test_standalone_archive_recommends_the_three_models_in_chinese(self):
        spec = importlib.util.spec_from_file_location('november_packager', ROOT / 'scripts/package_skill.py')
        package = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(package)
        with tempfile.TemporaryDirectory() as directory:
            temporary = Path(directory)
            archive = package.package(temporary / 'skill.zip')
            with zipfile.ZipFile(archive) as zipped:
                zipped.extractall(temporary / 'unpacked')
            skill = temporary / 'unpacked/promptharbor'
            job = temporary / 'job.json'
            job.write_text(json.dumps({'tasks': ['agent.workflow'], 'available_models': list(MODELS),
                                       'language': 'zh-CN'}, ensure_ascii=False), encoding='utf-8')
            result = subprocess.run([sys.executable, '-X', 'utf8', str(skill / 'scripts/harbor.py'),
                                     'recommend', '--job', str(job), '--as-of', str(NOW)],
                                    capture_output=True, text=True, encoding='utf-8',
                                    env={**os.environ, 'PYTHONIOENCODING': 'utf-8'})
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn('价格参考', result.stdout)
            for model in MODELS:
                self.assertIn(f'`{model}`', result.stdout)


if __name__ == '__main__':
    unittest.main()
