"""Language follows the request through recommendations and portable handoffs."""
import copy
import importlib.util
import json
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
import project

NOW = date(2026, 9, 30)
HAS_CHINESE = re.compile(r'[\u3400-\u9fff]')


class LanguageTests(unittest.TestCase):
    def setUp(self):
        self.data = harbor.load_data()
        self.sample = ROOT / 'examples/library-system/project.json'
        self.project = harbor.read_json(self.sample)

    def english_project(self):
        value = copy.deepcopy(self.project)
        value['goal'] = 'Build a local library catalog with book reviews.'
        value.pop('language', None)
        value['constraints'].pop('language', None)
        for task in value['tasks']:
            task['title'] = task['id'] + ' implementation'
            task['objective'] = 'Implement the assigned files against the frozen API contract.'
            task['acceptance'] = ['Run the relevant checks and return their actual results.']
            task.pop('assignment_reason', None)
            task.pop('recommended_model', None)
            task['job'].pop('language', None)
        value['integration']['checks'] = ['Assemble returned files and run integration checks.']
        return value

    def compile(self, root, value, **kwargs):
        # An absolute input contract path is intentionally not needed: copy the
        # contract unchanged next to the temporary project, as a user would.
        path = root / 'project.json'
        for contract in value['contracts']:
            original = self.sample.parent / contract['path']
            target = root / contract['path']
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(original.read_bytes())
        path.write_text(json.dumps(value, ensure_ascii=False), encoding='utf-8')
        output = root / 'handoffs'
        manifest = project.compile_project(path, output, NOW, **kwargs)
        return output, manifest

    def cli(self, script, *args):
        return subprocess.run(
            [sys.executable, '-X', 'utf8', str(script), *map(str, args)],
            capture_output=True, text=True, encoding='utf-8',
            env={**os.environ, 'PYTHONIOENCODING': 'utf-8'},
        )

    def test_chinese_project_auto_localizes_entire_handoff(self):
        self.project['tasks'][0]['job']['language'] = 'en'
        with tempfile.TemporaryDirectory() as directory:
            output, manifest = self.compile(Path(directory), self.project)
            self.assertEqual(manifest['language'], 'zh-CN')
            plan = (output / 'PLAN.md').read_text(encoding='utf-8')
            self.assertNotIn('# Project handoffs', plan)
            self.assertNotIn('## Main-window integration', plan)
            self.assertRegex(plan, r'主窗口|当前对话')
            self.assertRegex(plan, r'集成|整合')
            self.assertRegex(plan, r'依赖')
            for assignment in manifest['assignments']:
                with self.subTest(task=assignment['task_id']):
                    self.assertRegex(assignment['reason'], HAS_CHINESE)
                    prompt = (output / assignment['prompt']).read_text(encoding='utf-8')
                    self.assertNotIn('## Your bounded assignment', prompt)
                    self.assertRegex(prompt, r'用中文|使用中文|以中文|中文(?:回复|回答|说明|输出)')
                    self.assertRegex(prompt, r'交付|返回')
                    self.assertRegex(prompt, r'验收|检查')
                    evidence = harbor.read_json(output / 'prompts' / (assignment['task_id'] + '.evidence.json'))
                    self.assertEqual(evidence['language'], 'zh-CN')
                    for recommendation in assignment['recommendations']:
                        self.assertRegex(recommendation['reason'], HAS_CHINESE)
                    for dependency in assignment['depends_on']:
                        self.assertIn(dependency, prompt)
                    for deliverable in assignment['deliverables']:
                        self.assertIn(deliverable, prompt)
            # Contracts, keys and machine values are not translated.
            for frozen in manifest['contracts']:
                original = self.sample.parent / self.project['contracts'][0]['path']
                self.assertEqual((output / frozen['path']).read_bytes(), original.read_bytes())
            backend = (output / 'prompts/backend.md').read_text(encoding='utf-8')
            self.assertIn('BOOK_NOT_FOUND', backend)
            self.assertIn('"status": "complete"', backend)
            self.assertIn('"model_used"', backend)

    def test_task_title_can_select_chinese_when_goal_is_english(self):
        value = self.english_project()
        value['tasks'][0]['title'] = '前端实现'
        with tempfile.TemporaryDirectory() as directory:
            output, manifest = self.compile(Path(directory), value)
            self.assertEqual(manifest['language'], 'zh-CN')
            for assignment in manifest['assignments']:
                evidence = harbor.read_json(output / 'prompts' / (assignment['task_id'] + '.evidence.json'))
                self.assertEqual(evidence['language'], 'zh-CN')

    def test_explicit_english_overrides_chinese_and_task_language(self):
        self.project['language'] = 'en'
        self.project['constraints']['language'] = 'zh-CN'
        self.project['tasks'][0]['job']['language'] = 'zh-CN'
        with tempfile.TemporaryDirectory() as directory:
            output, manifest = self.compile(Path(directory), self.project)
            self.assertEqual(manifest['language'], 'en')
            plan = (output / 'PLAN.md').read_text(encoding='utf-8')
            self.assertIn('# Project handoffs', plan)
            self.assertIn('## Main-window integration', plan)
            for assignment in manifest['assignments']:
                evidence = harbor.read_json(output / 'prompts' / (assignment['task_id'] + '.evidence.json'))
                self.assertEqual(evidence['language'], 'en')

    def test_english_project_stays_english_without_language_setting(self):
        with tempfile.TemporaryDirectory() as directory:
            output, manifest = self.compile(Path(directory), self.english_project())
            self.assertEqual(manifest['language'], 'en')
            self.assertIn('# Project handoffs', (output / 'PLAN.md').read_text(encoding='utf-8'))
            for assignment in manifest['assignments']:
                self.assertNotRegex(assignment['reason'], HAS_CHINESE)

    def test_constraints_language_is_used_without_project_override(self):
        value = self.english_project()
        value['constraints']['language'] = 'zh'
        with tempfile.TemporaryDirectory() as directory:
            _, manifest = self.compile(Path(directory), value)
            self.assertEqual(manifest['language'], 'zh-CN')

    def test_chinese_single_question_localizes_reasons_and_validation(self):
        job = {'prompt': '帮我为现有代码仓库设计测试',
               'tasks': ['software.testing'], 'classification_method': 'host_semantic',
               'available_models': ['gpt-6-sol']}
        result = harbor.route(job, self.data, NOW)
        self.assertEqual(result['language'], 'zh-CN')
        self.assertTrue(result['recommendations'])
        for recommendation in result['recommendations']:
            self.assertRegex(recommendation['reason'], HAS_CHINESE)
        self.assertRegex(result['switch']['reason'], HAS_CHINESE)
        self.assertTrue(result['warnings'])
        self.assertTrue(all(HAS_CHINESE.search(text) for text in result['warnings']))
        self.assertTrue(result['validation'])
        self.assertTrue(all(HAS_CHINESE.search(text) for text in result['validation']))
        for classification in result['classification']:
            self.assertRegex(classification['label'], HAS_CHINESE)
        rendered = harbor.markdown(result)
        self.assertNotIn('**Switch:**', rendered)

    def test_language_only_changes_presentation_not_ranking(self):
        job = {'tasks': ['software.frontend'], 'prompt': '制作一个图书列表网页',
               'available_models': ['gpt-6-sol', 'kimi-k3', 'deepseek-v4.1-flash']}
        chinese = harbor.route({**job, 'language': 'zh-CN'}, self.data, NOW)
        english = harbor.route({**job, 'language': 'en'}, self.data, NOW)
        self.assertEqual(chinese['language'], 'zh-CN')
        self.assertEqual(english['language'], 'en')
        self.assertEqual(chinese['primary'], english['primary'])
        self.assertEqual(chinese['decision'], english['decision'])
        self.assertEqual([r['model_id'] for r in chinese['recommendations']],
                         [r['model_id'] for r in english['recommendations']])
        self.assertEqual([r['ranking'] for r in chinese['candidates']],
                         [r['ranking'] for r in english['candidates']])
        self.assertEqual(chinese['sources'], english['sources'])
        # Real community explanations and model notes follow the same language
        # as the template; untranslated source records remain attributable.
        rendered = harbor.markdown(chinese, self.data)
        community_count = 0
        for candidate in chinese['recommendations']:
            for note in candidate['limitations']:
                self.assertRegex(note, HAS_CHINESE)
                self.assertIn(note, rendered)
            for evidence in candidate['evidence']:
                if evidence['kind'] != 'community_test':
                    continue
                community_count += 1
                localized = self.data['locale_zh']['evidence'][evidence['id']]
                for field in ('claim', 'setting', 'limitations', 'rating_rationale'):
                    self.assertRegex(localized[field], HAS_CHINESE)
                    self.assertIn(localized[field], rendered)
                self.assertNotIn(evidence['claim'], rendered)
                source = chinese['sources'][evidence['source_id']]
                self.assertIn(source['url'], rendered)
        self.assertGreater(community_count, 0)

    def test_route_cli_language_overrides_job(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'job.json'
            path.write_text(json.dumps({'tasks': ['software.repo'], 'prompt': '修复仓库',
                                        'language': 'zh-CN'}, ensure_ascii=False), encoding='utf-8')
            response = self.cli(ROOT / 'skills/promptharbor/scripts/harbor.py', 'recommend',
                                '--job', path, '--language', 'en', '--format', 'json', '--as-of', NOW)
            self.assertEqual(response.returncode, 0, response.stderr)
            result = json.loads(response.stdout)
            self.assertEqual(result['language'], 'en')
            self.assertNotRegex(result['switch']['reason'], HAS_CHINESE)

    def test_compile_cli_language_overrides_project(self):
        value = self.english_project()
        value['language'] = 'en'
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            # Create valid portable input using the same contract-copy helper.
            self.compile(root, value)
            response = self.cli(ROOT / 'skills/promptharbor/scripts/project.py', 'compile',
                                '--project', root / 'project.json', '--out', root / 'chinese',
                                '--language', 'zh-CN', '--as-of', NOW)
            self.assertEqual(response.returncode, 0, response.stderr)
            self.assertEqual(json.loads(response.stdout)['language'], 'zh-CN')
            self.assertRegex((root / 'chinese/PLAN.md').read_text(encoding='utf-8'), HAS_CHINESE)

    def test_standalone_archive_keeps_language_support(self):
        spec = importlib.util.spec_from_file_location('language_packager', ROOT / 'scripts/package_skill.py')
        package = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(package)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            archive = root / 'skill.zip'
            package.package(archive)
            with zipfile.ZipFile(archive) as zipped:
                self.assertIn('promptharbor/scripts/i18n.py', zipped.namelist())
                self.assertIn('promptharbor/data/locales/zh-CN.json', zipped.namelist())
                zipped.extractall(root / 'unpacked')
            response = self.cli(root / 'unpacked/promptharbor/scripts/harbor.py', 'recommend',
                                '--prompt', '帮我设计网页界面', '--language', 'zh-CN', '--as-of', NOW)
            self.assertEqual(response.returncode, 0, response.stderr)
            self.assertNotIn('**Switch:**', response.stdout)
            self.assertRegex(response.stdout, HAS_CHINESE)


if __name__ == '__main__':
    unittest.main()
