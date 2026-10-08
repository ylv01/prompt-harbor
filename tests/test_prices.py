"""API price references remain explanatory across recommendations and handoffs."""
import copy
import importlib.util
import os
import re
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
import project

NOW = date(2026, 10, 8)


def selection(result):
    return {'primary': result['primary'], 'decision': result['decision'],
            'switch': result['switch'], 'excluded': result['excluded'],
            'recommendations': [(r['rank'], r['model_id'], r['reason']) for r in result['recommendations']],
            'candidates': [(r['model_id'], r['ranking'], r['covered_tasks'], r['missing_tasks'], r['resources'])
                           for r in result['candidates']]}


def top_rows(markdown):
    return [line for line in markdown.splitlines() if line.startswith('| ')
            and not line.startswith('| Rank') and not line.startswith('| 排名')]


class PriceTests(unittest.TestCase):
    def setUp(self):
        self.data = harbor.load_data()
        self.sources = {s['id']: s for s in self.data['sources']['sources']}
        self.model = copy.deepcopy(next(m for m in self.data['models']['models'] if m['id'] == 'gpt-6.1-sol'))
        self.model['price_reference'] = {
            'currency': 'USD', 'unit': 'per_million_tokens',
            'source_id': self.model['source_id'], 'verified_on': str(NOW),
            'tiers': [{'max_input_tokens': 100_000, 'input': 0.1, 'output': 0.5},
                      {'max_input_tokens': 1_000_000, 'input': 0.5, 'output': 2.5}],
        }

    def render(self, model=None, **kwargs):
        return price.price_reference(model or self.model, self.sources, self.data['policy'], NOW, **kwargs)

    def test_display_prices_cannot_change_ranking_switch_or_budget_decisions(self):
        jobs = [
            {'tasks': ['software.repo'], 'current_model': 'gpt-6.1-sol', 'priority': 'quality'},
            {'tasks': ['software.frontend'], 'current_model': 'kimi-k3', 'priority': 'cost'},
            {'tasks': ['software.repo'], 'current_model': 'gpt-6.1-sol',
             'max_input_price': 0.2, 'max_output_price': 2, 'priority': 'cost'},
        ]
        for job in jobs:
            original = harbor.route(job, self.data, NOW)
            for mode in ['expensive', 'free', 'absent', 'unknown']:
                with self.subTest(job=job, mutation=mode):
                    mutated = copy.deepcopy(self.data)
                    for model in mutated['models']['models']:
                        if mode == 'absent':
                            model.pop('price_reference', None)
                        elif mode == 'unknown':
                            model['price_reference'] = None
                        else:
                            amount = 1_000_000 if mode == 'expensive' else 0
                            model['price_reference'] = {
                                'currency': 'USD', 'unit': 'per_million_tokens',
                                'source_id': model['source_id'], 'verified_on': str(NOW),
                                'tiers': [{'max_input_tokens': 1_000_000, 'input': amount, 'output': amount}],
                            }
                    self.assertEqual(selection(original), selection(harbor.route(job, mutated, NOW)))
                    self.assertEqual(self.data['policy']['ranking'], mutated['policy']['ranking'])

    def test_boundary_selects_the_applicable_input_and_output_tier(self):
        for tokens, expected in [(100_000, (0.1, 0.5)), (100_001, (0.5, 2.5)), (1_000_000, (0.5, 2.5))]:
            with self.subTest(tokens=tokens):
                result = self.render(context_tokens=tokens)
                self.assertEqual(result['status'], 'available')
                self.assertEqual(len(result['tiers']), 1)
                self.assertEqual((result['tiers'][0]['input'], result['tiers'][0]['output']), expected)
        self.assertEqual(self.render(context_tokens=1_000_001)['status'], 'unknown')

    def test_unspecified_length_shows_all_tiers_in_both_languages(self):
        for language in ['en', 'zh-CN']:
            with self.subTest(language=language):
                result = self.render(language=language)
                self.assertEqual(len(result['tiers']), 2)
                for value in ['$0.1', '$0.5', '$2.5', '100,000', '1,000,000']:
                    self.assertIn(value, result['text'])
                self.assertIn('input tokens' if language == 'en' else '输入', result['text'])
                cell = price.price_cell(result, language)
                self.assertIn(self.sources[self.model['source_id']]['url'], cell)
                self.assertIn(str(NOW), cell)

    def test_stale_future_expired_and_unknown_prices_are_not_presented_as_current(self):
        for field, value in [('verified_on', '2026-09-01'), ('verified_on', '2026-10-09'), ('valid_until', '2026-10-07')]:
            with self.subTest(field=field, value=value):
                model = copy.deepcopy(self.model)
                model['price_reference'][field] = value
                result = self.render(model)
                self.assertEqual(result['status'], 'unknown')
                self.assertFalse(result['tiers'])
                self.assertNotIn('$0.1', result['text'])
        self.assertEqual(self.render({**self.model, 'price_reference': None})['status'], 'unknown')
        absent = copy.deepcopy(self.model)
        absent.pop('price_reference')
        absent['price_usd_per_million'] = None
        self.assertEqual(self.render(absent)['status'], 'unknown')

    def test_zero_rate_is_valid_and_expiry_is_inclusive(self):
        self.model['price_reference']['tiers'][0].update(input=0, output=0)
        self.model['price_reference']['valid_until'] = str(NOW)
        reference = self.render(context_tokens=100)
        self.assertEqual(reference['status'], 'available')
        self.assertIn('$0 / $0', reference['text'])
        self.assertFalse(price.price_refresh_due(self.model, self.data['policy'], NOW))
        self.assertTrue(price.price_refresh_due(self.model, self.data['policy'], date(2026, 10, 9)))

    def test_explicit_unknown_does_not_fall_back_to_inapplicable_legacy_rate(self):
        self.model['price_reference'] = None
        self.assertIsNotNone(self.model['price_usd_per_million'])
        self.assertEqual(self.render()['status'], 'unknown')
        self.model.pop('price_reference')
        self.assertEqual(self.render()['status'], 'available')

    def test_refresh_audit_tracks_prices_without_marking_permanent_unknown_as_overdue(self):
        model = next(m for m in self.data['models']['models'] if m['id'] == 'gpt-6.1-sol')
        model['price_reference'] = copy.deepcopy(self.model['price_reference'])
        model['price_reference']['valid_until'] = '2026-10-07'
        unknown = next(m for m in self.data['models']['models'] if m['id'] == 'qwen3.8-27b')
        unknown['price_reference'] = None
        report = harbor.audit(self.data, NOW)
        self.assertIn(model['id'], report['prices_needing_refresh'])
        self.assertNotIn(unknown['id'], report['prices_needing_refresh'])
        self.assertTrue(report['due'])
        model['price_reference'].pop('valid_until')
        self.assertNotIn(model['id'], harbor.audit(self.data, NOW)['prices_needing_refresh'])

    def test_top_three_table_preserves_rank_model_and_each_price_reference(self):
        for language in ['en', 'zh-CN']:
            with self.subTest(language=language):
                result = harbor.route({'tasks': ['software.frontend'], 'language': language}, self.data, NOW)
                self.assertEqual(len(result['recommendations']), 3)
                rendered = harbor.markdown(result, self.data)
                rows = top_rows(rendered)
                self.assertEqual(len(rows), 3)
                self.assertIn('Price reference' if language == 'en' else '价格参考', rendered)
                self.assertIn('input / output tokens' if language == 'en' else '输入 / 输出', rendered)
                for row, recommendation in zip(rows, result['recommendations']):
                    self.assertTrue(row.startswith(f"| {recommendation['rank']} |"))
                    self.assertIn(recommendation['model_id'], row)
                    self.assertIn(price.price_cell(recommendation['price_reference'], language), row)

    def test_table_has_explicit_price_cells_for_known_unknown_and_long_context_candidates(self):
        job = {'tasks': ['software.frontend'], 'context_tokens': 200_000}
        result = harbor.route(job, self.data, NOW)
        self.assertEqual(len(result['recommendations']), 3)
        ids = [r['model_id'] for r in result['recommendations']]
        for index, model_id in enumerate(ids):
            model = next(m for m in self.data['models']['models'] if m['id'] == model_id)
            if index == 1:
                model['price_reference'] = None
            else:
                model['price_reference'] = {
                    'currency': 'USD', 'unit': 'per_million_tokens',
                    'source_id': model['source_id'], 'verified_on': str(NOW),
                    'tiers': [{'max_input_tokens': 1_000_000 if index == 0 else 100_000, 'input': 1, 'output': 2}],
                }
        result = harbor.route(job, self.data, NOW)
        self.assertEqual([r['model_id'] for r in result['recommendations']], ids)
        self.assertEqual([r['price_reference']['status'] for r in result['recommendations']], ['available', 'unknown', 'unknown'])
        rows = top_rows(harbor.markdown(result, self.data))
        self.assertIn('$1 / $2', rows[0])
        self.assertIn('Unknown', rows[1])
        self.assertIn('input length', rows[2])

    def test_project_plan_and_handoffs_keep_prices_aligned_and_user_choices_intact(self):
        sample = ROOT / 'examples/library-system/project.json'
        for language in ['en', 'zh-CN']:
            with self.subTest(language=language), tempfile.TemporaryDirectory() as directory:
                output = Path(directory) / 'handoffs'
                manifest = project.compile_project(sample, output, NOW, language=language)
                plan = (output / 'PLAN.md').read_text(encoding='utf-8')
                self.assertIn('Price reference' if language == 'en' else '价格参考', plan)
                self.assertIn('Planning default' if language == 'en' else '计划默认', plan)
                for assignment in manifest['assignments']:
                    row = next(line for line in plan.splitlines() if line.startswith('| ') and f"(`{assignment['task_id']}`)" in line)
                    prompt = (output / assignment['prompt']).read_text(encoding='utf-8')
                    evidence = harbor.read_json(output / 'prompts' / (assignment['task_id'] + '.evidence.json'))
                    self.assertIn('"model_used"', prompt)
                    self.assertEqual(assignment['selection'], 'user_choice')
                    self.assertEqual([r['model_id'] for r in assignment['recommendations']],
                                     [r['model_id'] for r in evidence['recommendations']])
                    for recommendation in assignment['recommendations']:
                        ref = price.price_cell(recommendation['price_reference'], language)
                        self.assertIn(f"{recommendation['rank']}. {recommendation['name']}", row)
                        self.assertIn(f"{recommendation['rank']}. {ref}", row)
                        top_row = next(line for line in top_rows(prompt) if f"`{recommendation['model_id']}`" in line)
                        self.assertTrue(top_row.startswith(f"| {recommendation['rank']} |"))
                        self.assertIn(ref, top_row)
                report = project.verify_deliveries(output / 'manifest.json', Path(directory) / 'receipts', Path(directory) / 'artifacts')
                self.assertFalse(report['ready_for_integration_review'])

    def test_fewer_than_three_choices_does_not_invent_priced_models(self):
        for allowed in [[], ['gpt-6.1-sol']]:
            with self.subTest(available=allowed):
                result = harbor.route({'tasks': ['software.repo'], 'available_models': allowed}, self.data, NOW)
                self.assertEqual(len(top_rows(harbor.markdown(result, self.data))), len(allowed))
                self.assertEqual([r['model_id'] for r in result['recommendations']], allowed)

    def test_haiku_has_its_own_task_evidence_and_recorded_community_search(self):
        model_id = 'claude-haiku-5-5'
        model = next(m for m in self.data['models']['models'] if m['id'] == model_id)
        self.assertEqual(model['status'], 'available')
        self.assertEqual(model['context_tokens'], 1_000_000)
        self.assertEqual(set(model['input_modalities']), {'text', 'image'})
        self.assertTrue(model['tool_calling'])
        research = next(r for r in self.data['community_research']['models'] if r['id'] == model_id)
        self.assertTrue(research['queries'])
        self.assertGreaterEqual(research['searched_on'], '2026-10-07')
        rows = [e for e in self.data['evidence']['evidence'] if e['model_id'] == model_id]
        self.assertTrue(rows)
        community = [e for e in rows if e['kind'] == 'community_test']
        self.assertEqual(set(research['evidence_ids']), {e['id'] for e in community})
        if research['status'] == 'no_specific_reports':
            self.assertFalse(community)
        for row in rows:
            if row['measurement']:
                self.assertGreaterEqual(row['reviewed_on'], '2026-10-07')
                if row['reported_on'] is not None:
                    self.assertGreaterEqual(row['reported_on'], '2026-10-07')
        short = price.price_reference(model, self.sources, self.data['policy'], NOW, context_tokens=100_000)
        long = price.price_reference(model, self.sources, self.data['policy'], NOW, context_tokens=100_001)
        self.assertEqual((short['tiers'][0]['input'], short['tiers'][0]['output']), (0.1, 0.5))
        self.assertEqual((long['tiers'][0]['input'], long['tiers'][0]['output']), (0.5, 2.5))
        formal = next(e for e in rows if e['kind'] != 'community_test' and harbor.evidence_fresh(e, self.data, NOW))
        task = (formal['direct_tasks'] + formal['proxy_tasks'])[0]
        result = harbor.route({'tasks': [task], 'available_models': [model_id]}, self.data, NOW)
        self.assertEqual([r['model_id'] for r in result['recommendations']], [model_id])

    def test_standalone_archive_renders_price_references_without_repository(self):
        spec = importlib.util.spec_from_file_location('price_packager', ROOT / 'scripts/package_skill.py')
        package = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(package)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            archive = root / 'skill.zip'
            package.package(archive)
            with zipfile.ZipFile(archive) as zipped:
                self.assertIn('promptharbor/scripts/price.py', zipped.namelist())
                zipped.extractall(root / 'unpacked')
            response = subprocess.run(
                [sys.executable, '-X', 'utf8', str(root / 'unpacked/promptharbor/scripts/harbor.py'), 'recommend',
                 '--prompt', '帮我设计一个网页界面', '--language', 'zh-CN', '--as-of', str(NOW)],
                capture_output=True, text=True, encoding='utf-8', env={**os.environ, 'PYTHONIOENCODING': 'utf-8'},
            )
            self.assertEqual(response.returncode, 0, response.stderr)
            self.assertIn('| 排名 |', response.stdout)
            self.assertIn('价格参考', response.stdout)
            self.assertIn('输入 / 输出', response.stdout)

    def test_mixed_sql_repository_reason_scopes_independent_results_to_sql(self):
        for language in ['en', 'zh-CN']:
            with self.subTest(language=language):
                result = harbor.route({'tasks': ['software.repo', 'data.sql'],
                                       'available_models': ['claude-haiku-5-5'],
                                       'language': language}, self.data, NOW)
                self.assertEqual(len(result['recommendations']), 1)
                recommendation = result['recommendations'][0]
                self.assertEqual(recommendation['independent_tasks'], ['data.sql'])
                task_labels = {c['id']: c['label'] for c in result['classification']}
                clause = next(c for c in re.split('[;；]', recommendation['reason'])
                              if ('independent evaluation' if language == 'en' else '独立') in c)
                self.assertIn(task_labels['data.sql'], clause)
                self.assertNotIn(task_labels['software.repo'], clause)
                self.assertIn(task_labels['software.repo'], recommendation['reason'])
                self.assertIn('adjacent-task' if language == 'en' else '相邻', recommendation['reason'])

    def test_haiku_handoff_preserves_bounded_helper_limit_and_all_model_notes(self):
        sample = ROOT / 'examples/library-system/project.json'
        for language in ['en', 'zh-CN']:
            with self.subTest(language=language), tempfile.TemporaryDirectory() as directory:
                output = Path(directory) / 'handoffs'
                manifest = project.compile_project(sample, output, NOW, language=language)
                backend = next(a for a in manifest['assignments'] if a['task_id'] == 'backend')
                self.assertIn('claude-haiku-5-5', [r['model_id'] for r in backend['recommendations']])
                prompt = (output / backend['prompt']).read_text(encoding='utf-8')
                self.assertIn('## Model-specific limits' if language == 'en' else '## 各模型的适用限制', prompt)
                evidence = harbor.read_json(output / 'prompts/backend.evidence.json')
                for candidate in evidence['recommendations']:
                    for note in candidate['limitations']:
                        self.assertIn(note, prompt)
                self.assertIn('bounded' if language == 'en' else '范围明确', prompt)


if __name__ == '__main__':
    unittest.main()
