# architecture-decisions.md

## Auth
For authentication I chose a static API key checked via a FastAPI dependency, passed in an `X-API-Key` header and compared against a value stored in an environment variable. I considered OAuth2/JWT with per-user accounts, but this is a single user notes app with no concept of having multiple users. The JWT/OAuth2 would solve a problem I don't have (identity, sessions, token expiry/refresh) and add commplexity with no corresponding benefit. A shared static key satisfies the "reject requests without valid API key" requirement with minimal surface area.

## Tags storage
Tags are stored as a single `tags` TEXT column holding a comma-separated string,
converted to and from `List[str]` at the Pydantic schema layer. The alternative I
considered was a proper many-to-many design with a separate `tags` table and a
`note_tags` join table. That's the more "correct" normalized approach, and it
would be the right call if tags needed to be queried or counted independently
(e.g. listing all distinct tags, tag autocomplete) or reused across notes with
referential integrity. But since neither of those is a stated requirement here. The CSV column keeps the schema to a single table and the ORM model trivial, at the cost of doing tag search with a `LIKE` on the raw string instead of a join, which is an acceptable trade-off at this scale.

## Search implementation
Search is implemented as a SQL `LIKE '%term%'` query (case-insensitive) against `title`, `body`, and `tags`, combined with `AND` when both a `tag` and a `q` parameter are given. I considered SQLite's FTS5 full-text search extension, which gives better relevance ranking and performance at scale, but it requires a second virtual table kept in sync with the notes table via triggers or manual writes. This meaningful extra plumbing for an app that will likely hold a small number of notes. `LIKE` is an O(n) table scan, but it's simple, correct, and fully sufficient at the sizes this app will realistically see. I've noted it as a known scaling limit rather than treating it as invisible.

## ORM vs. raw SQL
I used the SQLAlchemy ORM with declarative models, paired with Pydantic schemas for request/response validation, rather than raw `sqlite3` with hand-written SQL. Raw SQL would mean fewer dependencies and arguably more transparency for something this small, but the ORM gives automatic parameterization (SQL injection safety by default). It also gives a clean separation between DB models and API schemas, and less boilerplate across the CRUD and search endpoints. Since the task explicitly calls for input validation and meaningful errors, having Pydantic schemas sit on top of the ORM models keeps that validation logic in one obvious place rather than scattered across hand-written queries.

## Frontend state
On the frontend I used plain React `useState`/`useEffect` in the page component, backed by a small typed `api.ts` fetch wrapper, rather than a global state library like Redux or Zustand, or a data-fetching library like React Query. The app really only has one piece of shared state (the notes list) and one form, so a global store or a caching/query library wouldn't be needed for this project. Local state keeps the code easy for a reviewer to follow without first having to learn a state-management convention.