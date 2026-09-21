# Current Status

Last updated: 21 September 2026

## Repository

- Local path: `C:\Users\domin\Desktop\StudyIndex`
- Remote: `https://github.com/dominikszilvasi04/study-index`
- Branch: `main`
- Current remote commit: `ff37b45 chore: initialise repository`
- Current local commit: `07bddfc set up window and adding module functionality`
- Local `main` is one commit ahead of `origin/main` and needs to be pushed.
- The latest local commit adds the first in-memory module interaction.
- The `context/` directory is tracked by Git so project reasoning and continuity are shared with contributors.

## Application

- The Conda environment was created successfully.
- A root `app.py` contains the first PySide6 application shell and launches successfully.
- `StudyIndexWindow` is separated into `study_index/main_window.py`.
- The module interface is separated into `study_index/modules_page.py`.
- The current source needs a final Flake8 formatting pass: top-level declarations need two blank lines and wrapped calls must use the agreed visual indentation.
- The initial application entry point will be the root file `app.py`.
- The planned run command is `python app.py`.
- The initial Conda environment includes Python 3.12, PySide6, PyInstaller, pytest, pytest-qt and Flake8.
- Conda is not available on the Codex shell `PATH`, so commands inside the environment cannot be tested from this session.
- The owner's installed Conda requires `conda env create` to parse `environment.yml`; plain `conda create --file` treated it as a package specification.

## Immediate Next Step

Clean and verify the committed in-memory module flow, amend the unpushed commit and push it. Then add SQLite persistence behind a small module repository injected from `app.py`, so module names survive an application restart without placing SQL in the Qt classes.
