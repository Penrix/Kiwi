import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "extension-probes" / "mv2-android9"

class ManifestWiring(unittest.TestCase):
    def test_mv2_and_blocking_permissions(self):
        manifest = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["manifest_version"], 2)
        self.assertTrue({"webRequest", "webRequestBlocking", "storage"}.issubset(set(manifest["permissions"])))
        self.assertTrue(manifest["background"]["persistent"])
        self.assertIn("background.js", manifest["background"]["scripts"])
        self.assertIn("content.js", manifest["content_scripts"][0]["js"])
        self.assertEqual(manifest["browser_action"]["default_popup"], "popup.html")
        for path in ("background.js", "content.js", "popup.html", "popup.js"):
            self.assertTrue((ROOT / path).is_file())

if __name__ == "__main__":
    unittest.main()
