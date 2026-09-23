# Decisions

## Product

- The product name is StudyIndex.
- StudyIndex is a local-first desktop application for connecting college tasks, modules and existing files.
- Original academic files stay in their current folders. StudyIndex stores references and derived metadata.
- The application must remain useful without an account or internet connection.
- Use the Forest Paper visual direction: warm paper-like neutral surfaces with a restrained forest-green accent.
- Structure the module workspace as a clear module header above two task-focused panels: linked folders on the left and searchable files on the right. Keep actions beside the content they affect, with the back and refresh actions at page level.

## Python And Dependencies

- The Python package is named `study_index`.
- Dependencies are managed with Conda. Do not use pip.
- Define `environment.yml` before adding application code.
- Create the environment with `conda env create --file environment.yml --solver=libmamba`. This works with the installed Conda version, while its plain `conda create --file` command does not parse the YAML format correctly.
- Use PySide6 with Qt Widgets for the desktop interface.
- Use Python's built-in `sqlite3` initially. The earlier SQLAlchemy and Alembic proposal is superseded unless a concrete need appears.
- Use PyInstaller for distributable builds.
- Use Flake8 as a narrow correctness checker rather than a style checker. Select `E9`, `F` and `W292`; formatting remains a human decision guided by the project conventions.
- Do not use Ruff.
- Do not add Vulture yet. It detects unused code rather than general lint problems and becomes useful only when dead functions or classes are difficult to identify.

## Application Entry Point

- Use a root `app.py` as the application entry point.
- Run the application with `python app.py`.
- Point PyInstaller at `app.py`.
- Treat `app.py` as the composition root. It creates `QApplication`, creates the main window, shows it and starts the event loop.
- Keep `study_index/main_window.py` as the application shell. It registers top-level pages and window-wide components but does not implement feature-specific interfaces.
- Keep shared module models, persistence and the module-list page directly in `study_index/modules/`.
- Group the growing module-workspace feature under `study_index/modules/workspace/`, with separate files for the page, module files table and file finder.
- Keep reusable display formatting in `study_index/formatters.py` rather than embedding it in page classes or collecting unrelated helpers in a generic utilities module.
- Keep linked-folder persistence in `ModuleDatabase` while folders exist only as part of a module workflow.
- Use `StudyIndexWindow` to switch between the module list and a module workspace.
- Prefer explicit named component attributes such as `self.module_list_page` and `self.add_module_button` where they make the object structure easy to inspect.
- Create classes for cohesive pages or reusable components, not placeholder classes for individual labels, buttons or dependencies that have no behaviour yet.
- Keep `study_index/__init__.py` empty. It marks the application package but must not trigger startup or perform registration through import side effects.
- Do not create controller, service, repository or database modules until those responsibilities exist in working code.

## Delivery

- Follow Semantic Versioning.
- Build PyInstaller artefacts separately on each target operating system.
- Start with PyInstaller's directory-based output before considering a single-file build.
- GitHub Actions will eventually run checks and build releases.
- No software licence has been selected yet.
