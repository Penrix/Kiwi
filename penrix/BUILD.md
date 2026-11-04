# Independent Kiwi Chromium 105 build

This fork does **not** contain the final 137 browser source as a reproducible Chromium checkout. The public source snapshot is pinned to 105.0.5195.24. Neither the original private Kiwi build server nor its signing keys are available.

## Requirements

A fresh Linux build workspace, Git, depot_tools/gclient, Python 3, `gn` and `autoninja`; Chromium builds may require 100+ GB free disk and significant RAM. Historical Chromium toolchain dependencies may need repairs. **Do not use the old Penrix-Browser working directory.**

## Bootstrap

```bash
# Run on an adequately provisioned Linux build host:
bash penrix/build/bootstrap_chromium_105.sh /absolute/path/to/NEW-empty-chromium-workspace
```

The command downloads Chromium **105.0.5195.24** and its dependencies into a fresh workspace. It refuses an existing non-empty path.

## Dry run / source overlay

```bash
python3 penrix/tools/overlay.py --kiwi-source . \
  --chromium-src /absolute/path/to/new-chromium-workspace/src
```

That previews changes without modifying Chromium. Then independently attempt the APK:

```bash
bash penrix/build/build_android9.sh . /absolute/path/to/new-chromium-workspace/src
```

It applies the Kiwi overlay, runs hooks, generates GN configuration, and invokes `autoninja -C out/PenrixAndroid9 chrome_public_apk`.

Output package is configured to `app.penrix.browser.kiwi` (not the existing `app.penrix.browser` or official `com.kiwibrowser.browser`). This is unverified until inspecting the generated manifest.

A first full build can fail due to historical Chromium toolchains or missing build-time inputs. Capture the compiler errors and repair the fixed baseline, **not** by silently switching to latest Chromium. Do not call a failed/untested build complete.

## Offline checks

```bash
python3 penrix/tools/overlay.py --kiwi-source . --source-only
python3 -m unittest discover -s penrix/tests -v
bash -n penrix/build/bootstrap_chromium_105.sh penrix/build/build_android9.sh
```
