@echo off
echo ========================================
echo   Vercel Deployment Script
echo ========================================
echo.

cd /d "%~dp0frontend"

echo Step 1: Installing Vercel CLI...
npm install -g vercel
echo.

echo Step 2: Logging in to Vercel...
vercel login
echo.

echo Step 3: Deploying to Vercel...
echo.
echo IMPORTANT: After deployment, set the environment variable:
echo   NEXT_PUBLIC_API_URL = https://your-backend-url.com
echo.
echo You can set this in Vercel Dashboard:
echo   Project Settings ^> Environment Variables
echo.

vercel --prod

echo.
echo ========================================
echo   Deployment Complete!
echo ========================================
pause
