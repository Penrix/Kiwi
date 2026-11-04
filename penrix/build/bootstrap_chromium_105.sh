#!/usr/bin/env bash
set -euo pipefail
if [[ $# -ne 1 || "$1" != /* ]]; then
  echo "Usage: bash bootstrap_chromium_105.sh /absolute/path/to/NEW-empty-workspace" >&2
  exit 2
fi
workspace="$1"
if [[ -e "$workspace" ]] && { [[ ! -d "$workspace" ]] || [[ -n "$(ls -A "$workspace")" ]]; }; then
  echo "Refusing existing non-empty workspace: $workspace" >&2
  exit 2
fi
for tool in git python3; do
  command -v "$tool" >/dev/null || { echo "Missing: $tool" >&2; exit 2; }
done
mkdir -p "$workspace"
if ! command -v gclient >/dev/null; then
  git clone --depth 1 https://chromium.googlesource.com/chromium/tools/depot_tools.git "$workspace/depot_tools"
  export PATH="$workspace/depot_tools:$PATH"
fi
cd "$workspace"
gclient config --name=src https://chromium.googlesource.com/chromium/src.git
git clone --depth=1 --branch 105.0.5195.24 https://chromium.googlesource.com/chromium/src.git src
gclient sync --nohooks --with_branch_heads --with_tags
actual="$(git -C src describe --tags --exact-match)"
if [[ "$actual" != "105.0.5195.24" ]]; then
  echo "Chromium source drift: expected 105.0.5195.24, got $actual" >&2
  exit 2
fi
echo "Pinned complete Chromium source at $workspace/src"
