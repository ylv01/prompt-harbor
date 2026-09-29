"""Behavioral checks for transparent, bounded community influence and Top 3 choice."""
import copy
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'skills/promptharbor/scripts'))
import harbor
import project

NOW = date(2026, 9, 29)


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
        # These models have equal synthetic formal observations; isolate community effect.
        for e in self.data['evidence']['evidence']:
            if e['source_id'] == 'arena-webdev':
                e['measurement']['value'] = 1600
        allowed = ['kimi-k3', 'gpt-6-sol']
        off = self.result(community_weight=0, available_models=allowed)
        on = self.result(community_weight=0.3, available_models=allowed)
        self.assertEqual(off['recommendations'][0]['model_id'], 'gpt-6-sol')
        self.assertEqual(on['recommendations'][0]['model_id'], 'kimi-k3')

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
        before = self.kimi()['ranking']['support']
        negative = next(e for e in self.data['evidence']['evidence'] if e['id'] == 'kimi-community-ui-counterpoint')
        self.data['evidence']['evidence'].remove(negative)
        self.assertGreater(self.kimi()['ranking']['support'], before)
        self.data['evidence']['evidence'].append(negative)
        text = harbor.markdown(self.result(available_models=['kimi-k3']))
        self.assertIn('Another user reports preferring', text)

    def test_negative_only_evidence_cannot_recommend_a_model(self):
        self.data['evidence']['evidence'] = [e for e in self.data['evidence']['evidence']
            if e['id'] == 'kimi-community-ui-counterpoint']
        self.assertEqual(self.result()['recommendations'], [])

    def test_zero_weight_disables_community_only_admission(self):
        self.data['evidence']['evidence'] = [e for e in self.data['evidence']['evidence']
            if e['kind'] == 'community_test']
        self.assertTrue(self.result()['recommendations'])
        self.assertEqual(self.result(community_weight=0)['recommendations'], [])

    def test_community_does_not_override_hard_constraints(self):
        self.assertEqual(self.result(available_models=['kimi-k3'], context_tokens=2_000_000,
                                     community_weight=0.4)['recommendations'], [])

    def test_undated_evidence_is_discounted(self):
        before = self.kimi()['ranking']['tasks'][0]['community_signal']
        e = next(e for e in self.data['evidence']['evidence'] if e['id'] == 'kimi-community-websites')
        e['reported_on'] = '2026-09-29'
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

    def test_no_frontend_fidelity_or_backend_extrapolation(self):
        for task in ['software.frontend.fidelity', 'data.schema']:
            self.assertFalse(harbor.route({'tasks': [task]}, self.data, NOW)['recommendations'])

    def test_project_handoffs_offer_choices_and_actual_model_receipt(self):
        with tempfile.TemporaryDirectory() as d:
            out = Path(d) / 'handoffs'
            m = project.compile_project(ROOT/'examples/library-system/project.json', out, NOW)
            frontend = next(a for a in m['assignments'] if a['task_id'] == 'frontend')
            qa = next(a for a in m['assignments'] if a['task_id'] == 'qa')
            self.assertEqual(qa['model'], 'gpt-6-sol')
            self.assertEqual(len(frontend['recommendations']), 3)
            self.assertEqual(frontend['selection'], 'user_choice')
            prompt = (out/'prompts/frontend.md').read_text(encoding='utf-8')
            self.assertIn('Top 3 choices', prompt)
            self.assertIn('REPLACE_WITH_ACTUAL_MODEL', prompt)
            self.assertIn('same contracts', prompt)


if __name__ == '__main__':
    unittest.main()
