"""Kimi K3.1 Pro routing uses its own evidence, access limits and price references."""
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

NOW = date(2026, 10, 27)
MODEL = 'kimi-k3.1-pro'
CONTEXT = 1_048_576


def selection(result):
    return {
        'primary': result['primary'], 'decision': result['decision'],
        'switch': result['switch'], 'excluded': result['excluded'],
        'recommendations': [(r['rank'], r['model_id']) for r in result['recommendations']],
        'candidates': [(c['model_id'], c['ranking'], c['covered_tasks'], c['missing_tasks'])
                       for c in result['candidates']],
    }


class Kimi31Tests(unittest.TestCase):
    def setUp(self):
        self.data = harbor.load_data()
        self.model = next(m for m in self.data['models']['models'] if m['id'] == MODEL)
        self.sources = {s['id']: s for s in self.data['sources']['sources']}
        self.rows = [e for e in self.data['evidence']['evidence'] if e['model_id'] == MODEL]
        formal = next(e for e in self.rows if e['kind'] != 'community_test'
                      and harbor.evidence_fresh(e, self.data, NOW))
        self.task = (formal['direct_tasks'] + formal['proxy_tasks'])[0]

    def route(self, today=NOW, **extra):
        return harbor.route({'tasks': [self.task], 'available_models': [MODEL], **extra},
                            self.data, today)

    def test_exact_version_resource_selection_does_not_substitute_k3_or_aliases(self):
        result = self.route(language='zh-CN', current_model=MODEL)
        self.assertEqual([r['model_id'] for r in result['recommendations']], [MODEL])
        candidate = result['recommendations'][0]
        self.assertEqual(candidate['resources']['access'], 'user_listed')
        self.assertEqual(candidate['metadata_url'], self.sources[self.model['source_id']]['url'])
        self.assertIn('kimi-k3', {m['id'] for m in self.data['models']['models']})
        self.assertFalse(self.route(available_models=[])['recommendations'])
        alias = self.route(available_models=['k3.1-pro'])
        self.assertNotIn(MODEL, [r['model_id'] for r in alias['recommendations']])

    def test_later_verification_cannot_support_historical_queries(self):
        for historical in [date(2026, 10, 22), date(2026, 10, 26)]:
            with self.subTest(as_of=historical):
                result = self.route(historical)
                self.assertFalse(result['recommendations'])
                excluded = next(c for c in result['excluded'] if c['model_id'] == MODEL)
                self.assertIn('metadata_needs_refresh', excluded['reasons'])
                self.assertFalse(any(harbor.evidence_fresh(e, self.data, historical)
                                     for e in self.rows))
        self.assertTrue(self.route()['recommendations'])

    def test_verified_visual_inputs_and_tools_do_not_admit_native_audio(self):
        self.assertEqual(set(self.model['input_modalities']), {'text', 'image', 'video'})
        self.assertTrue(self.model['tool_calling'])
        visual = self.route(input_modalities=['text', 'image', 'video'], tools_required=True)
        self.assertEqual([r['model_id'] for r in visual['recommendations']], [MODEL])
        audio = self.route(input_modalities=['text', 'audio'])
        self.assertFalse(audio['recommendations'])
        excluded = next(c for c in audio['excluded'] if c['model_id'] == MODEL)
        self.assertIn('input_modality_not_verified', excluded['reasons'])

    def test_announced_weight_release_does_not_make_hosted_model_locally_available(self):
        self.assertFalse(self.model['open_weights'])
        for as_of in [NOW, date(2026, 11, 4)]:
            with self.subTest(as_of=as_of):
                result = self.route(as_of, open_weights_only=True)
                self.assertFalse(result['recommendations'])
                excluded = next(c for c in result['excluded'] if c['model_id'] == MODEL)
                self.assertIn('closed_weights', excluded['reasons'])
        self.assertTrue(self.route()['recommendations'])

    def test_context_and_price_boundaries_do_not_use_an_unverified_extension(self):
        self.assertEqual(self.model['context_tokens'], CONTEXT)
        permitted = self.route(context_tokens=CONTEXT)
        self.assertEqual([r['model_id'] for r in permitted['recommendations']], [MODEL])
        self.assertEqual(permitted['recommendations'][0]['price_reference']['status'], 'available')
        too_long = self.route(context_tokens=CONTEXT + 1)
        self.assertFalse(too_long['recommendations'])
        excluded = next(c for c in too_long['excluded'] if c['model_id'] == MODEL)
        self.assertIn('context_too_small_or_unknown', excluded['reasons'])
        quote = price.price_reference(self.model, self.sources, self.data['policy'], NOW,
                                      context_tokens=CONTEXT + 1)
        self.assertEqual(quote['status'], 'unknown')

    def test_verified_standard_price_supports_explicit_budgets_and_reference_display(self):
        standard = self.model['price_usd_per_million']
        self.assertEqual((standard['input'], standard['output']), (2, 10))
        result = self.route(language='zh-CN')
        reference = result['recommendations'][0]['price_reference']
        self.assertEqual(reference['status'], 'available')
        self.assertEqual(reference['source']['verified_on'], NOW.isoformat())
        self.assertEqual((reference['tiers'][0]['input'], reference['tiers'][0]['output']), (2, 10))
        self.assertTrue(reference['source']['url'].startswith('https://'))
        rendered = harbor.markdown(result, self.data)
        row = next(line for line in rendered.splitlines()
                   if line.startswith('| 1 |') and f'`{MODEL}`' in line)
        self.assertIn('$2 / $10', row)
        self.assertIn(reference['source']['url'], row)
        self.assertIn(NOW.isoformat(), row)
        capped = self.route(max_input_price=2, max_output_price=10)
        self.assertEqual([c['model_id'] for c in capped['recommendations']], [MODEL])
        below_rate = self.route(max_input_price=1.99)
        self.assertFalse(below_rate['recommendations'])
        excluded = next(c for c in below_rate['excluded'] if c['model_id'] == MODEL)
        self.assertIn('input_price_over_budget', excluded['reasons'])

    def test_price_reference_changes_do_not_change_rank_switch_or_cost_decisions(self):
        for caps in [{}, {'max_input_price': 10, 'max_output_price': 30}]:
            job = {'tasks': [self.task], 'available_models': [MODEL, 'kimi-k3', 'gemini-4-argon'],
                   'priority': 'cost', 'current_model': MODEL, **caps}
            original = selection(harbor.route(job, self.data, NOW))
            for replacement in [None, {'currency': 'USD', 'unit': 'per_million_tokens',
                                       'source_id': self.model['source_id'], 'verified_on': NOW.isoformat(),
                                       'tiers': [{'max_input_tokens': CONTEXT,
                                                  'input': 1_000_000, 'output': 1_000_000}]}]:
                with self.subTest(caps=caps, price=replacement):
                    changed = copy.deepcopy(self.data)
                    model = next(m for m in changed['models']['models'] if m['id'] == MODEL)
                    model['price_reference'] = replacement
                    self.assertEqual(original, selection(harbor.route(job, changed, NOW)))

    def test_exact_model_task_reports_and_localized_assessments_have_separate_provenance(self):
        research = next(r for r in self.data['community_research']['models'] if r['id'] == MODEL)
        community = [e for e in self.rows if e['kind'] == 'community_test']
        self.assertTrue(research['queries'])
        self.assertEqual(research['searched_on'], NOW.isoformat())
        self.assertEqual(set(research['evidence_ids']), {e['id'] for e in community})
        self.assertTrue(community)
        self.assertTrue(self.data['locale_zh']['models'][MODEL]['notes'])
        old_ids = {e['id'] for e in self.data['evidence']['evidence'] if e['model_id'] == 'kimi-k3'}
        for evidence in self.rows:
            with self.subTest(evidence=evidence['id']):
                self.assertNotIn(evidence['id'], old_ids)
                self.assertEqual(evidence['reviewed_on'], NOW.isoformat())
                if evidence['reported_on'] is not None:
                    self.assertLessEqual(evidence['reported_on'], evidence['reviewed_on'])
                self.assertEqual(self.sources[evidence['source_id']]['checked_on'], NOW.isoformat())
                self.assertTrue(self.sources[evidence['source_id']]['url'].startswith('https://'))
                localized = self.data['locale_zh']['evidence'][evidence['id']]
                self.assertTrue(all(localized[field] for field in ['claim', 'setting', 'limitations']))
                if evidence['kind'] == 'community_test':
                    assessment = evidence['community']['rating']
                    self.assertTrue(0 <= assessment['value'] <= 10)
                    self.assertIn(assessment['confidence'], ['low', 'medium', 'high'])
                    self.assertTrue(localized['rating_rationale'])

    def test_webdev_preference_evidence_uses_the_same_task_scope_as_older_models(self):
        arena = next(e for e in self.rows if e['kind'] == 'independent_eval'
                     and e['measurement']['benchmark'].startswith('Arena WebDev'))
        older = [e for e in self.data['evidence']['evidence']
                 if e['model_id'] in {'kimi-k3', 'gpt-6.1-sol'}
                 and e['kind'] == 'independent_eval' and e['measurement']
                 and e['measurement']['benchmark'].startswith('Arena WebDev')]
        self.assertTrue(older)
        for previous in older:
            with self.subTest(previous=previous['id']):
                self.assertEqual(set(arena['direct_tasks']), set(previous['direct_tasks']))
                self.assertEqual(set(arena['proxy_tasks']), set(previous['proxy_tasks']))
                self.assertFalse(harbor.comparable_pairs([arena], [previous]))
        self.assertIn('software.frontend', arena['direct_tasks'])
        self.assertIn('software.frontend.design', arena['proxy_tasks'])
        self.assertNotIn('software.frontend.design', arena['direct_tasks'])
        self.assertNotIn('software.frontend.fidelity', arena['direct_tasks'] + arena['proxy_tasks'])

    def test_current_audit_keeps_new_model_separate_from_older_maintenance_work(self):
        report = harbor.audit(self.data, NOW)
        for field in ['models_needing_refresh', 'community_searches_due', 'prices_needing_refresh']:
            self.assertNotIn(MODEL, report[field])
        self.assertFalse({e['id'] for e in self.rows} & set(report['stale_evidence']))

    def test_standalone_archive_routes_exact_model_with_chinese_price_reference(self):
        spec = importlib.util.spec_from_file_location('kimi31_packager', ROOT / 'scripts/package_skill.py')
        packager = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(packager)
        with tempfile.TemporaryDirectory() as directory:
            temporary = Path(directory)
            archive = packager.package(temporary / 'skill.zip')
            with zipfile.ZipFile(archive) as zipped:
                zipped.extractall(temporary / 'unpacked')
            skill = temporary / 'unpacked/promptharbor'
            packaged = harbor.load_data(skill)
            self.assertIn(MODEL, {m['id'] for m in packaged['models']['models']})
            job = temporary / 'job.json'
            job.write_text(json.dumps({'tasks': [self.task], 'available_models': [MODEL],
                                       'language': 'zh-CN'}, ensure_ascii=False), encoding='utf-8')
            result = subprocess.run([sys.executable, '-X', 'utf8', str(skill / 'scripts/harbor.py'),
                                     'recommend', '--job', str(job), '--as-of', NOW.isoformat()],
                                    capture_output=True, text=True, encoding='utf-8',
                                    env={**os.environ, 'PYTHONIOENCODING': 'utf-8'})
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn(f'`{MODEL}`', result.stdout)
            self.assertIn('价格参考', result.stdout)
            self.assertIn('$2 / $10', result.stdout)


if __name__ == '__main__':
    unittest.main()
