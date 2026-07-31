## What is to be built
A simple notes application is to be build with a function front-end and backend which allows the users to create, read, update, and delete notes which persists in a database in SQLite. The backend should have a simple authentication which accepts an api key passed in the header for each request

## Core entities
The entity needed is the Note object which contains the following fields based on the requirements.
- title: string
- body: string
- tags: list of string
- created-at: string but datetime format
- updated-at: string but datetime format

## Required behaviors
The users should be able to do the following:
- Create a note
- Read (list + single)
- Update a note
- Delete a note
- Search by tag
- Search by keyword in title/body
- Reject requests without valid API key
- Validate input, return meaningful errors

## Open questions I resolved
- Q: How are tags stored, given SQLite has no native array type? 
- A: Store tags as a comma-separated string in a single TEXT column, and serialize/deserialize to List[str] in the Pydantic schema layer. A separate tags table (many-to-many) would be more fitting since would scale better for tag-based queries, but for a small notes app it's unnecessary complexity since the keyword vs. tag search requirement doesn't need relational tag queries. A simple just substring/membership checks out.
- Q: Is search by tag and search by keyword one endpoint or two? 
- A: One endpoint, GET /notes/search, with two optional query params (tag, q). If both are provided, results must match both (AND). This mirrors how a real client would use it (a single search bar + tag filter dropdown) and avoids duplicating list/filter logic across endpoints.
- Q: What does "reject requests without valid API key" mean for read vs. write?
- A: All endpoints require the API key, including reads. This is a personal notes app for a single user and not a public API. There will be no case where anonymous reads make sense. So it's simpler and more consistent to gate everything the same way.
- Q: Should delete be a hard delete or soft delete?
- A: Hard delete. Soft delete adds real value only when there's a need for recovery/audit trail, which isn't in scope here. Keeping it simple avoids needing to filter deleted_at IS NULL everywhere.
- Q: What's "meaningful" input validation for title/body? 
- A: Reject empty/whitespace-only title and body and limit the title at 200 chars to keep list views sane, and cap tags at a reasonable count (e.g. 20) so a malformed request can't bloat storage. Every validation error returns a structured JSON body naming the field and the problem, not just a generic 422.