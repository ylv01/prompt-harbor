import copy
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
UPDATED = date(2026, 10, 8)


class RecommendationTests(unittest.TestCase):
    def setUp(self):
        self.data = harbor.load_data()

    def run_job(self, **kwargs):
        return harbor.route(kwargs, self.data, NOW)

    def test_catalog_links_are_valid(self):
        self.assertTrue(harbor.validate(self.data))

    def test_retired_sol_is_removed_without_relabeling_its_evidence(self):
        models = {m['id'] for m in self.data['models']['models']}
        self.assertNotIn('gpt-6-sol', models)
        self.assertIn('gpt-6.1-sol', models)
        self.assertNotIn('gpt-6-sol', self.data['locale_zh']['models'])
        self.assertFalse(any(e['model_id'] == 'gpt-6-sol'
                             for e in self.data['evidence']['evidence']))
        self.assertFalse(any(e['id'].startswith('gpt-6-sol-')
                             for e in self.data['evidence']['evidence']))

    def test_native_video_excludes_text_image_only_models(self):
        r = harbor.route({'tasks': ['vision.video'], 'current_model': 'gpt-6.1-sol'},
                         self.data, UPDATED)
        self.assertNotIn('gpt-6.1-sol', [m['model_id'] for m in r['candidates']])
        self.assertEqual(r['switch']['action'], 'consider_switch')
        self.assertIn('gemini-3.8-flash', [m['model_id'] for m in r['candidates']])

    def test_missing_database_evidence_is_not_a_zero_score(self):
        # This catalog model has no database-specific evidence. Other models may
        # gain real task reports as the catalog grows.
        r = self.run_job(tasks=['data.schema'], available_models=['gpt-6-luna'])
        self.assertIsNone(r['primary'])
        self.assertEqual(r['decision'], 'insufficient_evidence')

    def test_quant_is_not_claimed_as_direct_finance_evidence(self):
        r = self.run_job(tasks=['finance.backtest'])
        self.assertTrue(r['candidates'])
        self.assertTrue(all(not m['direct_tasks'] for m in r['candidates']))
        self.assertIn('look-ahead', r['validation'][0])

    def test_finance_proxy_is_not_exclusive_to_one_vendor(self):
        r = self.run_job(tasks=['finance.backtest','software.repo'])
        self.assertIsNone(r['primary'])
        self.assertGreaterEqual(len([c for c in r['candidates'] if not c['missing_tasks']]), 3)

    def test_empty_allowed_models_means_none(self):
        self.assertFalse(self.run_job(tasks=['software.repo'], available_models=[])['candidates'])

    def test_unknown_current_model_stays_unknown(self):
        r = self.run_job(tasks=['software.repo'], current_model='mystery-model')
        self.assertEqual(r['switch']['action'], 'unknown')

    def test_missing_current_model_not_inferred(self):
        self.assertEqual(self.run_job(tasks=['software.repo'])['switch']['action'], 'unknown')

    def test_routine_current_model_does_not_trigger_upsell(self):
        r = self.run_job(tasks=['general.everyday'], current_model='gpt-6-luna')
        self.assertEqual(r['switch']['action'], 'stay')

    def test_local_requirement_excludes_closed_weights(self):
        r = self.run_job(tasks=['software.repo'], open_weights_only=True)
        allowed = {m['id'] for m in self.data['models']['models'] if m['open_weights']}
        self.assertTrue(r['candidates'])
        self.assertTrue({m['model_id'] for m in r['candidates']} <= allowed)

    def test_mimo_hosted_acceleration_is_not_a_local_weights_option(self):
        available = ['mimo-v2.6-pro-ultraspeed', 'mimo-v2.6-pro', 'mimo-v2.6-flash']
        r = self.run_job(tasks=['software.repo'], available_models=available,
                         open_weights_only=True)
        self.assertEqual({m['model_id'] for m in r['candidates']},
                         {'mimo-v2.6-pro', 'mimo-v2.6-flash'})
        acceleration = next(m for m in r['excluded'] if m['model_id'] == 'mimo-v2.6-pro-ultraspeed')
        self.assertIn('closed_weights', acceleration['reasons'])

    def test_glm_video_routing_respects_the_specific_variant(self):
        result = harbor.route({'tasks': ['vision.video'],
                               'current_model': 'glm-5.3',
                               'available_models': ['glm-5.3', 'glm-5.3-flash']},
                              self.data, UPDATED)
        self.assertEqual([r['model_id'] for r in result['recommendations']], ['glm-5.3-flash'])
        self.assertNotIn('glm-5.3', [c['model_id'] for c in result['candidates']])
        self.assertEqual(result['switch']['action'], 'consider_switch')

    def test_glm_context_and_budget_constraints_apply_to_recommendations(self):
        available = ['glm-5.3', 'glm-5.3-flash']
        too_long = harbor.route({'tasks': ['software.repo'], 'available_models': available,
                                 'context_tokens': 1_000_001}, self.data, UPDATED)
        self.assertFalse(too_long['recommendations'])
        affordable = harbor.route({'tasks': ['software.repo'], 'available_models': available,
                                    'open_weights_only': True, 'tools_required': True,
                                    'max_input_price': 0.2}, self.data, UPDATED)
        self.assertEqual([r['model_id'] for r in affordable['recommendations']], ['glm-5.3-flash'])

    def test_old_snapshot_cannot_claim_current_winner(self):
        r = harbor.route({'tasks':['software.repo']}, self.data, date(2027,1,1))
        self.assertFalse(r['candidates'])
        self.assertEqual(r['decision'], 'insufficient_evidence')

    def test_review_does_not_renew_old_measurement(self):
        e = self.data['evidence']['evidence'][0]
        e['reported_on'] = '2025-01-01'
        self.assertFalse(harbor.evidence_fresh(e, self.data, NOW))

    def test_future_metadata_is_ineligible(self):
        r = harbor.route({'tasks':['software.repo']}, self.data, date(2026,1,1))
        self.assertFalse(r['candidates'])

    def test_missing_price_fails_budget_cap(self):
        r = self.run_job(tasks=['finance.filings'], max_input_price=1)
        self.assertFalse(r['candidates'])

    def test_unknown_long_context_tier_fails_price_cap(self):
        # Verified MiMo rates cover long inputs. Isolate providers whose
        # recorded standard tier stops before this input size.
        models = [m['id'] for m in self.data['models']['models']
                  if m['provider'] in ['OpenAI', 'Anthropic']]
        r = self.run_job(tasks=['software.repo'], max_input_price=100,
                         context_tokens=500000, available_models=models)
        self.assertFalse(r['candidates'])

    def test_context_does_not_use_unverified_extension(self):
        r = self.run_job(tasks=['software.repo'], available_models=['qwen3.8-27b'], context_tokens=500000)
        self.assertFalse(r['candidates'])

    def test_no_global_quality_score(self):
        r = self.run_job(tasks=['software.repo'])
        self.assertTrue(all('score' not in c for c in r['candidates']))
        self.assertEqual(r['confidence'], 'limited')

    def test_different_harness_scores_are_not_compared(self):
        a = next(e for e in self.data['evidence']['evidence'] if e['id']=='astra-terminal')
        b = next(e for e in self.data['evidence']['evidence'] if e['id']=='opus-terminal')
        self.assertFalse(harbor.comparable_pairs([a],[b]))

    def test_known_comparison_group_selects_provisional_leader(self):
        r = self.run_job(tasks=['vision.chart'], available_models=['claude-opus-5-5','claude-sonnet-5-5'])
        self.assertEqual(r['primary'], 'claude-opus-5-5')
        self.assertEqual(r['decision'], 'provisional')

    def test_comparison_group_rejects_mixed_protocols(self):
        e = next(e for e in self.data['evidence']['evidence'] if e['id']=='opus-chart')
        e['measurement']['protocol'] = 'different harness'
        with self.assertRaises(ValueError):
            harbor.validate(self.data)

    def test_duplicates_and_broken_sources_rejected(self):
        self.data['models']['models'][0]['source_id']='missing'
        with self.assertRaises(ValueError):
            harbor.validate(self.data)

    def test_malformed_jobs_rejected(self):
        for job in ({'tasks':['unknown']}, {'tasks':[]}, {'tasks':['software.repo'],'tools_required':'yes'},
                    {'tasks':['software.repo'],'context_tokens':-1}, {'tasks':['software.repo'],'max_input_price':float('nan')},
                    {'tasks':['software.repo'],'context_tokens':1.5}, {'tasks':['software.repo'],'made_up':True}):
            with self.subTest(job=job), self.assertRaises(ValueError):
                harbor.validate_job(job, self.data)

    def test_lexical_baseline_declares_its_limits(self):
        for prompt, leaf in [('检查 Python 回测的未来函数','finance.backtest'),('Review this SQL query','data.sql'),
                             ('帮我翻译这句话','writing.translation'),('Summarize this video','vision.video')]:
            job=harbor.classify(prompt,self.data)
            self.assertIn(leaf,job['tasks'])
            self.assertEqual(job['classification_confidence'],'low')

    def test_empty_prompt_rejected(self):
        with self.assertRaises(ValueError):
            harbor.classify('  ', self.data)


class ProjectTests(unittest.TestCase):
    def setUp(self):
        self.data=harbor.load_data()
        self.sample=ROOT/'examples/library-system/project.json'
        self.p=harbor.read_json(self.sample)

    def test_dependency_batches(self):
        self.assertEqual(project.validate_project(self.p,self.data), [['frontend','database'],['backend'],['qa']])

    def test_cycle_rejected(self):
        self.p['tasks'][0]['depends_on']=['qa']
        with self.assertRaisesRegex(ValueError,'cycle'):
            project.validate_project(self.p,self.data)

    def test_duplicate_owners_rejected(self):
        self.p['tasks'][1]['deliverables'].append(self.p['tasks'][0]['deliverables'][0])
        with self.assertRaisesRegex(ValueError,'same deliverable'):
            project.validate_project(self.p,self.data)

    def test_shared_hard_constraint_cannot_be_bypassed(self):
        self.p['constraints']['open_weights_only']=True
        self.p['tasks'][0]['job']['open_weights_only']=False
        with self.assertRaisesRegex(ValueError,'hard constraint'):
            project.validate_project(self.p,self.data)

    def test_unsafe_paths_rejected(self):
        for path in ('../secret','/tmp/key','C:/key','x\\y','a/../b','a//b'):
            with self.subTest(path=path), self.assertRaises(ValueError):
                project.safe_relative(path)

    def test_compilation_produces_complete_prompts(self):
        with tempfile.TemporaryDirectory() as d:
            out=Path(d)/'handoffs'
            m=project.compile_project(self.sample,out,UPDATED,language='en')
            self.assertEqual(len(m['assignments']),4)
            db=next(a for a in m['assignments'] if a['task_id']=='database')
            self.assertEqual(db['model'],'gpt-6.1-sol')
            self.assertIn('baseline',db['reason'])
            backend=(out/'prompts/backend.md').read_text(encoding='utf-8')
            self.assertIn('database/001_schema.sql',backend)
            self.assertIn('BOOK_NOT_FOUND',backend)
            self.assertIn(m['contracts'][0]['version'],backend)
            self.assertTrue((out/'prompts/frontend.evidence.json').exists())
            with self.assertRaisesRegex(ValueError,'already exists'):
                project.compile_project(self.sample,out,NOW)

    def test_planning_default_respects_only_non_openai_resources(self):
        # The sample declares a current model. A user with another provider's
        # model gets the same planning behavior without an OpenAI dependency.
        allowed = {'kimi-k3'}
        for declared_current in ['kimi-k3', None]:
            with self.subTest(current_model=declared_current), tempfile.TemporaryDirectory() as d:
                value = copy.deepcopy(self.p)
                value['constraints']['available_models'] = sorted(allowed)
                if declared_current:
                    value['constraints']['current_model'] = declared_current
                else:
                    value['constraints'].pop('current_model', None)
                for task in value['tasks']:
                    task.pop('recommended_model', None)
                    task.pop('assignment_reason', None)
                root = Path(d)
                for contract in value['contracts']:
                    target = root / contract['path']
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_bytes((self.sample.parent / contract['path']).read_bytes())
                path = root / 'project.json'
                path.write_text(json.dumps(value, ensure_ascii=False), encoding='utf-8')
                manifest = project.compile_project(path, root / 'handoffs', UPDATED, language='en')
                for assignment in manifest['assignments']:
                    self.assertIn(assignment['model'], allowed | {None})
                    self.assertEqual(assignment['selection'], 'user_choice')
                    self.assertTrue({r['model_id'] for r in assignment['recommendations']} <= allowed)
                if declared_current:
                    database = next(a for a in manifest['assignments'] if a['task_id'] == 'database')
                    self.assertEqual(database['model'], declared_current)
                    self.assertIn('baseline', database['reason'])

    def test_stale_assignment_fails_before_output_creation(self):
        with tempfile.TemporaryDirectory() as d:
            out=Path(d)/'handoffs'
            with self.assertRaisesRegex(ValueError,'not evidence-eligible'):
                project.compile_project(self.sample,out,date(2027,1,1))
            self.assertFalse(out.exists())

    def test_missing_receipts_cannot_pass(self):
        with tempfile.TemporaryDirectory() as d:
            out=Path(d)/'handoffs'
            project.compile_project(self.sample,out,UPDATED)
            report=project.verify_deliveries(out/'manifest.json',Path(d)/'receipts',Path(d)/'artifacts')
            self.assertFalse(report['ready_for_integration_review'])

    def test_receipts_require_files_checks_and_matching_contracts(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); out=root/'handoffs'; receipts=root/'receipts'; artifacts=root/'artifacts'
            receipts.mkdir(); artifacts.mkdir()
            m=project.compile_project(self.sample,out,UPDATED,language='en')
            for a in m['assignments']:
                for path in a['deliverables']:
                    target=artifacts/path; target.parent.mkdir(parents=True,exist_ok=True); target.write_text('test fixture',encoding='utf-8')
                receipt={'task_id':a['task_id'],'status':'complete','files':a['deliverables'],
                         'contracts':{c['id']:c['version'] for c in m['contracts']},
                         'checks':[{'command':'fixture check','result':'passed','evidence':'fixture only'}]}
                (receipts/(a['task_id']+'.json')).write_text(json.dumps(receipt),encoding='utf-8')
            report=project.verify_deliveries(out/'manifest.json',receipts,artifacts)
            self.assertTrue(report['ready_for_integration_review'])
            self.assertIn('not code correctness',report['notice'])
            first=receipts/'frontend.json'; r=harbor.read_json(first);r['contracts']={};first.write_text(json.dumps(r),encoding='utf-8')
            report=project.verify_deliveries(out/'manifest.json',receipts,artifacts)
            self.assertFalse(report['ready_for_integration_review'])



if __name__=='__main__':
    unittest.main()
