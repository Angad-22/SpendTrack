# Spec: Registration

## Overview
Wire up the registration form so new users can create a Spendly account. The `POST /register` route will validate the submitted fields, reject duplicates and weak passwords, hash the password with werkzeug, insert the new row into the `users` table, on success user is shown with a success message and then redirected to the login page. The UI template (`register.html`) and the database schema are already in place from prior steps — this step only adds the server-side handler.

## Depends on
- Step 01 — Database setup (`users` table must exist, `get_db()` must work)

## Routes
- `GET /register` — render the registration form — public (already exists, no change needed)
- `POST /register` — process form submission, create user, redirect to login — public

## Database changes
No database changes. The `users` table is already defined with the correct schema:
`id`, `name`, `email` (UNIQUE), `password_hash`, `created_at`

## Templates
- **Modify:** `templates/register.html`
  - Change `action="/register"` to `action="{{ url_for('register') }}"` for consistency
  - The `{% if error %}` block is already in place — no structural changes needed

## Files to change
- `app.py` — convert the `register` route from GET-only to GET+POST; add form handling logic
- `templates/register.html` — update form `action` to use `url_for`

## Files to create
None.

## New dependencies
No new dependencies. `werkzeug.security` is already installed.

## Rules for implementation
- No SQLAlchemy or ORMs — use raw `sqlite3` via `get_db()`
- Parameterised queries only — never use string formatting in SQL
- Passwords hashed with `werkzeug.security.generate_password_hash`
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- Import `request`, `redirect`, `url_for` from Flask as needed
- Do not use `flask.session` in this step — session/login handling is Step 3
- On duplicate email (UNIQUE constraint violation), re-render the form with a user-friendly error message — do not let the sqlite3 exception bubble up as a 500
- Minimum password length: 8 characters — validate server-side before touching the DB
- After successful registration, redirect to `url_for('login')` — do not auto-login the user yet
- Do not modify any other route or page

## Definition of done
- [ ] Submitting the form with valid data inserts a new row in `users` with a hashed password (not plaintext)
- [ ] Submitting with an email that already exists re-renders the form with the message "An account with that email already exists"
- [ ] Submitting with a password shorter than 8 characters re-renders the form with the message "Password must be at least 8 characters"
- [ ] Submitting with any blank field is rejected (HTML `required` + server-side guard)
- [ ] Successful registration redirects to `/login`
- [ ] The password column in the DB contains a werkzeug hash string, not the raw password
- [ ] No 500 errors under any normal user-error scenario
- [ ] No other pages or routes are affected
