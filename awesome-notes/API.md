# Awesome Notes API Documentation

## Base URL
- Development: `http://localhost:5000/api`
- Production: `https://your-api-endpoint.amazonaws.com/api`

## Authentication

All endpoints except `/auth/register` and `/auth/login` require authentication. The application uses session-based authentication with Flask-Login.

## Response Format

### Success Response
```json
{
  "message": "Success message",
  "data": { ... }
}
```

### Error Response
```json
{
  "error": "Error message"
}
```

## Endpoints

### Health Check

#### GET /health
Check if the API is running.

**Response:**
```json
{
  "status": "healthy"
}
```

---

## Authentication Endpoints

### Register User

#### POST /api/auth/register
Create a new user account.

**Request Body:**
```json
{
  "username": "johndoe",
  "email": "john@example.com",
  "password": "securepassword123"
}
```

**Response:** `201 Created`
```json
{
  "message": "User registered successfully",
  "user": {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "role": "user",
    "created_at": "2024-01-01T00:00:00",
    "updated_at": "2024-01-01T00:00:00"
  }
}
```

**Errors:**
- `400 Bad Request`: Missing required fields or validation error
- `400 Bad Request`: Email or username already exists

---

### Login

#### POST /api/auth/login
Authenticate a user and create a session.

**Request Body:**
```json
{
  "email": "john@example.com",
  "password": "securepassword123"
}
```

**Response:** `200 OK`
```json
{
  "message": "Login successful",
  "user": {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "role": "user",
    "created_at": "2024-01-01T00:00:00",
    "updated_at": "2024-01-01T00:00:00"
  }
}
```

**Errors:**
- `400 Bad Request`: Missing email or password
- `401 Unauthorized`: Invalid credentials

---

### Logout

#### POST /api/auth/logout
End the current user session.

**Authentication:** Required

**Response:** `200 OK`
```json
{
  "message": "Logout successful"
}
```

---

### Get Current User

#### GET /api/auth/me
Get information about the currently authenticated user.

**Authentication:** Required

**Response:** `200 OK`
```json
{
  "user": {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "role": "user",
    "created_at": "2024-01-01T00:00:00",
    "updated_at": "2024-01-01T00:00:00"
  }
}
```

---

## Notes Endpoints

### List Notes

#### GET /api/notes
Get all notes for the current user.

**Authentication:** Required

**Response:** `200 OK`
```json
{
  "notes": [
    {
      "id": 1,
      "title": "My First Note",
      "content": "# Hello World\n\nThis is my first note.",
      "user_id": 1,
      "author": "johndoe",
      "created_at": "2024-01-01T00:00:00",
      "updated_at": "2024-01-01T00:00:00"
    },
    {
      "id": 2,
      "title": "Another Note",
      "content": "More content here",
      "user_id": 1,
      "author": "johndoe",
      "created_at": "2024-01-02T00:00:00",
      "updated_at": "2024-01-02T00:00:00"
    }
  ]
}
```

---

### Get Note

#### GET /api/notes/:id
Get a specific note by ID.

**Authentication:** Required

**URL Parameters:**
- `id` (integer): Note ID

**Response:** `200 OK`
```json
{
  "note": {
    "id": 1,
    "title": "My First Note",
    "content": "# Hello World\n\nThis is my first note.",
    "user_id": 1,
    "author": "johndoe",
    "created_at": "2024-01-01T00:00:00",
    "updated_at": "2024-01-01T00:00:00"
  }
}
```

**Errors:**
- `404 Not Found`: Note doesn't exist
- `403 Forbidden`: User doesn't own the note

---

### Create Note

#### POST /api/notes
Create a new note.

**Authentication:** Required

**Request Body:**
```json
{
  "title": "My New Note",
  "content": "# Note Content\n\nThis is the content of my note in markdown."
}
```

**Response:** `201 Created`
```json
{
  "message": "Note created successfully",
  "note": {
    "id": 3,
    "title": "My New Note",
    "content": "# Note Content\n\nThis is the content of my note in markdown.",
    "user_id": 1,
    "author": "johndoe",
    "created_at": "2024-01-03T00:00:00",
    "updated_at": "2024-01-03T00:00:00"
  }
}
```

**Errors:**
- `400 Bad Request`: Missing title

---

### Update Note

#### PUT /api/notes/:id
Update an existing note.

**Authentication:** Required

**URL Parameters:**
- `id` (integer): Note ID

**Request Body:**
```json
{
  "title": "Updated Title",
  "content": "Updated content"
}
```

**Response:** `200 OK`
```json
{
  "message": "Note updated successfully",
  "note": {
    "id": 1,
    "title": "Updated Title",
    "content": "Updated content",
    "user_id": 1,
    "author": "johndoe",
    "created_at": "2024-01-01T00:00:00",
    "updated_at": "2024-01-03T12:00:00"
  }
}
```

**Errors:**
- `404 Not Found`: Note doesn't exist
- `403 Forbidden`: User doesn't own the note
- `400 Bad Request`: No data provided

---

### Delete Note

#### DELETE /api/notes/:id
Delete a note.

**Authentication:** Required

**URL Parameters:**
- `id` (integer): Note ID

**Response:** `200 OK`
```json
{
  "message": "Note deleted successfully"
}
```

**Errors:**
- `404 Not Found`: Note doesn't exist
- `403 Forbidden`: User doesn't own the note

---

### Search Notes

#### GET /api/notes/search
Search notes by title, content, or date range.

**Authentication:** Required

**Query Parameters:**
- `q` (string, optional): Search query for title or content
- `from` (ISO datetime, optional): Start date filter
- `to` (ISO datetime, optional): End date filter

**Examples:**
- `/api/notes/search?q=python`
- `/api/notes/search?from=2024-01-01&to=2024-01-31`
- `/api/notes/search?q=tutorial&from=2024-01-01`

**Response:** `200 OK`
```json
{
  "notes": [
    {
      "id": 1,
      "title": "Python Tutorial",
      "content": "Learning Python...",
      "user_id": 1,
      "author": "johndoe",
      "created_at": "2024-01-15T00:00:00",
      "updated_at": "2024-01-15T00:00:00"
    }
  ],
  "count": 1
}
```

**Errors:**
- `400 Bad Request`: Invalid date format

---

## User Management Endpoints (Admin Only)

### List Users

#### GET /api/users
Get all users (admin only).

**Authentication:** Required (Admin role)

**Response:** `200 OK`
```json
{
  "users": [
    {
      "id": 1,
      "username": "admin",
      "email": "admin@example.com",
      "role": "admin",
      "created_at": "2024-01-01T00:00:00",
      "updated_at": "2024-01-01T00:00:00"
    },
    {
      "id": 2,
      "username": "johndoe",
      "email": "john@example.com",
      "role": "user",
      "created_at": "2024-01-02T00:00:00",
      "updated_at": "2024-01-02T00:00:00"
    }
  ]
}
```

**Errors:**
- `403 Forbidden`: User is not an admin

---

### Get User

#### GET /api/users/:id
Get a specific user (admin only).

**Authentication:** Required (Admin role)

**URL Parameters:**
- `id` (integer): User ID

**Response:** `200 OK`
```json
{
  "user": {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "role": "user",
    "created_at": "2024-01-01T00:00:00",
    "updated_at": "2024-01-01T00:00:00"
  }
}
```

**Errors:**
- `403 Forbidden`: User is not an admin
- `404 Not Found`: User doesn't exist

---

### Update User

#### PUT /api/users/:id
Update a user (admin only).

**Authentication:** Required (Admin role)

**URL Parameters:**
- `id` (integer): User ID

**Request Body:**
```json
{
  "email": "newemail@example.com",
  "username": "newusername",
  "role": "admin"
}
```

**Response:** `200 OK`
```json
{
  "message": "User updated successfully",
  "user": {
    "id": 1,
    "username": "newusername",
    "email": "newemail@example.com",
    "role": "admin",
    "created_at": "2024-01-01T00:00:00",
    "updated_at": "2024-01-03T00:00:00"
  }
}
```

**Errors:**
- `403 Forbidden`: User is not an admin
- `404 Not Found`: User doesn't exist
- `400 Bad Request`: Email or username already in use
- `400 Bad Request`: Invalid role

---

### Delete User

#### DELETE /api/users/:id
Delete a user (admin only).

**Authentication:** Required (Admin role)

**URL Parameters:**
- `id` (integer): User ID

**Response:** `200 OK`
```json
{
  "message": "User deleted successfully"
}
```

**Errors:**
- `403 Forbidden`: User is not an admin
- `404 Not Found`: User doesn't exist
- `400 Bad Request`: Cannot delete your own account

---

## HTTP Status Codes

- `200 OK`: Request successful
- `201 Created`: Resource created successfully
- `400 Bad Request`: Invalid request data
- `401 Unauthorized`: Authentication required or failed
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server error

## Rate Limiting

Currently, there are no rate limits on API endpoints. In production, consider implementing rate limiting to prevent abuse.

## CORS

The API supports CORS for cross-origin requests. Allowed origins are configured in the Flask application.

## Examples

### cURL Examples

**Register:**
```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"test","email":"test@example.com","password":"pass123"}'
```

**Login:**
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -c cookies.txt \
  -d '{"email":"test@example.com","password":"pass123"}'
```

**Create Note:**
```bash
curl -X POST http://localhost:5000/api/notes \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{"title":"My Note","content":"# Hello\nWorld"}'
```

**Get Notes:**
```bash
curl -X GET http://localhost:5000/api/notes \
  -b cookies.txt
```

### JavaScript/TypeScript Examples

Using the Angular HttpClient (as in the frontend):

```typescript
// Login
this.http.post('/api/auth/login', {
  email: 'test@example.com',
  password: 'pass123'
}).subscribe(response => {
  console.log('Logged in:', response);
});

// Create Note
this.http.post('/api/notes', {
  title: 'My Note',
  content: '# Hello World'
}).subscribe(response => {
  console.log('Note created:', response);
});

// Search Notes
this.http.get('/api/notes/search?q=python').subscribe(response => {
  console.log('Search results:', response);
});
```
