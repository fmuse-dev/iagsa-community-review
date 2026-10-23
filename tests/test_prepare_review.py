import hashlib
import importlib.util
from pathlib import Path
import stat
import subprocess
import sys
import tempfile
import unittest
import warnings
import zipfile

SCRIPT = Path(__file__).resolve().parents[1] / 'tools/prepare_review.py'
spec = importlib.util.spec_from_file_location('prepare_review', SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class PreparationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.archive = self.root / 'input.zip'
        self.output = self.root / 'output'

    def make_archive(self, entries):
        with warnings.catch_warnings():
            warnings.simplefilter('ignore', UserWarning)
            with zipfile.ZipFile(self.archive, 'w') as archive:
                for name, content in entries:
                    archive.writestr(name, content)

    def prepare(self, digest=None, length=None):
        data = self.archive.read_bytes()
        return module.prepare(self.archive, self.output,
                              digest or hashlib.sha256(data).hexdigest(),
                              len(data) if length is None else length)

    def test_extracts_valid_contents_without_executing_them(self):
        self.make_archive([('release/run.py', 'raise RuntimeError("must not execute")')])
        self.prepare()
        self.assertTrue((self.output / 'release/run.py').is_file())

    def test_rejects_digest_mismatch(self):
        self.make_archive([('ok', 'data')])
        with self.assertRaisesRegex(ValueError, 'SHA-256'):
            self.prepare(digest='0' * 64)
        self.assertFalse(self.output.exists())

    def test_rejects_length_mismatch(self):
        self.make_archive([('ok', 'data')])
        with self.assertRaisesRegex(ValueError, 'length'):
            self.prepare(length=1)

    def test_rejects_traversal_and_ambiguous_paths(self):
        for name in ['../escape', '/absolute', 'C:/drive', 'a\\b', 'a//b', './x']:
            with self.subTest(name=name):
                self.make_archive([(name, 'bad')])
                with self.assertRaisesRegex(ValueError, 'path'):
                    self.prepare()
                self.assertFalse(self.output.exists())

    def test_rejects_duplicate_members(self):
        self.make_archive([('same', 'one'), ('same', 'two')])
        with self.assertRaisesRegex(ValueError, 'Duplicate'):
            self.prepare()

    def test_rejects_symlinks(self):
        info = zipfile.ZipInfo('link')
        info.create_system = 3
        info.external_attr = (stat.S_IFLNK | 0o777) << 16
        self.make_archive([(info, '/tmp/target')])
        with self.assertRaisesRegex(ValueError, 'Special'):
            self.prepare()

    def test_rejects_file_directory_collisions(self):
        self.make_archive([('file', 'data'), ('file/child', 'data')])
        with self.assertRaisesRegex(ValueError, 'collision'):
            self.prepare()

    def test_refuses_existing_output_without_modifying_it(self):
        self.make_archive([('ok', 'data')])
        self.output.mkdir()
        marker = self.output / 'keep'
        marker.write_text('unchanged')
        with self.assertRaisesRegex(ValueError, 'already exist'):
            self.prepare()
        self.assertEqual(marker.read_text(), 'unchanged')

    def test_rejects_oversized_expansion(self):
        self.make_archive([('ok', 'data')])
        old = module.MAX_EXPANDED
        try:
            module.MAX_EXPANDED = 1
            with self.assertRaisesRegex(ValueError, 'expands'):
                self.prepare()
        finally:
            module.MAX_EXPANDED = old

    def test_refuses_optimized_python(self):
        for flag in ['-O', '-OO']:
            result = subprocess.run([sys.executable, flag, str(SCRIPT), '--help'],
                                    capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('Optimized Python', result.stderr)


if __name__ == '__main__':
    unittest.main()
