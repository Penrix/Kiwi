import sys
import tempfile
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from overlay import BaselineError, apply, plan, verify_kiwi, verify_chromium

class OverlayTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        root = Path(self.temp.name)
        self.kiwi, self.chromium = root / "kiwi", root / "chromium"
        for name in ("base", "chrome", "components", "content", "extensions",
                     "net", "remoting", "services", "third_party", "toolbox", "ui"):
            (self.kiwi / name).mkdir(parents=True)
        self.write(self.kiwi / "CHROMIUM_VERSION",
                   "CHROMIUM_MAJOR=105\nCHROMIUM_MINOR=0\nCHROMIUM_BUILD=5195\nCHROMIUM_PATCH=24\n")
        self.write(self.kiwi / "KIWI_VERSION", "MAJOR=105\nMINOR=0\nBUILD=5195\nPATCH=33\n")
        self.write(self.kiwi / "chrome/VERSION", "MAJOR=105\nMINOR=0\nBUILD=5195\nPATCH=24\n")
        self.write(self.kiwi / "extensions/extension.cc", "Kiwi content\n")
        self.write(self.chromium / "DEPS", "deps={}\n")
        self.write(self.chromium / "build/config/android/config.gni", "version=105\n")
        self.write(self.chromium / "chrome/VERSION", "MAJOR=105\nMINOR=0\nBUILD=5195\nPATCH=24\n")
        self.write(self.chromium / "extensions/extension.cc", "Chromium content\n")
        self.write(self.chromium / "extensions/untouched.cc", "keep\n")

    @staticmethod
    def write(path, content):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    def test_source_metadata(self):
        verify_kiwi(self.kiwi)
        verify_chromium(self.chromium)

    def test_dry_run_has_no_effect(self):
        self.assertGreater(len(plan(self.kiwi, self.chromium)), 0)
        self.assertEqual((self.chromium / "extensions/extension.cc").read_text(), "Chromium content\n")

    def test_apply_preserves_other_files(self):
        apply(plan(self.kiwi, self.chromium))
        self.assertEqual((self.chromium / "extensions/extension.cc").read_text(), "Kiwi content\n")
        self.assertEqual((self.chromium / "extensions/untouched.cc").read_text(), "keep\n")
        self.assertEqual(plan(self.kiwi, self.chromium), [])

    def test_refuse_different_chromium_version(self):
        self.write(self.chromium / "chrome/VERSION", "MAJOR=106\nMINOR=0\nBUILD=1\nPATCH=0\n")
        with self.assertRaises(BaselineError):
            plan(self.kiwi, self.chromium)

    def test_refuse_incomplete_source(self):
        (self.chromium / "DEPS").unlink()
        with self.assertRaises(BaselineError):
            plan(self.kiwi, self.chromium)

    def test_refuse_external_symlink(self):
        (self.kiwi / "net/link").symlink_to(self.chromium / "DEPS")
        with self.assertRaises(BaselineError):
            plan(self.kiwi, self.chromium)

if __name__ == "__main__":
    unittest.main()
