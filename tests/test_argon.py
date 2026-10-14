"""Gemini 4 Argon stays task grounded, resource constrained and price transparent."""
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

NOW = date(2026, 10, 14)
MODEL = 'gemini-4-argon'
CONTEXT = 1_048_576


def selection(result):
    """Compare decisions independently of their explanatory price cells."""
    return {
        'primary': result['primary'], 'decision': result['decision'],
        'switch': result['switch'], 'excluded': result['excluded'],
        'recommendations': [(r['rank'], r['model_id']) for r in result['recommendations']],
        'candidates': [(c['model_id'], c['ranking'], c['covered_tasks'], c['missing_tasks'])
                       for c in result['candidates']],
    }


class ArgonTests(unittest.TestCase):
    def setUp(self):
        self.data = harbor.load_data()
        self.model = next(m for m in self.data['models']['models'] if m['id'] == MODEL)
        self.sources = {s['id']: s for s in self.data['sources']['sources']}
        self.rows = [e for e in self.data['evidence']['evidence'] if e['model_id'] == MODEL]
        self.formal = next(e for e in self.rows if e['kind'] != 'community_test'
                           and harbor.evidence_fresh(e, self.data, NOW))
        self.task = (self.formal['direct_tasks'] + self.formal['proxy_tasks'])[0]

    def route(self, today=NOW, **extra):
        return harbor.route({'tasks': [self.task], 'available_models': [MODEL], **extra},
                            self.data, today)

    def test_exact_resource_selection_keeps_argon_without_inventing_other_models(self):
        result = self.route(language='zh-CN', current_model=MODEL)
        self.assertEqual([r['model_id'] for r in result['recommendations']], [MODEL])
        self.assertEqual(result['recommendations'][0]['resources']['access'], 'user_listed')
        self.assertEqual(result['recommendations'][0]['metadata_url'],
                         self.sources[self.model['source_id']]['url'])
        self.assertFalse(self.route(available_models=[])['recommendations'])
        self.assertFalse(self.route(available_models=['gemini-argon'])['recommendations'])

    def test_historical_query_cannot_use_later_verification_or_evidence(self):
        for today in [date(2026, 10, 12), date(2026, 10, 13)]:
            with self.subTest(today=today):
                result = self.route(today)
                self.assertFalse(result['recommendations'])
                excluded = next(e for e in result['excluded'] if e['model_id'] == MODEL)
                self.assertIn('metadata_needs_refresh', excluded['reasons'])
                self.assertFalse(any(harbor.evidence_fresh(e, self.data, today)
                                     for e in self.rows))
        self.assertTrue(self.route()['recommendations'])

    def test_native_modalities_and_tools_do_not_imply_open_weights(self):
        self.assertEqual(set(self.model['input_modalities']), {'text', 'image', 'audio', 'video'})
        self.assertTrue(self.model['tool_calling'])
        result = self.route(input_modalities=['text', 'image', 'audio', 'video'], tools_required=True)
        self.assertEqual([r['model_id'] for r in result['recommendations']], [MODEL])
        local = self.route(open_weights_only=True, tools_required=True)
        self.assertFalse(local['recommendations'])
        excluded = next(e for e in local['excluded'] if e['model_id'] == MODEL)
        self.assertIn('closed_weights', excluded['reasons'])

    def test_context_capacity_is_one_combined_budget_with_verified_price_bounds(self):
        self.assertEqual(self.model['context_tokens'], CONTEXT)
        result = self.route(context_tokens=CONTEXT)
        self.assertEqual([r['model_id'] for r in result['recommendations']], [MODEL])
        self.assertEqual(result['recommendations'][0]['price_reference']['status'], 'available')
        too_long = self.route(context_tokens=CONTEXT + 1)
        self.assertFalse(too_long['recommendations'])
        excluded = next(e for e in too_long['excluded'] if e['model_id'] == MODEL)
        self.assertIn('context_too_small_or_unknown', excluded['reasons'])
        reference = price.price_reference(self.model, self.sources, self.data['policy'], NOW,
                                          context_tokens=CONTEXT + 1)
        self.assertEqual(reference['status'], 'unknown')
        notes = ' '.join(self.model['notes']).lower()
        self.assertIn('input', notes)
        self.assertIn('output', notes)
        self.assertTrue('combined' in notes or 'shared' in notes or 'unified' in notes)

    def test_introductory_price_expires_without_automatically_claiming_future_rates(self):
        reference = self.model['price_reference']
        self.assertEqual(reference['valid_until'], '2026-11-30')
        for tokens in [1, 1_000_000, CONTEXT]:
            with self.subTest(tokens=tokens):
                rendered = price.price_reference(self.model, self.sources, self.data['policy'], NOW,
                                                  context_tokens=tokens)
                self.assertEqual(rendered['status'], 'available')
                self.assertEqual((rendered['tiers'][0]['input'], rendered['tiers'][0]['output']), (2, 10))
                self.assertTrue(rendered['source']['url'].startswith('https://'))
        # Rechecking an introductory offer does not extend its announced deadline.
        refreshed = copy.deepcopy(self.model)
        refreshed['price_reference']['verified_on'] = '2026-11-30'
        final_day = price.price_reference(refreshed, self.sources, self.data['policy'], date(2026, 11, 30))
        expired = price.price_reference(refreshed, self.sources, self.data['policy'], date(2026, 12, 1))
        self.assertEqual(final_day['status'], 'available')
        self.assertEqual(expired['status'], 'unknown')
        self.assertFalse(expired['tiers'])
        self.assertTrue(price.price_refresh_due(refreshed, self.data['policy'], date(2026, 12, 1)))

    def test_community_reports_have_their_own_search_sources_and_chinese_assessments(self):
        research = next(r for r in self.data['community_research']['models'] if r['id'] == MODEL)
        reports = [e for e in self.rows if e['kind'] == 'community_test']
        self.assertTrue(research['queries'])
        self.assertEqual(research['searched_on'], NOW.isoformat())
        self.assertEqual(set(research['evidence_ids']), {e['id'] for e in reports})
        self.assertEqual(research['status'], 'reviewed' if reports else 'no_specific_reports')
        self.assertTrue(self.data['locale_zh']['models'][MODEL]['notes'])
        for row in self.rows:
            with self.subTest(evidence=row['id']):
                self.assertEqual(row['reviewed_on'], NOW.isoformat())
                self.assertTrue(self.sources[row['source_id']]['url'].startswith('https://'))
                localized = self.data['locale_zh']['evidence'][row['id']]
                for field in ['claim', 'setting', 'limitations']:
                    self.assertTrue(localized[field])
                if row['kind'] == 'community_test':
                    rating = row['community']['rating']
                    self.assertTrue(0 <= rating['value'] <= 10)
                    self.assertTrue(rating['rationale'])
                    self.assertTrue(localized['rating_rationale'])
                    self.assertIn(rating['confidence'], ['low', 'medium', 'high'])

    def test_argon_display_prices_do_not_change_selection_or_budget_eligibility(self):
        allowed = [MODEL, 'claude-opus-5-5', 'gemini-3.8-flash']
        for budget in [{}, {'max_input_price': 10, 'max_output_price': 30}]:
            job = {'tasks': [self.task], 'available_models': allowed, 'current_model': MODEL,
                   'priority': 'cost', **budget}
            original = selection(harbor.route(job, self.data, NOW))
            for replacement in [None, {'currency': 'USD', 'unit': 'per_million_tokens',
                                       'source_id': self.model['source_id'], 'verified_on': NOW.isoformat(),
                                       'tiers': [{'max_input_tokens': CONTEXT,
                                                  'input': 1_000_000, 'output': 1_000_000}]}]:
                with self.subTest(budget=budget, price=replacement):
                    changed = copy.deepcopy(self.data)
                    model = next(m for m in changed['models']['models'] if m['id'] == MODEL)
                    model['price_reference'] = replacement
                    self.assertEqual(original, selection(harbor.route(job, changed, NOW)))

    def test_display_offer_does_not_satisfy_an_unverified_selection_price_cap(self):
        self.assertIsNone(self.model['price_usd_per_million'])
        self.assertEqual(self.route()['recommendations'][0]['price_reference']['status'], 'available')
        capped = self.route(max_input_price=2)
        self.assertFalse(capped['recommendations'])
        excluded = next(e for e in capped['excluded'] if e['model_id'] == MODEL)
        self.assertIn('input_price_unknown_for_request', excluded['reasons'])

    def test_current_audit_does_not_treat_new_argon_records_as_due(self):
        audit = harbor.audit(self.data, NOW)
        for field in ['models_needing_refresh', 'community_searches_due', 'prices_needing_refresh']:
            self.assertNotIn(MODEL, audit[field])
        self.assertFalse({e['id'] for e in self.rows} & set(audit['stale_evidence']))

    def test_standalone_archive_can_route_only_argon_in_chinese(self):
        spec = importlib.util.spec_from_file_location('argon_packager', ROOT / 'scripts/package_skill.py')
        package = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(package)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            archive = package.package(root / 'skill.zip')
            with zipfile.ZipFile(archive) as zipped:
                zipped.extractall(root / 'unpacked')
            skill = root / 'unpacked/promptharbor'
            packaged = harbor.load_data(skill)
            self.assertIn(MODEL, {m['id'] for m in packaged['models']['models']})
            job = root / 'job.json'
            job.write_text(json.dumps({'tasks': [self.task], 'available_models': [MODEL],
                                       'language': 'zh-CN'}, ensure_ascii=False), encoding='utf-8')
            result = subprocess.run(
                [sys.executable, '-X', 'utf8', str(skill / 'scripts/harbor.py'), 'recommend',
                 '--job', str(job), '--as-of', NOW.isoformat()],
                capture_output=True, text=True, encoding='utf-8',
                env={**os.environ, 'PYTHONIOENCODING': 'utf-8'},
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn(f'`{MODEL}`', result.stdout)
            self.assertIn('价格参考', result.stdout)
            self.assertIn('$2 / $10', result.stdout)


if __name__ == '__main__':
    unittest.main()
