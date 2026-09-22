# Current Status

Last updated: 22 September 2026

## Repository

- Local path: `C:\Users\domin\Desktop\StudyIndex`
- Remote: `https://github.com/dominikszilvasi04/study-index`
- Branch: `main`
- Local and remote `main` are at `41a4a99 update project context`.
- The working tree contains the in-progress resource scanning and workspace reorganisation.
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
- The initial Conda environment includes Python 3.12, PySide6, PyInstaller, pytest, pytest-qt and Flake8.
- Conda is not on the shell `PATH`, but its executable at `C:\Users\domin\anaconda3\Scripts\conda.exe` can run project checks.
- The environment's direct Python executable at `C:\Users\domin\anaconda3\envs\study_index\python.exe` can run Pytest and Flake8 without relying on `conda run`.
- The owner's installed Conda requires `conda env create` to parse `environment.yml`; plain `conda create --file` treated it as a package specification.

## Immediate Next Step

Manually verify the resource list with empty, populated and unavailable linked folders before adding scanner tests.
