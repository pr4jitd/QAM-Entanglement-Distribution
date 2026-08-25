# Release Notes

## v0.1.1

Import-path hotfix and reproducibility diagnostics for the manuscript data
release.

- Added explicit validation that the core source files are present, including
  `source_code/src/mpsk_ghz_hashing.py`.
- Made packaged source-code drivers add `source_code/src` to `sys.path` before
  importing the core simulation modules.
- Added `scripts/check_environment.py`, a lightweight diagnostic for users who
  cannot run the package.
- Verified the clean zip package from a fresh extraction with
  `python -B scripts/validate_release.py`.

## v0.1.0

Initial manuscript data-release package containing curated data, figure-specific
CSV extraction scripts, source-code provenance, and reproducibility spot checks.
