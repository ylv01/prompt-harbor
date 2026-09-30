"""Behavioral checks for transparent, bounded community influence and Top 3 choice."""
import contextlib
import copy
import io
import json
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'skills/promptharbor/scripts'))
import harbor
import project

NOW = date(2026, 9, 30)


def keep_evidence(data, rows):
    """Change a test catalog while preserving its research references."""
    data['evidence']['evidence'] = rows
    ids = {e['id'] for e in rows}
    for research in data['community_research']['models']:
        research['evidence_ids'] = [e for e in research['evidence_ids'] if e in ids]


def community_fixture(value=8, origin='fixture-author', task='software.frontend.design',
                      grade='firsthand', model='gpt-6-luna'):
    return {
        'id': 'fixture-' + origin,
        'model_id': model,
        'source_id': 'kimi-community-neuralhub',
        'kind': 'community_test',
        'claim': 'Synthetic report for isolating scoring behavior.',
        'direct_tasks': [task],
        'proxy_tasks': [],
        'measurement': None,
        'setting': 'Synthetic test fixture; no real evaluation is asserted.',
        'limitations': 'Synthetic test fixture.',
        'reported_on': NOW.isoformat(),
        'reviewed_on': NOW.isoformat(),
        'comparison_group': None,
        'community': {
            'author': origin,
            'origin_id': origin,
            'grade': grade,
            'stance': 'positive' if value > 5 else 'negative' if value < 5 else 'mixed',
            'artifact_urls': ['https://example.com/test-artifact'] if grade != 'firsthand' else [],
            'first_seen_on': NOW.isoformat(),
            'rating': {'value': value, 'rationale': 'Synthetic task outcome.',
                       'confidence': 'low', 'assessed_on': NOW.isoformat()}
        }
    }


class CommunityTests(unittest.TestCase):
    def setUp(self):
        self.data = harbor.load_data()
        self.job = {'tasks': ['software.frontend.design']}

    def result(self, **extra):
        return harbor.route({**self.job, **extra}, self.data, NOW)

    def kimi(self, **extra):
        return next(c for c in self.result(**extra)['candidates'] if c['model_id'] == 'kimi-k3')

    def test_top_three_are_ordered_unique_and_resource_filtered(self):
        ids = ['kimi-k3', 'gpt-6-sol', 'deepseek-v4.1-flash']
        r = self.result(available_models=ids)
        self.assertEqual([c['rank'] for c in r['recommendations']], [1, 2, 3])
        self.assertEqual({c['model_id'] for c in r['recommendations']}, set(ids))
        self.assertTrue(all(c['resources']['access'] == 'user_listed' for c in r['recommendations']))
        self.assertIn('Top 3', harbor.markdown(r))

    def test_missing_slots_not_fabricated(self):
        r = self.result(available_models=['kimi-k3'])
        self.assertEqual(len(r['recommendations']), 1)
        self.assertTrue(any('Only 1' in w for w in r['warnings']))

    def test_community_changes_recommendation_order(self):
        # Equal formal capability records isolate community influence from
        # changing real-world reports and benchmark comparisons.
        seed = next(e for e in self.data['evidence']['evidence'] if e['kind'] == 'official_capability')
        rows = []
        for model in ['gpt-6-sol', 'gpt-6-luna']:
            formal = copy.deepcopy(seed)
            formal.update(id='fixture-formal-' + model, model_id=model,
                          direct_tasks=self.job['tasks'], proxy_tasks=[], comparison_group=None)
            rows.append(formal)
        report = community_fixture(value=9, model='gpt-6-sol')
        report['source_id'] = next(e['source_id'] for e in self.data['evidence']['evidence']
                                   if e['kind'] == 'community_test')
        rows.append(report)
        keep_evidence(self.data, rows)
        allowed = ['gpt-6-luna', 'gpt-6-sol']
        off = self.result(community_weight=0, available_models=allowed)
        on = self.result(community_weight=0.3, available_models=allowed)
        self.assertEqual(off['recommendations'][0]['model_id'], 'gpt-6-luna')
        self.assertEqual(on['recommendations'][0]['model_id'], 'gpt-6-sol')
        self.assertGreater(on['recommendations'][0]['ranking']['support'],
                           on['recommendations'][1]['ranking']['support'])

    def test_reposts_do_not_multiply_support(self):
        before = self.kimi()['ranking']
        seed = next(e for e in self.data['evidence']['evidence'] if e['id'] == 'kimi-community-websites')
        for i in range(20):
            duplicate = copy.deepcopy(seed)
            duplicate['id'] = 'repost-' + str(i)
            self.data['evidence']['evidence'].append(duplicate)
        after = self.kimi()['ranking']
        self.assertEqual(before['support'], after['support'])
        self.assertEqual(before['tasks'][0]['community_origins'], after['tasks'][0]['community_origins'])

    def test_negative_feedback_reduces_support_and_remains_visible(self):
        original = copy.deepcopy(self.data)
        before = self.kimi()['ranking']['support']
        negative = next(e for e in self.data['evidence']['evidence'] if e['id'] == 'kimi-community-ui-counterpoint')
        keep_evidence(self.data, [e for e in self.data['evidence']['evidence'] if e is not negative])
        self.assertGreater(self.kimi()['ranking']['support'], before)
        self.data = original
        text = harbor.markdown(self.result(available_models=['kimi-k3']))
        self.assertIn('Another user reports preferring', text)

    def test_negative_only_evidence_cannot_recommend_a_model(self):
        keep_evidence(self.data, [e for e in self.data['evidence']['evidence']
            if e['id'] == 'kimi-community-ui-counterpoint'])
        self.assertEqual(self.result()['recommendations'], [])

    def test_zero_weight_disables_community_only_admission(self):
        keep_evidence(self.data, [e for e in self.data['evidence']['evidence']
            if e['kind'] == 'community_test'])
        self.assertTrue(self.result()['recommendations'])
        self.assertEqual(self.result(community_weight=0)['recommendations'], [])

    def test_community_does_not_override_hard_constraints(self):
        self.assertEqual(self.result(available_models=['kimi-k3'], context_tokens=2_000_000,
                                     community_weight=0.4)['recommendations'], [])

    def test_undated_evidence_is_discounted(self):
        before = self.kimi()['ranking']['tasks'][0]['community_signal']
        e = next(e for e in self.data['evidence']['evidence'] if e['id'] == 'kimi-community-websites')
        e['reported_on'] = NOW.isoformat()
        e['reviewed_on'] = NOW.isoformat()
        self.assertGreater(self.kimi()['ranking']['tasks'][0]['community_signal'], before)

    def test_undated_evidence_cannot_be_renewed_by_rereading(self):
        e = next(e for e in self.data['evidence']['evidence'] if e['id'] == 'kimi-community-websites')
        e['community']['first_seen_on'] = '2026-08-01'
        self.assertFalse(harbor.evidence_fresh(e, self.data, NOW))

    def test_known_old_reports_expire_despite_recent_review(self):
        e = next(e for e in self.data['evidence']['evidence'] if e['id'] == 'kimi-community-websites')
        e['reported_on'] = '2026-01-01'
        self.assertFalse(harbor.evidence_fresh(e, self.data, NOW))

    def test_invalid_weights_and_fake_reproduction_rejected(self):
        for weight in [-0.1, 0.41, float('nan'), True, 'high']:
            with self.subTest(weight=weight), self.assertRaises(ValueError):
                self.result(community_weight=weight)
        e = next(e for e in self.data['evidence']['evidence'] if e['id'] == 'kimi-community-websites')
        e['community']['grade'] = 'reproduced'
        with self.assertRaises(ValueError):
            harbor.validate(self.data)

    def test_visual_reports_do_not_imply_fidelity_or_database_ability(self):
        visual = next(e for e in self.data['evidence']['evidence']
                      if e['id'] == 'kimi-community-websites')
        for task in ['software.frontend.fidelity', 'data.schema']:
            assessment = harbor.community_assessment([visual], task, NOW)
            self.assertIsNone(assessment['score'])
            self.assertEqual(assessment['origin_count'], 0)

    def test_project_handoffs_offer_choices_and_actual_model_receipt(self):
        with tempfile.TemporaryDirectory() as d:
            out = Path(d) / 'handoffs'
            m = project.compile_project(ROOT/'examples/library-system/project.json', out, NOW, language='en')
            frontend = next(a for a in m['assignments'] if a['task_id'] == 'frontend')
            qa = next(a for a in m['assignments'] if a['task_id'] == 'qa')
            self.assertEqual(qa['model'], 'gpt-6-sol')
            self.assertEqual(len(frontend['recommendations']), 3)
            self.assertEqual(frontend['selection'], 'user_choice')
            prompt = (out/'prompts/frontend.md').read_text(encoding='utf-8')
            self.assertIn('Top 3 choices', prompt)
            self.assertIn('REPLACE_WITH_ACTUAL_MODEL', prompt)
            self.assertIn('same contracts', prompt)


class EditorialAssessmentTests(unittest.TestCase):
    def setUp(self):
        self.data = harbor.load_data()

    def test_score_is_task_specific_and_missing_does_not_mean_zero(self):
        report = community_fixture(value=8)
        rated = harbor.community_assessment([report], 'software.frontend.design', NOW)
        missing = harbor.community_assessment([report], 'data.schema', NOW)
        self.assertEqual(rated['score'], 8)
        self.assertEqual(rated['scale'], 10)
        self.assertEqual(rated['origin_count'], 1)
        self.assertIsNone(missing['score'])
        self.assertEqual(missing['signal'], 0)
        self.assertEqual(missing['confidence'], 'insufficient')
        self.assertEqual(missing['report_count'], 0)

    def test_duplicate_origins_cannot_inflate_score_or_signal(self):
        positive = community_fixture(value=9, origin='one-person')
        negative = community_fixture(value=3, origin='another-person')
        before = harbor.community_assessment([positive, negative], 'software.frontend.design', NOW)
        duplicates = [copy.deepcopy(positive) for _ in range(20)]
        for i, row in enumerate(duplicates):
            row['id'] += '-repost-' + str(i)
        after = harbor.community_assessment([positive, negative, *duplicates],
                                            'software.frontend.design', NOW)
        for key in ['score', 'signal', 'origin_count', 'report_count', 'confidence']:
            self.assertEqual(before[key], after[key], key)

    def test_adverse_outcome_only_affects_its_mapped_task(self):
        frontend = community_fixture(value=9, origin='frontend-success')
        debugging = community_fixture(value=2, origin='debugging-failure', task='software.debug')
        before = harbor.community_assessment([frontend], 'software.frontend.design', NOW)
        after = harbor.community_assessment([frontend, debugging], 'software.frontend.design', NOW)
        self.assertEqual(before['score'], after['score'])
        self.assertEqual(before['signal'], after['signal'])
        adverse = harbor.community_assessment([debugging], 'software.debug', NOW)
        self.assertEqual(adverse['score'], 2)
        self.assertLess(adverse['signal'], 0)

    def test_artifacts_and_direct_matches_have_more_influence(self):
        firsthand = community_fixture(value=9)
        artifact = community_fixture(value=9, grade='artifact_report')
        direct = harbor.community_assessment([artifact], 'software.frontend.design', NOW)
        anecdote = harbor.community_assessment([firsthand], 'software.frontend.design', NOW)
        self.assertGreater(direct['signal'], anecdote['signal'])
        artifact['proxy_tasks'] = ['software.frontend.fidelity']
        proxy = harbor.community_assessment([artifact], 'software.frontend.fidelity', NOW)
        self.assertLess(proxy['signal'], direct['signal'])
        self.assertAlmostEqual(proxy['signal'], direct['signal'] * 0.45, places=6)

    def test_known_revision_fix_discounts_adverse_history_without_erasing_it(self):
        row = next(e for e in self.data['evidence']['evidence']
                   if e['kind'] == 'community_test'
                   and e.get('community', {}).get('applicability', {}).get('weight') == 0.25)
        task = (row['direct_tasks'] + row['proxy_tasks'])[0]
        original = copy.deepcopy(row)
        del original['community']['applicability']
        historical = harbor.community_assessment([original], task, NOW)
        revised = harbor.community_assessment([row], task, NOW)
        self.assertLess(historical['signal'], 0)
        self.assertLess(revised['signal'], 0)
        self.assertAlmostEqual(revised['signal'], historical['signal'] * 0.25, places=6)
        self.assertEqual(revised['score'], historical['score'])
        self.assertEqual(revised['origin_count'], historical['origin_count'])
        self.assertIn(row['id'], revised['origins'][0]['evidence_ids'])

    def test_future_assessment_cannot_affect_historical_recommendation(self):
        report = community_fixture(value=9)
        report['reported_on'] = '2026-09-29'
        report['reviewed_on'] = '2026-09-29'
        report['community']['first_seen_on'] = '2026-09-29'
        report['source_id'] = next(e['source_id'] for e in self.data['evidence']['evidence']
                                   if e['kind'] == 'community_test')
        source = next(s for s in self.data['sources']['sources'] if s['id'] == report['source_id'])
        source['checked_on'] = '2026-09-29'
        source['published_on'] = None
        self.assertFalse(harbor.evidence_fresh(report, self.data, date(2026, 9, 29)))
        yesterday = harbor.community_assessment([report], 'software.frontend.design', date(2026, 9, 29))
        self.assertIsNone(yesterday['score'])
        today = harbor.community_assessment([report], 'software.frontend.design', NOW)
        self.assertEqual(today['score'], 9)

    def test_invalid_editorial_scores_rejected(self):
        seed = next(e for e in self.data['evidence']['evidence'] if e['kind'] == 'community_test')
        for value in [-1, 11, float('nan'), True, 'excellent']:
            with self.subTest(value=value):
                edited = copy.deepcopy(self.data)
                row = next(e for e in edited['evidence']['evidence'] if e['id'] == seed['id'])
                row['community']['rating']['value'] = value
                with self.assertRaises(ValueError):
                    harbor.validate(edited)
        edited = copy.deepcopy(self.data)
        next(e for e in edited['evidence']['evidence'] if e['id'] == seed['id'])['community']['rating']['assessed_on'] = '2026-10-01'
        with self.assertRaises(ValueError):
            harbor.validate(edited)

    def test_every_catalog_model_has_a_community_search_record(self):
        model_ids = {m['id'] for m in self.data['models']['models']}
        research = self.data['community_research']['models']
        self.assertEqual({r['id'] for r in research}, model_ids)
        for row in research:
            with self.subTest(model=row['id']):
                self.assertTrue(row['queries'])
                self.assertTrue(row['summary'])
                self.assertIn(row['status'], ['reviewed', 'no_specific_reports'])
        edited = copy.deepcopy(self.data)
        edited['community_research']['models'].pop()
        with self.assertRaisesRegex(ValueError, 'cover every catalog model'):
            harbor.validate(edited)

    def test_report_exposes_all_models_and_cli_scores(self):
        report = harbor.community_report(self.data, NOW)
        self.assertEqual({r['model_id'] for r in report['models']},
                         {m['id'] for m in self.data['models']['models']})
        with contextlib.redirect_stdout(io.StringIO()) as output:
            self.assertEqual(harbor.main(['community', '--as-of', NOW.isoformat()]), 0)
        cli = json.loads(output.getvalue())
        self.assertEqual(cli['as_of'], NOW.isoformat())
        self.assertEqual(len(cli['models']), len(report['models']))
        for model in cli['models']:
            for task in model['tasks']:
                self.assertEqual(task['scale'], 10)
                self.assertTrue(task['origins'])
            for row in model['reports']:
                source = cli['sources'][row['source_id']]
                self.assertTrue(source['url'].startswith('https://'))
                self.assertTrue(row['community']['rating']['rationale'])
                if row['community'].get('applicability'):
                    revision = row['community']['applicability']
                    self.assertTrue(revision['reason'])
                    self.assertTrue(cli['sources'][revision['source_id']]['url'].startswith('https://'))

    def test_new_gpt61_and_mimo_models_can_be_resource_filtered(self):
        models = {m['id']: m for m in self.data['models']['models']}
        added = ['gpt-6.1-sol'] + sorted(m for m in models if m.startswith('mimo-'))
        self.assertIn('gpt-6.1-sol', models)
        self.assertGreaterEqual(len(added), 2)
        for model in added:
            supported = next(e for e in self.data['evidence']['evidence']
                             if e['model_id'] == model and e['kind'] != 'community_test'
                             and harbor.evidence_fresh(e, self.data, NOW))
            task = (supported['direct_tasks'] + supported['proxy_tasks'])[0]
            with self.subTest(model=model, task=task):
                result = harbor.route({'tasks': [task], 'available_models': [model]}, self.data, NOW)
                self.assertEqual([r['model_id'] for r in result['recommendations']], [model])


if __name__ == '__main__':
    unittest.main()
