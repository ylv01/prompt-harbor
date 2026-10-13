"""Maintenance warnings keep expired evidence visible without renewing it."""
import copy
import importlib.util
import io
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from datetime import date
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'skills/promptharbor/scripts'))
import harbor

SPEC = importlib.util.spec_from_file_location('freshness_maintenance', ROOT / 'scripts/freshness.py')
freshness = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(freshness)

CLEAN = date(2026, 10, 8)
ALERT = date(2026, 10, 12)
EXPIRED = {'glm-5.3-flash-deepswe', 'glm-5.3-flash-terminal', 'glm-5.3-flash-hle-tools'}


class FreshnessTests(unittest.TestCase):
    def setUp(self):
        self.data = harbor.load_data()

    def run_cli(self, arguments, data=None):
        stdout, stderr = io.StringIO(), io.StringIO()
        with patch.object(freshness, 'load_data', return_value=self.data if data is None else data), \
                redirect_stdout(stdout), redirect_stderr(stderr):
            status = freshness.main(arguments)
        return status, stdout.getvalue(), stderr.getvalue()

    def test_actual_october_alert_retains_the_three_expired_records(self):
        original = copy.deepcopy(self.data)
        report = freshness.generate_report(self.data, ALERT)
        self.assertEqual(report['as_of'], str(ALERT))
        self.assertEqual(set(report['stale_evidence']), EXPIRED)
        self.assertTrue(report['due'])
        for key in ('models_needing_refresh', 'community_searches_due',
                    'prices_needing_refresh', 'sources_due'):
            self.assertEqual(report[key], [])
        self.assertEqual(self.data, original)
        self.assertEqual(self.data['policy']['evidence_max_age_days']['vendor_eval'], 45)
        records = {e['id']: e for e in self.data['evidence']['evidence']}
        for record_id in EXPIRED:
            self.assertEqual(records[record_id]['reported_on'], '2026-08-26')
            self.assertEqual(records[record_id]['reviewed_on'], '2026-10-08')

    def test_normal_cli_is_successful_while_due_remains_true(self):
        status, stdout, stderr = self.run_cli(['--as-of', str(ALERT)])
        self.assertEqual(status, 0)
        self.assertEqual(stderr, '')
        report = json.loads(stdout)
        self.assertTrue(report['due'])
        self.assertEqual(set(report['stale_evidence']), EXPIRED)

    def test_explicit_strict_gate_still_exits_one(self):
        status, stdout, stderr = self.run_cli(['--as-of', str(ALERT), '--fail-due'])
        self.assertEqual(status, 1)
        self.assertEqual(stderr, '')
        self.assertTrue(json.loads(stdout)['due'])

    def test_clean_snapshot_has_no_due_items_or_github_warning(self):
        report = freshness.generate_report(self.data, CLEAN)
        self.assertFalse(report['due'])
        self.assertEqual(report['stale_evidence'], [])
        status, stdout, stderr = self.run_cli(
            ['--as-of', str(CLEAN), '--github-actions', '--fail-due'])
        self.assertEqual(status, 0)
        self.assertEqual(stderr, '')
        self.assertNotIn('::warning', stdout)
        self.assertFalse(json.loads(stdout)['due'])

    def test_github_warning_and_artifact_keep_json_and_summary_readable(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / 'freshness.json'
            summary = Path(directory) / 'summary.md'
            status, stdout, stderr = self.run_cli([
                '--as-of', str(ALERT), '--output', str(output),
                '--summary', str(summary), '--github-actions'])
            self.assertEqual(status, 0)
            self.assertEqual(stderr, '')
            self.assertIn('::warning', stdout)
            self.assertEqual(json.loads(output.read_text(encoding='utf-8')),
                             freshness.generate_report(self.data, ALERT))
            rendered = summary.read_text(encoding='utf-8')
            self.assertIn(str(ALERT), rendered)
            for record_id in EXPIRED:
                self.assertIn(record_id, rendered)
            self.assertIn('47 days (limit 45)', rendered)
            self.assertIn('excluded from current recommendations', rendered)

    def test_summary_explains_original_age_and_links_the_actual_source(self):
        report = freshness.generate_report(self.data, ALERT)
        summary = freshness.markdown_summary(report, self.data)
        records = {e['id']: e for e in self.data['evidence']['evidence']}
        sources = {s['id']: s for s in self.data['sources']['sources']}
        for record_id in EXPIRED:
            row = next(line for line in summary.splitlines() if f'`{record_id}`' in line)
            record = records[record_id]
            self.assertIn(record['model_id'], row)
            self.assertIn('2026-08-26', row)
            self.assertIn('2026-10-08', row)
            self.assertIn('reported_on: 47 days (limit 45)', row)
            self.assertIn(sources[record['source_id']]['url'], row)
        self.assertIn('historical inspection', summary)
        self.assertIn('does not reset its report date', summary)

    def test_source_review_queue_is_preserved_even_if_evidence_is_fresh(self):
        data = copy.deepcopy(self.data)
        source = next(s for s in data['sources']['sources']
                      if s['published_on'] is None)
        source['checked_on'] = '2026-09-23'
        report = freshness.generate_report(data, CLEAN)
        self.assertTrue(report['due'])
        self.assertIn({'id': source['id'], 'url': source['url']}, report['sources_due'])
        summary = freshness.markdown_summary(report, data)
        self.assertIn(source['url'], summary)
        self.assertIn('2026-09-23', summary)

    def test_invalid_catalog_returns_two_without_writing_misleading_outputs(self):
        invalid = copy.deepcopy(self.data)
        invalid['evidence']['evidence'][0]['source_id'] = 'missing-source'
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / 'freshness.json'
            summary = Path(directory) / 'summary.md'
            status, stdout, stderr = self.run_cli([
                '--as-of', str(ALERT), '--output', str(output),
                '--summary', str(summary), '--github-actions'], invalid)
            self.assertEqual(status, 2)
            self.assertEqual(stdout, '')
            self.assertIn('Freshness report failed', stderr)
            self.assertFalse(output.exists())
            self.assertFalse(summary.exists())

    def test_unreadable_catalog_is_an_error_instead_of_a_maintenance_warning(self):
        stdout, stderr = io.StringIO(), io.StringIO()
        with patch.object(freshness, 'load_data', side_effect=OSError('catalog unavailable')), \
                redirect_stdout(stdout), redirect_stderr(stderr):
            status = freshness.main(['--as-of', str(ALERT), '--github-actions'])
        self.assertEqual(status, 2)
        self.assertEqual(stdout.getvalue(), '')
        self.assertIn('catalog unavailable', stderr.getvalue())

    def test_expired_vendor_evidence_stays_out_of_routing_without_retiring_model(self):
        result = harbor.route({'tasks': ['software.repo', 'software.terminal'],
                               'available_models': ['glm-5.3-flash']}, self.data, ALERT)
        self.assertEqual([c['model_id'] for c in result['candidates']], ['glm-5.3-flash'])
        admitted = {e['id'] for c in result['candidates'] for e in c['evidence']}
        self.assertTrue(admitted)
        self.assertFalse(admitted & EXPIRED)
        for record_id in EXPIRED:
            record = next(e for e in self.data['evidence']['evidence'] if e['id'] == record_id)
            self.assertFalse(harbor.evidence_fresh(record, self.data, ALERT))


if __name__ == '__main__':
    unittest.main()
