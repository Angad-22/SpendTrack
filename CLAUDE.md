# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

Spendly — a personal expense tracker built as a Flask tutorial scaffold. The project is staged: `app.py` registers real routes for already-built pages (landing, login, register, terms, privacy) and placeholder routes that return plain strings ("coming in Step N") for features a student will implement later (logout, profile, add/edit/delete expense). Preserve that split — do not replace placeholder routes with real implementations unless the task asks for that step.

## Commands

Windows shell is bash (git-bash). Use Unix paths.

```bash
# First-time setup
python -m venv venv
source venv/Scripts/activate   # Windows bash; on macOS/Linux: source venv/bin/activate
pip install -r requirements.txt

# Run the dev server (http://localhost:5001, debug reload on)
python app.py

# Tests (pytest + pytest-flask are pinned, but no test suite exists yet)
pytest
pytest path/to/test_file.py::test_name
```

Port is **5001**, not Flask's default 5000 — set in `app.py`.

## Architecture

- `app.py` — single-file Flask app, all routes live here. Follow the existing style when adding routes: real routes return `render_template(...)`, unimplemented features return a short placeholder string.
- `database/db.py` — stub for `get_db()` / `init_db()` / `seed_db()`. SQLite DB file is `expense_tracker.db` (gitignored). Schema and seeding are not yet written.
- `templates/` — Jinja templates. `base.html` is the shared layout (navbar, footer, `{% block content %}`, `{% block scripts %}`); every page template extends it. The footer and nav are defined once in `base.html` — do not duplicate them into child templates.
- `static/css/style.css` — global styles used by `base.html`. `static/css/landing.css` — landing-page-only styles, included via the landing template's `{% block head %}`.
- `static/js/main.js` — global JS loaded from `base.html`. Page-specific JS goes inline in the page's `{% block scripts %}`.

Fonts: DM Serif Display + DM Sans from Google Fonts, loaded in `base.html`. Brand mark is the `◈` glyph — reuse it rather than swapping in an icon library.

## Conventions

- **No JS frameworks or build step.** Vanilla JS only (see `file.txt` line 62 — explicit project rule). Do not add npm, bundlers, or a package.json.
- **Commit message style:** `<area>: <lowercase summary>` — e.g. `landing: add youtube modal on see how it works click`. Match this format; `git log` shows the pattern.
- **Scope discipline:** task prompts in this repo (see `file.txt`) frequently say "Do not modify anything else on the page." Respect tight scopes — when asked to change the hero, touch only the hero; when asked to add a footer link, don't restyle the footer.
- Use `url_for('<route_name>')` for internal links in templates, not hardcoded paths. The existing templates follow this (with the exception of the `/terms` and `/privacy` footer links, which are hardcoded).

## Repo-specific notes

- `file.txt` is a scratchpad of past task prompts the user has been running through, not documentation. It's useful as a record of what has already been built and the style of instruction the user gives.
- `.claude/specs/` holds per-step spec + plan docs (e.g. `01-database-setup.md`). Treat these as the source of truth for what to build.
- No README exists; this file is the primary onboarding doc.
