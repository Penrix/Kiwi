#!/usr/bin/env bash
set -euo pipefail
if [[ $# -ne 2 ]]; then
  echo "Usage: bash build_android9.sh /path/to/Penrix-Kiwi /path/to/Chromium-105/src" >&2
  exit 2
fi
kiwi="$(cd "$1" && pwd)"
chromium="$(cd "$2" && pwd)"
# A bootstrap-installed depot_tools PATH does not survive across GitHub Actions steps.
if [[ -d "$(dirname "$chromium")/depot_tools" ]]; then
  export PATH="$(dirname "$chromium")/depot_tools:$PATH"
fi
for tool in python3 gclient gn autoninja; do
  command -v "$tool" >/dev/null || { echo "Missing prerequisite: $tool" >&2; exit 2; }
done
python3 "$kiwi/penrix/tools/overlay.py" --kiwi-source "$kiwi" --chromium-src "$chromium"
python3 "$kiwi/penrix/tools/overlay.py" --kiwi-source "$kiwi" --chromium-src "$chromium" --apply
cd "$chromium"
gclient runhooks
mkdir -p out/PenrixAndroid9
cp "$kiwi/penrix/build/args.android9.gn" out/PenrixAndroid9/args.gn
gn gen out/PenrixAndroid9
autoninja -C out/PenrixAndroid9 chrome_public_apk
echo "Build succeeded. Locate APK artifacts:"
find out/PenrixAndroid9/apks -maxdepth 2 -type f -name '*.apk' -print 2>/dev/null || true
echo "Inspect APK minSdk and package; test real MV2 extensions on K20 before acceptance."
