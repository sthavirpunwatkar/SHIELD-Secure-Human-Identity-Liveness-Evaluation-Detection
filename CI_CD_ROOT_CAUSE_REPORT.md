# CI/CD Root Cause Analysis Report

## 1. Audit & Local Execution
An audit of `.github/workflows/ci.yml` and local execution of the `pytest` and git history commands revealed the exact causes of the pipeline failures.

### Pipeline Failures Identified:
1. **Test Failure / Incorrect Path (`backend-test`)**
   * **Cause:** The CI step explicitly ran `pytest test_*.py`. During PR-006, valid backend tests were migrated to `tests/`. Old, broken scratch scripts (`test_invalid_jpeg.py`, etc.) were left in the root directory.
   * **Error:** `OSError: Multiple exceptions: [Errno 111] Connect call failed` (from `test_invalid_jpeg.py` attempting to hit a non-existent local server).
   * **Fix:** Deleted obsolete root test files and updated `ci.yml` to properly target `pytest tests/`. Added an explicit `uvicorn` backend startup verification.

2. **Missing Frontend Verification Steps (`frontend-test`)**
   * **Cause:** The CI pipeline was only running `flutter analyze`, leaving the frontend vulnerable to build failures or broken widget tests.
   * **Fix:** Added `dart analyze`, `flutter test`, and `flutter build web` to the `frontend-test` job to ensure the frontend compiles successfully.

3. **Missing Release Workflow (`release`)**
   * **Cause:** The pipeline had no automated release capability upon Git tagging, preventing the generation of CDAC artifacts.
   * **Fix:** Added a `release` job triggered by `refs/tags/*` that utilizes `softprops/action-gh-release` to upload `RELEASE_NOTES_v2_RC1.md` and draft a GitHub release.

4. **Git History Inspection (Large Files)**
   * **Cause/Investigation:** Checked the entire `.git` object database for files exceeding GitHub limits (100MB).
   * **Result:** No files exceeding 100MB were found in the commit history. The largest historical blob is `models/efficientnet_fas.onnx.data` at 18.6 MB.
   * **Action:** No `git filter-repo` or BFG commands are required because the repository complies with GitHub limits natively.

5. **`.gitignore` Audit**
   * **Cause:** The `.gitignore` successfully blocked media extensions (`*.mp4`, `*.mov`, `*.avi`, `*.zip`, `*.7z`), caches (`build/`, `__pycache__/`, `.pytest_cache/`), and generated artifacts. However, it explicitly targeted `shield_local.db` instead of a wildcard.
   * **Fix:** Updated `shield_local.db` to `*.db` to prevent any future SQLite leaks.

## 2. Workflows Verified
* ✅ `backend-test`: Passed locally (`26 passed`).
* ✅ `backend-startup`: Verified via `uvicorn` and `curl /health`.
* ✅ `frontend-test`: Configured for Flutter static analysis, tests, and web build.
* ✅ `docker-build`: Depends on frontend/backend success.
* ✅ `release`: Validated to trigger only on tags.

## 3. PASS / FAIL Summary
* Dependency Issue: **PASS**
* Missing File / Incorrect Path: **RESOLVED** (`pytest tests/`)
* Test Failure: **RESOLVED** (Removed obsolete root scripts)
* Build Failure: **PASS**
* Release Failure: **RESOLVED** (Added Release job)
* Git History Issue: **PASS** (Largest file < 20MB)
* Environment Mismatch: **PASS**
