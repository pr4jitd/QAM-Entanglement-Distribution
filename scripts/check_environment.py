#!/usr/bin/env python3
"""Check whether this release package can import its required dependencies.

Run from the release root:

    python scripts/check_environment.py

This script is intentionally lightweight.  It does not regenerate manuscript
data; it only checks Python, required packages, required source files, and core
imports.  If a user reports that the package cannot run, ask them to paste this
script's output together with the package version.
"""

from __future__ import annotations

import importlib
import os
import platform
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = ROOT / "source_code" / "src"
VERSION_FILE = ROOT / "VERSION"

os.environ.setdefault("MPLCONFIGDIR", str(ROOT / ".matplotlib"))
os.environ.setdefault("XDG_CACHE_HOME", str(ROOT / ".cache"))

REQUIRED_PACKAGES = [
    "numpy",
    "pandas",
    "scipy",
    "matplotlib",
    "openpyxl",
    "threadpoolctl",
]

REQUIRED_SOURCE_FILES = [
    "mpsk_ghz_hashing.py",
    "qam_hashing.py",
    "compare_schmidt_bell_povm_qam.py",
    "qam_source_loss_hashing.py",
    "qam_reflection_source_loss_hashing.py",
    "optimize_qam4_general_povm.py",
]

CORE_IMPORTS = [
    "mpsk_ghz_hashing",
    "qam_hashing",
    "compare_schmidt_bell_povm_qam",
    "qam_reflection_source_loss_hashing",
    "optimize_qam4_general_povm",
]


def check_import(name: str) -> tuple[bool, str]:
    try:
        module = importlib.import_module(name)
    except Exception as exc:  # pragma: no cover - diagnostic script
        return False, f"{type(exc).__name__}: {exc}"
    version = getattr(module, "__version__", "")
    suffix = f" {version}" if version else ""
    return True, f"ok{suffix}"


def main() -> int:
    version = VERSION_FILE.read_text(encoding="utf-8").strip() if VERSION_FILE.exists() else "unknown"
    print(f"Release version: {version}")
    print(f"Release root: {ROOT}")
    print(f"Python: {sys.version.split()[0]} ({platform.platform()})")
    print()

    ok = True

    print("Python packages:")
    for name in REQUIRED_PACKAGES:
        passed, detail = check_import(name)
        ok = ok and passed
        print(f"  [{'PASS' if passed else 'FAIL'}] {name}: {detail}")

    print()
    print("Core source files:")
    for name in REQUIRED_SOURCE_FILES:
        path = SOURCE_ROOT / name
        passed = path.exists()
        ok = ok and passed
        detail = str(path) if passed else f"missing: {path}"
        print(f"  [{'PASS' if passed else 'FAIL'}] {name}: {detail}")

    print()
    print("Core imports from source_code/src:")
    sys.path.insert(0, str(SOURCE_ROOT))
    for name in CORE_IMPORTS:
        passed, detail = check_import(name)
        ok = ok and passed
        if passed:
            module = sys.modules[name]
            module_path = Path(module.__file__).resolve()
            passed = module_path.is_relative_to(SOURCE_ROOT)
            ok = ok and passed
            detail = str(module_path)
        print(f"  [{'PASS' if passed else 'FAIL'}] {name}: {detail}")

    print()
    if ok:
        print("Environment check passed.")
        print("Next command: python scripts/validate_release.py")
        return 0

    print("Environment check failed.")
    print("Install dependencies with: python -m pip install -r requirements.txt")
    print("Then rerun this script from the release root.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
