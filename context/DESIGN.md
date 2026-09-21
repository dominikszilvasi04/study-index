# StudyIndex Design Document

Status: Discovery and architecture draft  
Intended first public version: 0.1.0  
Primary platform during early development: Windows  
Long-term platforms: Windows, macOS, and Linux  
Document purpose: Define the product before implementation and record the reasoning behind important decisions.

## 1. Product Summary

StudyIndex is a local-first desktop workspace for college work. It gives a student one place to see what needs attention, locate existing study material, and move between related resources without copying those resources into another service.

The application does not replace Moodle, a filesystem, a note editor, or a calendar. It connects those systems and makes the student's existing information easier to navigate.

The core promise is:

> Open StudyIndex and understand what to do, where the relevant material is, and what work is connected to it.

StudyIndex should remain useful without an internet connection, an account, or a hosted backend. A new user should be able to install it, link their existing college folders, and receive value quickly.

## 2. Problem Statement

A student's academic information is fragmented across several places:

- Deadlines and announcements live in Moodle or another learning platform.
- Notes and slides live in local folders, cloud-synced folders, or downloads.
- Past exam papers may be stored separately from module notes.
- Programming assignments may live in Git repositories.
- Personal tasks and study intentions may live in a notes application or nowhere at all.
- File names and folder structures are often inconsistent.

The resulting problem is not simply file storage. It is loss of context. A student may know that an exam is approaching but still need to search several directories to find the relevant lecture notes, past papers, and unfinished work.

StudyIndex should reduce this navigation cost while preserving the user's ownership of their files.

## 3. Product Principles

### 3.1 Local first

Core behavior must work offline. User data should remain on the device unless the user explicitly enables a future integration that communicates with an external service.

### 3.2 Reference, do not imprison

Academic files remain in their original folders. StudyIndex stores references, metadata, extracted search text, and relationships. It must not silently relocate or rename files.

### 3.3 Useful before intelligent

Reliable folder navigation, task tracking, and search matter more than speculative AI features. Related-content suggestions should begin with understandable rules and metadata.

### 3.4 One action should have one obvious home

The interface should avoid duplicate controls and ambiguous navigation. Adding a task, linking a folder, finding a resource, and opening a module should each have a predictable route.

### 3.5 Recoverable behavior

File scanning, migrations, imports, and settings changes should either succeed completely or fail without damaging existing state. Derived indexes must always be rebuildable.

### 3.6 Respect attention

StudyIndex should feel like a quiet work surface. It should not use engagement mechanics, unnecessary notifications, streak pressure, or decorative dashboards that do not help a decision.

### 3.7 Explain recommendations

When the app labels something as urgent or related, the user should be able to understand why.

### 3.8 Build cleanly in public

The repository should be approachable to contributors. Modules should have clear responsibilities, behavior should be tested at sensible boundaries, and release artifacts should be reproducible enough to diagnose.

## 4. Intended Users

### 4.1 Primary user

A college or university student who:

- works primarily from a personal laptop or desktop;
- stores material in ordinary folders;
- uses Moodle or a similar platform;
- wants less friction, not another system to maintain;
- values privacy and offline access;
- may be comfortable installing a normal application but not configuring a server.

### 4.2 Secondary users

- Students managing project-heavy degrees with source repositories and datasets.
- Postgraduate students organizing papers, notes, milestones, and supervision material.
- Contributors who want to adapt the software to a different learning platform.

### 4.3 Accessibility expectations

The application should support keyboard navigation, readable contrast, scalable text, visible focus state, and labels for icon-only actions. Color must never be the only way information is communicated.

## 5. Product Scope

### 5.1 Core capabilities

1. Create and organize academic modules.
2. Associate one or more existing folders with a module.
3. Index supported resources without moving them.
4. Browse and open resources in their normal applications.
5. Create and manage personal academic tasks.
6. Present a useful Today view.
7. Search across modules, tasks, filenames, and indexed document text.
8. Surface related resources using transparent signals.
9. Import deadlines from standard calendar files such as Moodle `.ics` exports.
10. Back up, restore, and rebuild local application data safely.

### 5.2 Explicit non-goals for early releases

- Replacing Moodle or submitting assignments to it.
- Becoming a full note editor or word processor.
- Synchronizing application state between devices.
- Collaborative editing or multi-user workspaces.
- Automatic modification, renaming, or deletion of academic files.
- A hosted account system.
- Generative AI as a required dependency.
- Mobile applications.
- Grade prediction presented as authoritative advice.

These may be revisited after the local desktop workflow is stable.

## 6. Information Architecture

The main navigation should remain small and stable.

### 6.1 Today

The default page answers three questions:

- What requires attention?
- What was I recently working on?
- What useful action can I take next?

Candidate sections:

- Due soon
- Overdue
- Planned for today
- Continue working
- Upcoming exams
- Recently added or changed resources

Sections with no content should collapse cleanly rather than display empty cards.

### 6.2 Modules

The module list leads to a workspace for each subject. A module page may contain:

- identity: name, code, term, color, and optional lecturer;
- active tasks and deadlines;
- linked folders;
- resource filters such as notes, slides, assignments, and past papers;
- recent resources;
- related material;
- module-specific search.

### 6.3 Tasks

The task view supports scanning and editing work across modules. Important dimensions include status, due date, module, type, priority, and estimated effort.

### 6.4 Resources

The resource view provides a cross-module file browser over indexed references. It does not replace the operating system's file manager. Its value is academic classification, filtering, relationships, and search.

### 6.5 Calendar

The calendar combines personal tasks, exams, and imported events. It should show provenance so imported Moodle events are distinguishable from user-created tasks.

### 6.6 Search

Global search should be reachable from anywhere with a keyboard shortcut. Results should be grouped by type and show enough location context to disambiguate similar names.

### 6.7 Settings

Settings cover data location, indexing behavior, appearance, import sources, backups, diagnostics, and application information.

## 7. Primary Workflows

### 7.1 First run

1. StudyIndex explains that files stay in place.
2. The user creates their first module.
3. The user chooses one or more existing folders.
4. StudyIndex performs a visible initial scan.
5. The module page displays discovered resources.
6. The user can immediately open a resource.

The first-run flow should not require account creation, theme selection, or a lengthy questionnaire.

### 7.2 Daily use

1. The application opens to Today.
2. The user sees urgent tasks and recent work.
3. The user opens a task or module.
4. Relevant resources are visible beside the work.
5. The user opens the external file in its default application.
6. StudyIndex records only useful recency metadata, not invasive activity monitoring.

### 7.3 Linking a folder

1. The user selects a module.
2. The user invokes Add Folder.
3. A native directory picker opens.
4. StudyIndex validates accessibility and overlap with existing roots.
5. The user gives the root an optional label.
6. A background scan starts.
7. Progress and recoverable errors are displayed.

### 7.4 Missing or moved folder

1. StudyIndex detects that a root is unavailable.
2. Existing resource records remain visible but are marked unavailable.
3. The user may locate the moved root, remove the reference, or leave it disconnected.
4. Relocating the root updates one record because resources store relative paths.

### 7.5 Importing Moodle dates

1. The user chooses an `.ics` file exported by Moodle.
2. StudyIndex previews events and likely module matches.
3. The user confirms or changes mappings.
4. Imported items preserve their source identifiers.
5. Re-import updates matching events instead of creating duplicates.

## 8. User Interface Direction

StudyIndex should use PySide6 with Qt Widgets for the initial implementation. Widgets offer a mature desktop model, good native integration, accessibility support, and straightforward packaging.

### 8.1 Main window layout

- Narrow left navigation sidebar
- Persistent global search entry near the top
- Main content area using a stacked page container
- Optional details pane for selected work or resources
- Status region for background scans and recoverable errors

### 8.2 Visual character

- Calm, high-contrast neutral surfaces
- Module colors used sparingly as identifiers
- Dense enough for repeated daily use
- Borders and spacing used to establish hierarchy
- Minimal animation, limited to transitions that clarify state
- No nested card collections or oversized marketing-style headings

### 8.3 Interaction conventions

- Familiar icons for opening, searching, refreshing, adding, and settings
- Tooltips for unfamiliar icon-only controls
- Context menus for secondary resource actions
- Native file and folder pickers
- Destructive actions require clear target names and confirmation when recovery is difficult
- Long-running scans never freeze the user interface

### 8.4 Initial screen set

Version 0.1.0 needs only:

- application shell;
- module list;
- create/edit module dialog;
- module workspace;
- linked-folder management;
- resource list;
- scan progress and error feedback.

## 9. Domain Model

The initial domain language should remain independent from Qt and SQLAlchemy where practical.

### 9.1 Module

Represents an academic subject or unit.

Suggested fields:

- `id`: stable UUID
- `name`: required display name
- `code`: optional institutional code
- `term`: optional free-form term initially
- `color`: validated display color
- `archived`: whether hidden from current work
- `created_at`
- `updated_at`

### 9.2 LibraryRoot

Represents a user-approved directory associated with a module.

Suggested fields:

- `id`: stable UUID
- `module_id`
- `path`: normalized absolute root path
- `label`: optional human-readable purpose
- `available`: last observed availability
- `last_scan_started_at`
- `last_scan_completed_at`
- `created_at`

### 9.3 Resource

Represents an indexed file. It is not the file itself.

Suggested fields:

- `id`: stable UUID
- `library_root_id`
- `relative_path`
- `filename`
- `extension`
- `media_type`
- `category`
- `size_bytes`
- `modified_at`
- `content_hash`: optional and calculated only when needed
- `indexed_at`
- `available`

The unique identity inside a root should initially be `library_root_id + relative_path`. Rename detection may later use filesystem identity or hashes, but should not complicate the first release.

### 9.4 Task

Represents work the student intends to complete.

Suggested fields:

- `id`: stable UUID
- `module_id`: optional for general tasks
- `title`
- `description`
- `status`: inbox, planned, in_progress, completed, or cancelled
- `due_at`: optional timezone-aware timestamp
- `estimated_minutes`: optional
- `priority`: optional user-selected level
- `source_type`: local or imported
- `source_id`: optional external identity
- `created_at`
- `updated_at`
- `completed_at`

### 9.5 Event

Represents calendar information that may not be actionable. Exams and imported timetable events should not be forced into the Task model merely because both have dates.

### 9.6 Tag and Topic

Tags should be delayed until a concrete workflow needs them. Topics are more meaningful academically but require careful extraction and matching. Early related-resource behavior can use module membership, path components, filename tokens, and explicit links.

## 10. Data Ownership And Storage

### 10.1 SQLite decision

SQLite is the preferred application database because StudyIndex is local, single-user, offline, and modest in scale. It removes the need for a database service and can be included naturally in desktop distribution.

SQLite stores:

- modules;
- linked roots;
- indexed resource metadata;
- extracted searchable text;
- tasks and events;
- user-defined relationships;
- application settings that are unsuitable for platform preferences;
- migration state.

SQLite does not store original academic documents.

### 10.2 Database access

SQLAlchemy 2.x provides explicit sessions, transactions, typed mappings, and a testable repository implementation. Alembic owns schema migrations.

Rules:

- No SQLAlchemy model escapes into the presentation layer.
- UI code does not create sessions or issue queries.
- Transactions are controlled by application operations.
- Database work that could block is moved off the UI thread.
- Foreign keys are enabled for every SQLite connection.
- Development and release builds use the same migration path.

### 10.3 Application data directories

Use `platformdirs` rather than placing mutable state beside the executable.

Conceptual locations:

- data: database and durable application state;
- cache: rebuildable extracted text and previews where appropriate;
- logs: rotating diagnostic logs;
- configuration: small user preferences if not stored in the database.

Exact locations depend on the operating system.

### 10.4 Backup model

Backups should contain the SQLite database plus a small manifest. They should never copy the user's linked academic folders. A backup can restore organization and metadata, but missing source files remain the user's responsibility.

SQLite backups must use its online backup mechanism or a closed connection, not a casual copy during writes.

## 11. Filesystem Indexing

### 11.1 Safety rules

- Scan only roots explicitly selected by the user.
- Never follow directory links outside an approved root by default.
- Never modify scanned files.
- Skip inaccessible entries and report them without ending the entire scan.
- Apply configurable exclusions for hidden directories, build outputs, dependency folders, and temporary files.
- Normalize paths for comparison while preserving a usable display form.

### 11.2 Scan phases

1. Enumerate candidate files.
2. Compare path, size, and modification time with stored metadata.
3. Upsert new or changed resources.
4. Mark missing resources unavailable or remove derived records according to policy.
5. Queue supported files for content extraction.
6. Commit scan summary and completion time.

Metadata discovery and content extraction should be separate. This lets filenames appear quickly while expensive document parsing continues in the background.

### 11.3 Initial supported files

Version 0.1.0 can index metadata for every ordinary file while providing categories for common types:

- PDF documents
- Word documents
- PowerPoint presentations
- plain text and Markdown
- source code
- images
- spreadsheets

Text extraction should begin with PDF and plain-text formats in a later release. Unsupported content remains discoverable by filename and folder.

### 11.4 Watching for changes

Do not add continuous filesystem watching immediately. Manual refresh and scan-on-launch are easier to reason about. A watcher can later enqueue debounced rescans, with periodic reconciliation because operating-system events can be missed.

## 12. Search And Related Work

### 12.1 Search progression

Phase 1 searches structured fields and filenames using normalized text.

Phase 2 adds SQLite FTS5 for extracted document text.

Phase 3 adds ranking signals such as:

- exact title match;
- prefix match;
- module match;
- filename and path match;
- document-text relevance;
- recency;
- availability.

### 12.2 Related-resource progression

Initial relatedness should be deterministic and explainable:

1. Same module
2. Same user-selected category
3. Shared normalized filename terms
4. Shared meaningful path components
5. Explicit task-resource or resource-resource links
6. Similar extracted terms, once full-text indexing exists

A suggestion should be able to display a reason such as `Same module and matching topic: integration`.

Embeddings or a local language model are optional future experiments, not architectural requirements.

## 13. Application Architecture

Proposed source tree:

```text
app.py
study_index/
  __init__.py
  version.py
  domain/
    entities/
    value_objects/
    errors.py
  application/
    commands/
    queries/
    services/
    ports/
  infrastructure/
    database/
    filesystem/
    importers/
    indexing/
    logging/
  presentation/
    windows/
    dialogs/
    pages/
    widgets/
    models/
    styles/
tests/
  unit/
  integration/
  ui/
```

Directories should be introduced only when they contain real code. The structure is a target, not a requirement to create empty architecture in advance.

### 13.1 Dependency direction

```text
presentation -> application -> domain
                         ^
                         |
                 infrastructure
```

The domain must not import PySide6, SQLAlchemy, or operating-system adapters. Application ports describe capabilities such as module persistence and directory scanning. Infrastructure implements those ports.

### 13.2 Practical restraint

Clean architecture does not mean wrapping every library or creating one class per operation. Add boundaries around volatile or externally coupled behavior: database access, filesystem access, imports, document parsing, and UI presentation.

### 13.3 UI state

Qt widgets render state and emit user intent. Application services perform operations. For lists and tables, use Qt's model-view APIs once behavior extends beyond a trivial prototype.

### 13.4 Background work

Directory enumeration and document extraction must not run on the main Qt thread. Workers should report immutable progress messages and support cancellation between files. Database writes should have clear thread ownership.

## 14. Error Handling And Diagnostics

Errors should be divided into:

- expected user-facing conditions, such as a disconnected folder;
- recoverable operation failures, such as one unreadable PDF;
- programming or invariant errors;
- fatal startup problems, such as an unrecoverable migration failure.

User-facing messages should state what failed, what data was affected, and what the user can do. Technical details belong in logs and an optional details view.

Logging must avoid document contents and other sensitive data by default. Paths may contain personal information, so diagnostic export should warn the user and support redaction.

## 15. Privacy And Security

- No telemetry by default.
- No network access for core features.
- No file contents sent to external services.
- External integrations require explicit setup and clear data-flow descriptions.
- Imported files are treated as untrusted input.
- Document parsers run with narrow responsibility and sensible file-size limits.
- Paths received from the database are revalidated before file operations.
- The app opens files through the operating system rather than executing them itself.
- Release artifacts should eventually be signed.
- Dependencies and release workflows should be reviewed for supply-chain risk.

## 16. Dependency Management

Development uses Conda with the `conda-forge` channel and strict channel priority. There is no pip subsection in the environment definition.

Two files serve different purposes:

- `environment.yml` lists direct dependencies and supported version ranges for humans and contributors.
- a multi-platform lockfile records exact resolved builds for repeatable CI and release work.

The application source remains runnable from the repository root with:

```text
python app.py
```

This avoids requiring an editable pip installation. If StudyIndex later publishes a Conda package, a recipe can be added without changing the runtime architecture.

## 17. Versioning

StudyIndex follows Semantic Versioning once public releases begin:

- patch: compatible fixes;
- minor: compatible features;
- major: incompatible user-data, integration, or public-extension changes.

Before 1.0, minor releases may contain intentional design changes, but database migrations should still protect user data.

The authoritative application version should have one source in the repository. Release automation must verify that a `vX.Y.Z` Git tag matches it. Every release records:

- application version;
- Git commit;
- operating system and architecture;
- Python version;
- dependency lock identity.

## 18. Packaging And Installation

PyInstaller creates platform-specific standalone application bundles. It must run on each target operating system rather than cross-compiling.

Packaging strategy:

1. Begin with `onedir` builds because they are easier to inspect and diagnose.
2. Maintain a reviewed PyInstaller spec file.
3. Include icons, styles, migration files, and required Qt plugins explicitly.
4. Run a packaged startup smoke test on every target platform.
5. Wrap the bundle in a platform-appropriate installer only after raw bundles are stable.

Potential later installer formats:

- Windows: Inno Setup, WiX, or MSIX after evaluating update and signing needs
- macOS: signed `.app` distributed in a DMG
- Linux: archive first, then AppImage if demand justifies it

Application updates must not place mutable user data inside the installation directory.

## 19. Continuous Integration And Releases

### 19.1 Pull-request CI

Every pull request should run:

- environment creation from the declared dependency source;
- Ruff formatting check;
- Ruff linting;
- mypy over production code;
- unit tests;
- integration tests that do not require a display;
- selected UI tests using an appropriate virtual display on Linux;
- migration test from the oldest supported database fixture once migrations exist.

### 19.2 Release workflow

A release tag should:

1. Validate the tag and application version.
2. Run the complete test suite.
3. Build separately on Windows, macOS, and Linux.
4. Launch each packaged application in a smoke-test mode.
5. Produce checksums and a machine-readable manifest.
6. Upload immutable artifacts to a GitHub Release.
7. Generate release notes from curated changes.

Signing credentials must be stored as protected repository secrets and never exposed to pull-request workflows.

## 20. Testing Strategy

### 20.1 Unit tests

Fast tests cover domain rules, path classification, ranking, import mapping, and application services using in-memory fakes.

### 20.2 Database integration tests

Use temporary SQLite files to test repositories, constraints, transactions, and migrations. In-memory SQLite can hide connection and filesystem behavior, so it should not be the only database test mode.

### 20.3 Filesystem tests

Temporary directory trees cover nested resources, inaccessible entries where the operating system permits, renames, deleted files, exclusions, duplicate roots, and symbolic-link behavior.

### 20.4 UI tests

Use `pytest-qt` for important widget state and signals. Avoid tests that encode every pixel or internal widget hierarchy. Critical end-to-end flows should include creating a module, linking a temporary folder, scanning it, and opening the resource action through a replaceable system adapter.

### 20.5 Packaged tests

At minimum, each release bundle must start, locate its resources, create or open a temporary database, and exit successfully. Packaging failures often do not appear when running from source.

## 21. Performance Expectations

Initial practical targets, subject to measurement:

- main window visible within two seconds on a typical supported laptop after warm start;
- UI remains responsive during all scans;
- filename search responds within 100 milliseconds for tens of thousands of resources;
- initial metadata results appear before full content extraction finishes;
- idle memory use remains reasonable for a desktop organizer;
- rescans process unchanged files using metadata comparisons instead of reparsing them.

Performance decisions should be based on recorded measurements and representative fixture libraries.

## 22. Migration And Data Compatibility

- Every schema change receives an Alembic migration.
- Application startup checks schema compatibility before opening the main workspace.
- Migrations run with a backup or recovery strategy appropriate to the change.
- Downgrades are not promised for ordinary users, but failed upgrades must provide a clear recovery route.
- Derived search indexes can be deleted and rebuilt after incompatible indexing changes.
- Public releases should include migration tests using prior-version database fixtures.

## 23. Proposed Milestones

### 23.1 Foundation

- Conda environment
- `app.py` entry point
- basic Qt application shell
- logging and platform data directories
- test, lint, and type-check configuration
- initial CI

Exit condition: a clean checkout can create the environment, run checks, and open the application.

### 23.2 Version 0.1.0: Modules and resources

- create, edit, archive, and view modules;
- link and relocate folder roots;
- scan metadata in the background;
- display, filter, refresh, and open resources;
- persist state through SQLite migrations;
- produce a Windows PyInstaller artifact first;
- add macOS and Linux builds once behavior is stable.

Exit condition: a user can organize and reopen their existing academic folders without StudyIndex changing them.

### 23.3 Version 0.2.0: Tasks and Today

- task lifecycle;
- due dates and estimates;
- module association;
- Today query and recent-work behavior;
- overdue and upcoming views.

Exit condition: opening StudyIndex gives a useful answer about current work.

### 23.4 Version 0.3.0: Search

- global command/search surface;
- filename and metadata ranking;
- PDF and text extraction;
- FTS5 index;
- extraction status and errors;
- rebuild controls.

Exit condition: common resources can be found without remembering their folders.

### 23.5 Version 0.4.0: Related work

- explicit resource-task relationships;
- deterministic topic matching;
- explanations for suggestions;
- controls to dismiss or correct weak relationships.

Exit condition: module and task pages reliably surface useful neighboring material.

### 23.6 Version 0.5.0: Calendar import

- `.ics` preview;
- module mapping;
- source identity and idempotent re-import;
- conflict and deletion policy;
- calendar view.

Exit condition: Moodle dates can be refreshed without duplicate entry.

### 23.7 Version 1.0.0: Stable public release

- reviewed onboarding and accessibility;
- backup and restore;
- mature migration coverage;
- signed or clearly documented release artifacts;
- contributor and security documentation;
- stable extension boundaries where actually needed.

## 24. Risks And Mitigations

### 24.1 Scope growth

Risk: The all-in-one idea expands into a learning platform, editor, cloud service, and AI assistant.

Mitigation: Every feature must reinforce one of the core questions: what should I do, where is the material, or what is related?

### 24.2 UI coupled to persistence

Risk: Qt callbacks directly query and mutate the database, making behavior difficult to test.

Mitigation: Route user intent through application services and return presentation-friendly results.

### 24.3 Blocking scans

Risk: Folder or document work freezes the application.

Mitigation: Design worker boundaries and progress messages before adding large-file parsing.

### 24.4 Packaging differences

Risk: Source execution works while packaged builds miss Qt plugins, migrations, or assets.

Mitigation: Keep a spec file and execute packaged smoke tests from the first release milestone.

### 24.5 Stale paths

Risk: Files and folders are moved outside StudyIndex.

Mitigation: Model availability explicitly, separate roots from relative paths, and support root relocation.

### 24.6 Sensitive academic data

Risk: Logs, telemetry, or integrations expose filenames or content.

Mitigation: No telemetry by default, local processing, conservative logging, and explicit integration consent.

### 24.7 Conda ecosystem variance

Risk: Package versions or builds differ across platforms.

Mitigation: Maintain supported ranges for contributors, exact release lock inputs, and native CI builds for every target.

## 25. Decisions Already Made

- Product name for development: StudyIndex.
- Product shape: local desktop application.
- UI toolkit: PySide6 and Qt Widgets initially.
- Primary language: Python.
- Dependency manager: Conda without pip.
- Database: SQLite through SQLAlchemy, migrated by Alembic.
- File policy: index references and derived metadata; do not relocate originals.
- Packaging: PyInstaller, beginning with `onedir`.
- Source control: Git with GitHub CI and releases planned.
- Versioning: Semantic Versioning.
- Default privacy posture: offline and no telemetry.

## 26. Open Product Questions

These questions should be answered through small prototypes or real use rather than guesswork:

1. Should a module be allowed to span multiple academic years or should occurrences be distinct?
2. Which task statuses feel natural in daily use without becoming project-management overhead?
3. Should imported deadlines become tasks automatically or remain calendar events until promoted?
4. Which resource categories can be inferred safely, and which should remain user-defined?
5. How should overlapping linked roots be presented or prevented?
6. What does `recently worked on` mean without intrusive monitoring?
7. How much extracted document text should be retained, and how should users exclude sensitive files?
8. Is a details pane more efficient than separate resource detail pages?
9. Which keyboard workflows matter enough to design before polishing the interface?
10. What minimum signing and installer experience is acceptable for the first public release?

## 27. Immediate Next Decisions

Before implementing broad features, the first development session should settle:

1. Repository conventions and license choice.
2. The exact Conda environment and supported Python version.
3. Basic Qt application bootstrap.
4. Application data directory creation.
5. The first Module domain object and validation rules.
6. A minimal SQLite connection and migration.
7. A narrow end-to-end workflow: create a module, link a folder, scan filenames, display them, restart, and recover the same state.

## 28. Definition Of A Good First Public Release

StudyIndex 0.1.0 is successful when another student can:

- download the correct artifact for their system;
- launch it without installing Python or Conda;
- understand that their files remain where they are;
- create a module and connect existing folders;
- see and filter discovered files;
- open a file in its normal application;
- move a linked folder and reconnect it;
- close and reopen StudyIndex without losing organization;
- report a useful diagnostic when something fails.

It does not need tasks, semantic search, AI, Moodle integration, or a complete visual identity to satisfy that release. It does need to be trustworthy.

## 29. Document Maintenance

This document is working project context rather than polished user documentation. When a decision becomes stable and relevant to contributors, it should also be represented through an architecture decision record, contributor guide, user documentation, or code where appropriate.

Update this document when:

- the product boundary changes;
- a major architectural decision is made;
- a risk is discovered or retired;
- a milestone changes meaning;
- real usage contradicts an assumption.

Do not update it merely to mirror every implementation detail. Its purpose is to preserve intent and reasoning.
