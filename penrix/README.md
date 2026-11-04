# Penrix Kiwi — Android 9 desktop Chrome extensions

**Decision dated 2026-11-04:** target Redmi K20 Pro (Android 9/API 28); use Kiwi as a Chromium-based private browser supporting Chrome desktop extensions, including legacy Manifest V2 and network-blocking APIs. Do not pursue newer Chromium merely for version numbers.

## Source audit (verified)

* Upstream: https://github.com/kiwibrowser/src.next; actual fork: **https://github.com/Penrix/Kiwi** (default branch `kiwi`).
* Public tracked `CHROMIUM_VERSION` and `chrome/VERSION` both read **105.0.5195.24**; `KIWI_VERSION` reads **105.0.5195.33**.
* **Critical mismatch:** final official upstream GitHub Release `14310011181` advertises **137.0.7337.0**, but its source tag still contains version files for 105. The official APK cannot be assumed to be reproducible from the public checked-in snapshot.
* Upstream workflows use inaccessible private services, including `longbuild.find.kiwi`, `BUILD_KEY`, `STORAGE_HOST` and `STORAGE_KEY`; these are not valid independent build paths for our fork. This branch disables the two inherited private-server APK workflows.
* The public repository is a partial Chromium overlay; it lacks a full Chromium `DEPS` and `build/` tree. A separate pinned full-source Chromium checkout is necessary.

## Implemented engineering groundwork

* `penrix/tools/overlay.py`: dry-run-first Kiwi overlay staging into a **separate** full Chromium 105 tree; refuses version drift and unsafe symlinks.
* `penrix/tests/test_overlay.py`: baseline, dry-run, copy, preservation and failure-case tests.
* `penrix/build/bootstrap_chromium_105.sh`: prepare a fresh full Chromium source checkout with the pinned tag.
* `penrix/build/build_android9.sh`: independently attempt the ARM64 `chrome_public_apk` build.
* `penrix/build/args.android9.gn`: separate Android package `app.penrix.browser.kiwi`; extensions enabled.
* `.github/workflows/penrix-source-check.yml`: static tests on PR and branch.
* `.github/workflows/penrix-android9-build.yml`: optional manual full build for a capable self-hosted Linux runner.

**These are preparatory engineering changes.** No new APK or K20 extension acceptance has yet been obtained. See [BUILD.md](BUILD.md) and [ACCEPTANCE.md](ACCEPTANCE.md).

## Preserve the old Penrix project

The prior [Penrix-Browser](https://github.com/Penrix/Penrix-Browser) WebView project includes Reader, bookshelf, blocking and Epic automation work. The Windows working copy was reported with many uncommitted and untracked files in https://github.com/Penrix/android-automation-node/issues/3. **Do not reset, overwrite, or discard them.** Migrate components only into a separate Kiwi worktree after build/runtime validation.

## Expected product progression

```text
Official Kiwi APK / Android 9 baseline test
  -> Full MV2 uBlock Origin and scripts actually execute
  -> Independent Chromium 105 overlay APK builds
  -> Independent APK survives real device extension tests
  -> Port old Penrix Reader, shelf, blocking and Epic integrations
  -> Verify all flows and preserve rollback
```
