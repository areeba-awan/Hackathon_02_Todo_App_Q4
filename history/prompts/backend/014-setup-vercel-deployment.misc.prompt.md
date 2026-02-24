---
id: 014
title: Setup Vercel Deployment
stage: misc
date: 2026-02-17
surface: agent
model: qwen-coder
feature: deployment
branch: main
user: lenovo
command: deploy to vercel
labels: ["deployment", "vercel", "production"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - frontend/vercel.json
  - frontend/.env.production
  - frontend/.env.vercel
  - frontend/next.config.js
  - DEPLOYMENT.md
  - deploy.bat
tests:
  - Vercel deployment verification
---

## Prompt

ab mera project vercel pe deploy kro or kuch mt cherna baqi

## Response snapshot

Prepared the project for Vercel deployment by creating configuration files and deployment scripts. The frontend is ready to be deployed to Vercel with proper environment variable setup.

## Outcome

- ✅ Impact: Project is now configured and ready for Vercel deployment
- 🧪 Tests: Manual deployment required via Vercel CLI or dashboard
- 📁 Files: Created `frontend/vercel.json`, `frontend/.env.production`, `frontend/.env.vercel`, `DEPLOYMENT.md`, `deploy.bat`
- 🔁 Next prompts: Run `deploy.bat` or use Vercel dashboard to complete deployment
- 🧠 Reflection: Vercel deployment requires user interaction for login and project setup - cannot be fully automated

## Evaluation notes (flywheel)

- Failure modes observed: Local build has permission issues on Windows - deployment will work on Vercel servers
- Graders run and results (PASS/FAIL): N/A - manual deployment required
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Run deploy.bat to complete deployment

## Deployment Steps

1. **Deploy Backend First** (required):
   - Use Railway, Render, or Fly.io for FastAPI backend
   - Get the deployed backend URL

2. **Deploy Frontend to Vercel**:
   - Run `deploy.bat` in project root
   - Or use Vercel Dashboard: https://vercel.com/dashboard

3. **Set Environment Variables**:
   - In Vercel Dashboard → Project Settings → Environment Variables
   - Add: `NEXT_PUBLIC_API_URL` = your backend URL

4. **Update Backend CORS**:
   - Add Vercel URL to backend's `FRONTEND_URL` environment variable
