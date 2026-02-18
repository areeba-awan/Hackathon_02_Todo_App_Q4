# Vercel Deployment Guide for Todo App

## Prerequisites
- Vercel account (free at https://vercel.com)
- Backend API deployed and accessible via HTTPS

## Step 1: Deploy Backend First

Your backend (FastAPI) needs to be deployed separately. Options:
- **Railway**: https://railway.app (recommended for FastAPI)
- **Render**: https://render.com
- **Fly.io**: https://fly.io

### Deploy Backend to Railway:
1. Push your backend code to GitHub
2. Go to https://railway.app and create account
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your backend repository
5. Add environment variables:
   - `DATABASE_URL`: Your Neon PostgreSQL connection string
   - `BETTER_AUTH_SECRET`: Your auth secret
   - `FRONTEND_URL`: Your Vercel frontend URL (after deployment)
6. Deploy and copy the public URL

## Step 2: Deploy Frontend to Vercel

### Option A: Using Vercel CLI (Recommended)

```bash
# Install Vercel CLI
npm install -g vercel

# Navigate to frontend folder
cd frontend

# Login to Vercel
vercel login

# Deploy
vercel
```

Follow the prompts:
- Set up and deploy? **Y**
- Which scope? **Select your account**
- Link to existing project? **N** (first time)
- Project name: **todo-app-frontend**
- Directory: **./** (current directory)
- Override settings? **N**

### Option B: Using Vercel Dashboard

1. Go to https://vercel.com/dashboard
2. Click "Add New" → "Project"
3. Import your Git repository
4. Configure:
   - **Framework Preset**: Next.js
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `.next` (default)

5. Add Environment Variables:
   - Click "Environment Variables" → "Add Variable"
   - Name: `NEXT_PUBLIC_API_URL`
   - Value: `https://your-backend-url.railway.app` (your deployed backend URL)
   - Environment: Production ✓

6. Click "Deploy"

## Step 3: Update Backend CORS

After frontend is deployed, update backend CORS to allow your Vercel URL:

In `backend/main.py`, update:
```python
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")
```

Add your Vercel URL in `.env`:
```
FRONTEND_URL=https://your-app.vercel.app
```

## Step 4: Test Deployment

1. Visit your Vercel URL: `https://your-app.vercel.app`
2. Test signup/login
3. Create tasks and verify they work

## Environment Variables Summary

### Frontend (Vercel):
- `NEXT_PUBLIC_API_URL` = Your backend URL

### Backend (Railway/Render):
- `DATABASE_URL` = Neon PostgreSQL URL
- `BETTER_AUTH_SECRET` = Your auth secret
- `FRONTEND_URL` = Your Vercel frontend URL

## Troubleshooting

### API Calls Failing
- Check that `NEXT_PUBLIC_API_URL` is set correctly in Vercel
- Ensure backend CORS allows your Vercel domain
- Verify backend is running and accessible

### Build Failures
- Check build logs in Vercel dashboard
- Ensure all dependencies are in `package.json`
- Try running `npm run build` locally first

## Useful Commands

```bash
# Deploy to production
vercel --prod

# View deployment logs
vercel logs

# List deployments
vercel ls
```
