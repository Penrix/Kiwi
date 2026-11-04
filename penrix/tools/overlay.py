#!/usr/bin/env python3
"""Copy the Kiwi Chromium 105 overlay onto a separate, complete Chromium 105 checkout.

Default is a dry run. --apply is required to write.
"""
from __future__ import annotations
import argparse
import filecmp
import shutil
import sys
from pathlib import Path

OVERLAY_DIRS = ("base", "chrome", "components", "content", "extensions", "net",
                "remoting", "services", "third_party", "toolbox", "ui")
CHROMIUM_BASE = (105, 0, 5195, 24)

class BaselineError(RuntimeError):
    pass

def read_version(path: Path, prefix: str = "") -> tuple[int, int, int, int]:
    if not path.is_file():
        raise BaselineError(f"Missing version file: {path}")
    found = {}
    keys = tuple(prefix + k for k in ("MAJOR", "MINOR", "BUILD", "PATCH"))
    for line in path.read_text(encoding="utf-8").splitlines():
        if "=" not in line or line.lstrip().startswith("#"):
            continue
        key, value = (s.strip() for s in line.split("=", 1))
        if key in keys:
            try:
                found[key] = int(value)
            except ValueError as ex:
                raise BaselineError(f"Invalid version field: {key} in {path}") from ex
    if any(k not in found for k in keys):
        raise BaselineError(f"Missing version fields in {path}")
    return tuple(found[k] for k in keys)

def verify_kiwi(kiwi: Path) -> None:
    expected = CHROMIUM_BASE
    if read_version(kiwi / "CHROMIUM_VERSION", "CHROMIUM_") != expected:
        raise BaselineError("Fork CHROMIUM_VERSION is not the pinned 105 baseline")
    if read_version(kiwi / "chrome/VERSION") != expected:
        raise BaselineError("Fork chrome/VERSION is not the pinned 105 baseline")
    kiwi_version = read_version(kiwi / "KIWI_VERSION")
    if kiwi_version[:3] != expected[:3]:
        raise BaselineError(f"Kiwi patch series does not match 105: {kiwi_version}")
    for name in OVERLAY_DIRS:
        if not (kiwi / name).is_dir():
            raise BaselineError(f"Overlay directory absent: {name}")

def verify_chromium(chromium: Path) -> None:
    for name in ("DEPS", "build/config/android/config.gni", "chrome/VERSION"):
        if not (chromium / name).is_file():
            raise BaselineError(f"Not a full Chromium checkout: missing {name}")
    actual = read_version(chromium / "chrome/VERSION")
    if actual != CHROMIUM_BASE:
        raise BaselineError(f"Full Chromium version mismatch: {actual} != {CHROMIUM_BASE}")

def plan(kiwi: Path, chromium: Path) -> list[tuple[Path, Path]]:
    kiwi, chromium = kiwi.resolve(), chromium.resolve()
    if kiwi == chromium or kiwi in chromium.parents or chromium in kiwi.parents:
        raise BaselineError("Kiwi and full Chromium source must be separate directories")
    verify_kiwi(kiwi)
    verify_chromium(chromium)
    changes = []
    for name in OVERLAY_DIRS:
        for path in (kiwi / name).rglob("*"):
            if path.is_symlink():
                raise BaselineError(f"Refusing to copy symlink from overlay: {path}")
            if not path.is_file():
                continue
            relative = path.relative_to(kiwi)
            target = chromium / relative
            # A symlink in an ancestor directory could otherwise escape this tree.
            parent = chromium
            for component in relative.parts[:-1]:
                parent = parent / component
                if parent.is_symlink():
                    raise BaselineError(f"Refusing Chromium symlink directory: {parent}")
            if target.is_symlink() or (target.exists() and not target.is_file()):
                raise BaselineError(f"Refusing nonregular Chromium target: {target}")
            if not target.exists() or not filecmp.cmp(path, target, shallow=False):
                changes.append((path, target))
    return changes

def apply(changes: list[tuple[Path, Path]]) -> None:
    for source, target in changes:
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--kiwi-source", type=Path, default=Path.cwd())
    parser.add_argument("--chromium-src", type=Path)
    parser.add_argument("--source-only", action="store_true")
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    try:
        verify_kiwi(args.kiwi_source.resolve())
        if args.source_only:
            if args.apply:
                parser.error("--source-only cannot be combined with --apply")
            print("PASS: Kiwi pinned Chromium 105 metadata / overlay directories")
            return 0
        if args.chromium_src is None:
            parser.error("--chromium-src required without --source-only")
        changes = plan(args.kiwi_source, args.chromium_src)
        print(f"{'APPLY' if args.apply else 'DRY RUN'}: {len(changes)} new or changed files")
        for original, _ in changes[:12]:
            print(" ", original.relative_to(args.kiwi_source.resolve()))
        if len(changes) > 12:
            print(" ... additional:", len(changes) - 12)
        if args.apply:
            apply(changes)
            print("Copied to isolated Chromium tree; no other Chromium files deleted")
        else:
            print("Nothing written. Pass --apply to copy.")
        return 0
    except BaselineError as ex:
        print(f"ERROR: {ex}", file=sys.stderr)
        return 2

if __name__ == "__main__":
    raise SystemExit(main())
