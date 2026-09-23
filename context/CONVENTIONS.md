# Conventions

## Language And Naming

- Use British English spelling in prose, documentation, comments, identifiers and commit messages where natural.
- Preserve names defined by Python, external APIs, file formats and libraries.
- Use descriptive, complete words for names, including loop variables.
- Avoid abbreviations unless they are established terms such as HTML, URL, API, ID or SQL.
- Do not use a leading underscore merely to suggest that a variable, function or method is private.
- Keep language-required names such as `__init__` unchanged.

## Python

- Avoid `*` and `**` in function signatures unless required by Python, a framework or a clear interface constraint.
- Prefer explicit parameters.
- Do not use an automatic code formatter.
- Do not use Ruff.
- Use Flake8 only for high-signal correctness checks: serious parsing errors (`E9`), Pyflakes findings (`F`) and a missing final newline (`W292`). Do not use it to enforce blank lines, line length or other layout preferences. The tracked `.flake8` file defines this selection.
- Format code in PyCharm style.
- When a function declaration or call wraps, keep the first argument after the opening parenthesis and visually align later arguments beneath it. For example:

```python
module_name, accepted = QInputDialog.getText(self,
                                             "Add module",
                                             "Module name:")
```

- Keep declarations and calls on one line while they remain readable. Wrap only when the line becomes too long.
- Keep short function bodies continuous. Do not add blank lines merely to separate setup, action and assertion; use them only when a longer function has genuinely distinct sections.

## Implementation

- Prefer the simplest implementation that fully solves the current problem.
- Avoid speculative abstractions, unnecessary dependencies and boilerplate.
- Optimise for readable top-to-bottom flow.
- Prefer two clear lines over one compressed line when that improves readability.
- Use descriptive intermediate variables and named column constants so table code explains which data it reads. Prefer straightforward conditions over compact expressions when teaching or extending the UI.
- Fail loudly. Do not swallow exceptions, hide invalid state or add silent fallbacks unless explicitly required.
- Apply Ponytail's minimal-code approach to source code and code structure only.

## Context Documents

- Ponytail does not limit the detail in this directory.
- Context documents are written for future agents, not as public-facing prose.
- Preserve reasoning, constraints and unresolved questions where they will affect later work.
- Keep each fact in the most relevant file and avoid unnecessary duplication.
