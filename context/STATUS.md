# Current Status

Last updated: 21 September 2026

## Repository

- Local path: `C:\Users\Dominik\Desktop\study-index`
- Remote: `https://github.com/dominikszilvasi04/study-index`
- Branch: `main`
- Local and remote `main` are at `8499ab2 add full crud module functionality` before the current work.
- The working tree adds module workspaces and persistent linked folders.
- The `context/` directory is tracked by Git so project reasoning and continuity are shared with contributors.

## Application

- The Conda environment was created successfully.
- A root `app.py` contains the first PySide6 application shell and launches successfully.
- `StudyIndexWindow` is separated into `study_index/main_window.py`.
- Module models, persistence and interface code live in clearly named files under `study_index/modules/`.
- `ModuleDatabase` provides clearly named module and linked-folder operations backed by SQLite.
- Opening a module displays its workspace through the main window's stacked pages.
- Linked-folder records are managed by `ModuleDatabase` to keep the initial workflow small.
- A module workspace can add an existing folder through the native picker, list persisted folder references and remove a reference without changing the folder.
- The initial application entry point will be the root file `app.py`.
- The planned run command is `python app.py`.
- The initial Conda environment includes Python 3.12, PySide6, PyInstaller, pytest, pytest-qt and Flake8.
- Conda is not on the shell `PATH`, but its executable at `C:\Users\Dominik\anaconda3\Scripts\conda.exe` can run project checks.
- The owner's installed Conda requires `conda env create` to parse `environment.yml`; plain `conda create --file` treated it as a package specification.

## Immediate Next Step

Manually verify folder selection in the visible application, then add read-only metadata scanning for files beneath a linked folder without moving or modifying user files.
