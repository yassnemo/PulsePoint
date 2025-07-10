@echo off
echo 🚀 Deploying PulsePoint to Railway...
echo 📝 Make sure you have:
echo    1. Railway CLI installed
echo    2. Railway account connected
echo    3. Environment variables set
echo.

REM Check if railway CLI is installed
railway --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Railway CLI not found. Please install it first:
    echo    npm install -g @railway/cli
    pause
    exit /b 1
)

REM Check if logged in
railway whoami >nul 2>&1
if %errorlevel% neq 0 (
    echo 🔑 Please login to Railway first:
    echo    railway login
    pause
    exit /b 1
)

echo ✅ Railway CLI found and logged in
echo.

REM Deploy
echo 🚢 Deploying to Railway...
railway up

echo.
echo 🎉 Deployment initiated!
echo 📊 Check your Railway dashboard for deployment status
echo 🌐 Your app will be available at: https://your-app-name.railway.app
pause
