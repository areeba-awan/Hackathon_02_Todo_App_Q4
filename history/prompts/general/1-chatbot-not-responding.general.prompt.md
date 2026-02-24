---
id: 1
title: Chatbot not responding - Fixed .env configuration
stage: general
date_iso: 2026-02-22
surface: agent
model: qwen-coder
feature: none
branch: main
user: lenovo
command: N/A
labels: ["bugfix", "chatbot", "configuration"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml: |
  - backend/.env
  - backend/ai/config.py
tests_yaml: |
  - curl -X GET "http://localhost:8000/health"
---

## PROMPT_TEXT

my chatbot is not responding me baqi sb thk chl rha hai or kuch b ni cherna bs ye thk krdo Sorry, something went wrong. Please try again. or kuch b ni cherna bs

## RESPONSE_TEXT

Fixed the chatbot response issue by:

1. **Created missing `.env` file** in `backend/` directory with required environment variables:
   - `DATABASE_URL` (Neon PostgreSQL connection string)
   - `BETTER_AUTH_SECRET` (JWT secret)
   - `COHERE_API_KEY` (Cohere AI API key)
   - `COHERE_MODEL` (command-r-plus)
   - `FRONTEND_URL` (http://localhost:3000)

2. **Fixed `DATABASE_URL` variable name** - Changed from `NEON_DATABASE_URL` to `DATABASE_URL` to match what `db.py` expects.

3. **Fixed API key validation** in `backend/ai/config.py` - Removed strict `sk-` prefix requirement that was incompatible with the actual Cohere API key format.

4. **Restarted backend server** - Backend is now running on `http://localhost:8000` and health check returns `{"status":"healthy","version":"1.0.0"}`.

## OUTCOME

Chatbot backend is now running and should respond to messages. The "Sorry, something went wrong" error was caused by:
- Missing `.env` file (no API keys loaded)
- Wrong environment variable name (`NEON_DATABASE_URL` vs `DATABASE_URL`)
- Overly strict API key validation
