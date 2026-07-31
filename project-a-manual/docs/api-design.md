# api-design.md

All endpoints require header: `X-API-Key: <key>`
Missing/invalid key on any endpoint → `401 Unauthorized`:
```json
{ "detail": "Invalid or missing API key" }
```

---

## POST /notes
Create a note.

**Request**
```json
{
  "title": "Grocery list",
  "body": "Milk, eggs, bread",
  "tags": ["personal", "errands"]
}
```

**Response (success) — 201 Created**
```json
{
  "id": 1,
  "title": "Grocery list",
  "body": "Milk, eggs, bread",
  "tags": ["personal", "errands"],
  "created_at": "2026-07-31T09:00:00Z",
  "updated_at": "2026-07-31T09:00:00Z"
}
```

**Response (error) — 422 Unprocessable Entity** (e.g. empty title)
```json
{
  "detail": [
    { "field": "title", "message": "title must not be empty" }
  ]
}
```

---

## GET /notes
List all notes, most recently updated first.

**Query params (optional)**
- `limit` (int, default 50, max 200)
- `offset` (int, default 0)

**Response (success) — 200 OK**
```json
{
  "total": 3,
  "items": [
    { "id": 1, "title": "Grocery list", "body": "Milk, eggs, bread",
      "tags": ["personal", "errands"],
      "created_at": "2026-07-31T09:00:00Z", "updated_at": "2026-07-31T09:00:00Z" }
  ]
}
```

**Response (error) — 400 Bad Request** (e.g. `limit` out of range)
```json
{ "detail": "limit must be between 1 and 200" }
```

---

## GET /notes/{id}
Fetch a single note.

**Response (success) — 200 OK**
```json
{
  "id": 1,
  "title": "Grocery list",
  "body": "Milk, eggs, bread",
  "tags": ["personal", "errands"],
  "created_at": "2026-07-31T09:00:00Z",
  "updated_at": "2026-07-31T09:00:00Z"
}
```

**Response (error) — 404 Not Found**
```json
{ "detail": "Note with id 1 not found" }
```

---

## PUT /notes/{id}
Full update of a note. All fields required (this is a replace, not a patch).

**Request**
```json
{
  "title": "Grocery list (updated)",
  "body": "Milk, eggs, bread, butter",
  "tags": ["personal", "errands", "urgent"]
}
```

**Response (success) — 200 OK**
```json
{
  "id": 1,
  "title": "Grocery list (updated)",
  "body": "Milk, eggs, bread, butter",
  "tags": ["personal", "errands", "urgent"],
  "created_at": "2026-07-31T09:00:00Z",
  "updated_at": "2026-07-31T09:15:00Z"
}
```

**Response (error) — 404 Not Found**
```json
{ "detail": "Note with id 1 not found" }
```

**Response (error) — 422 Unprocessable Entity**
```json
{
  "detail": [
    { "field": "body", "message": "body must not be empty" }
  ]
}
```

---

## DELETE /notes/{id}
Delete a note permanently.

**Response (success) — 204 No Content**
(empty body)

**Response (error) — 404 Not Found**
```json
{ "detail": "Note with id 1 not found" }
```

---

## GET /notes/search
Search notes by tag and/or keyword. If both params are given, results must match both (AND).

**Query params**
- `tag` (string, optional) — exact tag match, case-insensitive
- `q` (string, optional) — substring match against `title` or `body`, case-insensitive
- `limit` / `offset` — same as `GET /notes`

At least one of `tag` or `q` must be provided.

**Response (success) — 200 OK**
```json
{
  "total": 1,
  "items": [
    { "id": 1, "title": "Grocery list", "body": "Milk, eggs, bread",
      "tags": ["personal", "errands"],
      "created_at": "2026-07-31T09:00:00Z", "updated_at": "2026-07-31T09:00:00Z" }
  ]
}
```

**Response (error) — 400 Bad Request** (neither param given)
```json
{ "detail": "At least one of 'tag' or 'q' query parameters is required" }
```