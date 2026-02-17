# Quickstart Guide: Backend Setup

**Feature**: Backend API for Todo App
**Branch**: 002-backend-specs
**Created**: 2026-02-17
**Status**: Draft

---

## Overview

This guide provides step-by-step instructions for setting up the FastAPI backend development environment.

---

## Prerequisites

- Python 3.11 or higher
- pip (Python package manager)
- Neon PostgreSQL database (provisioned)
- Better Auth service (frontend) for JWT tokens

---

## Step 1: Create Project Structure

Create the backend directory structure:

```
backend/
  main.py
  db.py
  models.py
  schemas.py
  auth.py
  routes/
    tasks.py
  .env
  .env.example
  .gitignore
  requirements.txt
```

---

## Step 2: Set Up Python Virtual Environment

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

---

## Step 3: Install Dependencies

Create `requirements.txt`:

```txt
fastapi>=0.104.0
uvicorn[standard]>=0.24.0
sqlmodel>=0.0.14
psycopg2-binary>=2.9.9
PyJWT>=2.8.0
python-dotenv>=1.0.0
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Step 4: Configure Environment Variables

Create `.env` file in the backend directory:

```bash
# Database connection (from Neon PostgreSQL)
DATABASE_URL=postgresql://user:password@host.neon.tech/database?sslmode=require

# JWT verification secret (must match Better Auth service)
BETTER_AUTH_SECRET=your-super-secret-key-at-least-32-characters-long

# Frontend URL for CORS
FRONTEND_URL=http://localhost:3000
```

**Important**:
- Never commit `.env` to version control
- Use `.env.example` as a template
- `BETTER_AUTH_SECRET` must match the frontend auth service

Create `.env.example` (safe to commit):

```bash
DATABASE_URL=postgresql://user:password@host.neon.tech/database?sslmode=require
BETTER_AUTH_SECRET=your-secret-key-here
FRONTEND_URL=http://localhost:3000
```

---

## Step 5: Create .gitignore

Create `.gitignore` file:

```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
ENV/

# Environment
.env

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
```

---

## Step 6: Initialize Database

After creating the models (see `models.py`), initialize the database:

```python
# Run this once to create tables
from sqlmodel import SQLModel, create_engine
from models import Task  # Import all models

engine = create_engine(DATABASE_URL)
SQLModel.metadata.create_all(engine)
```

Verify tables created in Neon PostgreSQL dashboard.

---

## Step 7: Start Development Server

Start the FastAPI server with auto-reload:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Options**:
- `--reload`: Auto-reload on code changes (development only)
- `--host`: Bind to all interfaces (or use `127.0.0.1` for local only)
- `--port`: Server port (default: 8000)

---

## Step 8: Verify Server Running

Open browser to:

- **API Root**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **OpenAPI JSON**: http://localhost:8000/openapi.json

You should see the FastAPI welcome message or API documentation.

---

## Step 9: Test API Endpoints

Use the interactive docs at `/docs` to test endpoints:

1. Click "Authorize" button
2. Enter JWT token: `Bearer {your-token-here}`
3. Try endpoints:
   - `GET /api/tasks` - List tasks
   - `POST /api/tasks` - Create task
   - etc.

Or use curl:

```bash
# List tasks
curl -H "Authorization: Bearer {jwt_token}" http://localhost:8000/api/tasks

# Create task
curl -X POST http://localhost:8000/api/tasks \
  -H "Authorization: Bearer {jwt_token}" \
  -H "Content-Type: application/json" \
  -d '{"title":"Test Task","description":"Testing the API"}'
```

---

## Troubleshooting

### Database Connection Error

**Error**: `could not connect to server`

**Solutions**:
1. Verify `DATABASE_URL` is correct
2. Check Neon PostgreSQL dashboard for connection string
3. Ensure SSL mode is set: `?sslmode=require`
4. Check firewall settings

### JWT Verification Failed

**Error**: `Invalid or expired token`

**Solutions**:
1. Verify `BETTER_AUTH_SECRET` matches frontend
2. Check token is not expired
3. Ensure token format is valid JWT
4. Verify Authorization header format: `Bearer {token}`

### CORS Error

**Error**: `Origin not allowed`

**Solutions**:
1. Add frontend URL to `FRONTEND_URL` env var
2. Check CORS middleware configuration in `main.py`
3. Verify frontend is running on expected port

### Module Import Error

**Error**: `No module named 'xxx'`

**Solutions**:
1. Ensure virtual environment is activated
2. Run `pip install -r requirements.txt`
3. Check you're in the backend directory

---

## Production Deployment Notes

For production deployment:

1. **Disable auto-reload**: Remove `--reload` flag
2. **Use production ASGI server**: Consider Gunicorn with Uvicorn workers
3. **Set production environment variables**:
   - Use secure `BETTER_AUTH_SECRET`
   - Set correct `FRONTEND_URL`
4. **Enable HTTPS**: Required for JWT security
5. **Set up logging**: Configure proper logging for production
6. **Monitor health**: Add health check endpoint

Example production command:

```bash
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
```

---

## Next Steps

After setup:
1. Implement database layer (`db.py`, `models.py`)
2. Implement authentication (`auth.py`)
3. Implement schemas (`schemas.py`)
4. Implement routes (`routes/tasks.py`)
5. Assemble application (`main.py`)
6. Test with frontend integration

---

## References

- FastAPI Documentation: https://fastapi.tiangolo.com/
- SQLModel Documentation: https://sqlmodel.tiangolo.com/
- Uvicorn Documentation: https://www.uvicorn.org/
- Neon PostgreSQL: https://neon.tech/docs
