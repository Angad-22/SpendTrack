# Spec: Login and Logout

## Overview
Wire up the login form so existing users can authenticate into Spendly, and replace the `/logout` placeholder with a real implementation. This step introduces Flask's session mechanism: on successful login the user's `id` is stored in `session['user_id']`, and logout clears it. No route guards or profile page are added here — those belong to Step 4. The goal is simply: credentials → session → redirect, and logout → clear session → redirect.

## Depends on
- Step 01 — Database setup (`users` table must exist, `get_db()` must work)
- Step 02 — Registration (`users` rows with hashed passwords must exist)

## Routes
- `GET /login` — render the login form — public (already exists, convert to GET+POST)
- `POST /login` — validate credentials, set session, redirect to `/profile` — public
- `GET /logout` — clear session, redirect to `/login` — public (replaces placeholder)

## Database changes
No database changes. The `users` table already has all required columns: `id`, `email`, `password_hash`.

## Templates
- **Modify:** `templates/login.html`
  - Change form `action` to `{{ url_for('login') }}` and `method="post"`
  - Add `{% if error %}` error banner (same pattern as `register.html`)
  - Add `{% if request.args.get('registered') %}` success banner: "Account created — please log in"
  - Keep all existing markup; only add the two conditional blocks and update the form tag

## Files to change
- `app.py`
  - Import `session` from flask (add to existing import line)
  - Set `app.secret_key` immediately after `app = Flask(__name__)` — use a hard-coded dev string for now (e.g. `"dev-secret-change-in-prod"`)
  - Convert `login` route from GET-only to GET+POST with credential validation logic
  - Replace `logout` placeholder with real implementation that calls `session.clear()` and redirects to `url_for('login')`
- `templates/login.html`
  - See Templates section above

## Files to create
None.

## New dependencies
No new dependencies. `werkzeug.security` (for `check_password_hash`) and `flask.session` are already available.

## Rules for implementation
- No SQLAlchemy or ORMs — use raw `sqlite3` via `get_db()`
- Parameterised queries only — never use string formatting in SQL
- Passwords verified with `werkzeug.security.check_password_hash`
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- Store only `session['user_id']` (the integer PK) — do not store name, email, or the hash in the session
- Use a single generic error message for failed login: "Invalid email or password" — do not reveal whether the email exists
- After successful login, redirect to `url_for('profile')` (still a placeholder — that is fine)
- After logout, redirect to `url_for('login')`
- Do not add `@login_required` guards to any route in this step — that is Step 4
- Do not modify any page other than `login.html` and `app.py`

## Definition of done
- [ ] Submitting the login form with correct credentials stores `session['user_id']` and redirects to `/profile`
- [ ] Submitting with a wrong password re-renders the form with "Invalid email or password"
- [ ] Submitting with an email that does not exist re-renders the form with "Invalid email or password"
- [ ] Submitting with any blank field is rejected server-side with the same error message
- [ ] Visiting `/logout` clears the session and redirects to `/login`
- [ ] After registration, the login page shows "Account created — please log in" when `?registered=1` is present
- [ ] No 500 errors under any normal user-error scenario
- [ ] No other pages or routes are affected
