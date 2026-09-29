import importlib.util
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]


def module(name):
    spec=importlib.util.spec_from_file_location('distribution_'+name,ROOT/'scripts'/f'{name}.py')
    mod=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class DistributionTests(unittest.TestCase):
    def test_installed_copy_runs_without_repository(self):
        with tempfile.TemporaryDirectory() as d:
            target=module('install').install(Path(d)/'skills')
            result=subprocess.run([sys.executable,str(target/'scripts/harbor.py'),'validate'],capture_output=True,text=True)
            self.assertEqual(result.returncode,0,result.stderr)
            for name in ('SKILL.md','LICENSE','NOTICE','THIRD_PARTY.md','assets/avatar.png','data/evidence.json'):
                self.assertTrue((target/name).is_file(),name)
            with self.assertRaises(FileExistsError):
                module('install').install(Path(d)/'skills')

    def test_archive_is_deterministic_and_standalone(self):
        with tempfile.TemporaryDirectory() as d:
            pack=module('package_skill');a=Path(d)/'a.zip';b=Path(d)/'b.zip'
            self.assertEqual(pack.package(a),pack.package(b))
            self.assertEqual(a.read_bytes(),b.read_bytes())
            with zipfile.ZipFile(a) as z:
                names=z.namelist()
                self.assertEqual(len(names),len(set(names)))
                self.assertIn('promptharbor/LICENSE',names)
                self.assertTrue(all(n.startswith('promptharbor/') for n in names))
                self.assertFalse(any('__pycache__' in n or n.endswith('.pyc') for n in names))
                z.extractall(Path(d)/'unpacked')
            result=subprocess.run([sys.executable,str(Path(d)/'unpacked/promptharbor/scripts/harbor.py'),'validate'],capture_output=True,text=True)
            self.assertEqual(result.returncode,0,result.stderr)


if __name__=='__main__':
    unittest.main()
