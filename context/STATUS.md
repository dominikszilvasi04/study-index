# Current Status

Last updated: 22 September 2026

## Repository

- Local path: `C:\Users\Dominik\Desktop\study-index`
- Remote: `https://github.com/dominikszilvasi04/study-index`
- Branch: `main`
- Local `main` is at `6cb9dce fix some linting errors, add utility methods for modules package, add minimal test`, one commit ahead of remote `main`.
- The working tree adds comprehensive automated tests and coverage enforcement.
- The `context/` directory is tracked by Git so project reasoning and continuity are shared with contributors.

## Application

- The Conda environment was created successfully.
- A root `app.py` contains the first PySide6 application shell and launches successfully.
- `StudyIndexWindow` is separated into `study_index/main_window.py`.
- Shared module models, persistence and the module-list page live directly under `study_index/modules/`.
- Module-workspace code is grouped under `study_index/modules/workspace/`, with separate page, linked-folder panel, module files table and file finder responsibilities.
- `ModuleDatabase` provides clearly named module and linked-folder operations backed by SQLite.
- Opening a module displays its workspace through the main window's stacked pages.
- Linked-folder records are managed by `ModuleDatabase` to keep the initial workflow small.
- A module workspace can add an existing folder through the native picker, list persisted folder references and remove a reference without changing the folder.
- Linked folders are searched read-only and their file metadata is displayed through a dedicated module files table.
- Reusable file-size and timestamp formatting lives in `study_index/formatters.py`.
- The initial application entry point will be the root file `app.py`.
- The planned run command is `python app.py`.
- The initial Conda environment includes Python 3.12, PySide6, PyInstaller, pytest, pytest-cov, pytest-qt and Flake8.
- The test suite contains 26 tests covering persistence, file discovery, formatting, configuration, widgets, navigation and application composition.
- Running Pytest enforces 100% line coverage over `study_index` and `app.py`.
- GitHub Actions runs lint and the complete test suite for every push and pull request, then builds, smoke-tests and uploads native Windows and macOS bundles.
- Conda is not on the shell `PATH`, but its executable at `C:\Users\Dominik\anaconda3\Scripts\conda.exe` can run project checks.
- The environment's direct Python executable at `C:\Users\Dominik\anaconda3\envs\study_index\python.exe` can run Pytest and Flake8 without relying on `conda run`.
- The owner's installed Conda requires `conda env create` to parse `environment.yml`; plain `conda create --file` treated it as a package specification.

## Immediate Next Step

- Folder scan errors are displayed without preventing other linked folders from loading, and Locate Folder reconnects moved roots.
- Files and linked folders support activation and context menus. Shared opening and clipboard behaviour lives in `study_index/path_actions.py`; widgets retain their own menu and selection logic.
- Flake8 and all 26 existing tests pass with coverage disabled after these changes. New interactions have not yet been covered by automated tests; the 100% coverage gate has not been verified for this work.
- Filename search and a fixed file-type dropdown filter together: All file types, PDF, Word (.doc/.docx), PowerPoint (.ppt/.pptx), and Text (.txt). Refresh leaves the selection unchanged. Other types and files without extensions remain visible under All file types. Dynamic type discovery and dropdown rebuilding were removed at the owner's request for simpler code.
- Filtering uses named filename/type column constants and descriptive intermediate variables for readability.
- Column sorting is enabled, initially by filename. A small FileTableItem comparison uses raw sizes/timestamps and case-insensitive text. Three sorting cases check ascending and descending order, including dates with identical displayed minutes. Flake8 and 29 tests pass with coverage disabled.
- Next: manually verify sorting alongside filtering and refresh, then continue with module codes, terms and archiving. Background scanning and persisted file indexes are deferred at the owner's request.
