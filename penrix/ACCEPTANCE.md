# Redmi K20 Pro acceptance (Android 9 / API 28)

| Gate | Evidence required | Status |
| --- | --- | --- |
| 1. Official Kiwi | APK minSdk/package/version independently read; K20 installation and browsing | Not yet verified here |
| 2. MV2 network blocking | Full uBlock Origin installation, actual request blocked | Not verified |
| 3. User scripts | Tampermonkey or Violentmonkey real DOM injection / popup / restart persistence | Not verified |
| 4. Independent compile | Chromium 105 + public Kiwi overlay, independent arm64 APK without private Kiwi service | Not yet built |
| 5. App isolation | APK `app.penrix.browser.kiwi`, minSdk <= 28, no overwrite of original Penrix-Browser | Not verified |
| 6. Product migration | Reader, bookshelf/progress, site filtering, Epic automation individually pass | Not started |
| 7. Rollback | Existing Penrix-Browser user data and uncommitted Windows code intact | Must preserve |

**Provenance:** final Kiwi official 137.0.7337.0 APK and public fork snapshot Chromium 105.0.5195.24 are distinct; passing source/static tests does not prove an independent replica of the 137 APK.

Extension tests must verify `webRequestBlocking` (not simply install), content scripts, background scripts, permissions and extension popup. Android 9 operation is an on-device requirement, not an inference from a GitHub README.
