#!/bin/bash
# Deploy script for Railway

echo "🚀 Deploying PulsePoint to Railway..."
echo "📝 Make sure you have:"
echo "   1. Railway CLI installed"
echo "   2. Railway account connected"
echo "   3. Environment variables set"
echo ""

# Check if railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "❌ Railway CLI not found. Please install it first:"
    echo "   npm install -g @railway/cli"
    exit 1
fi

# Check if logged in
if ! railway whoami &> /dev/null; then
    echo "🔑 Please login to Railway first:"
    echo "   railway login"
    exit 1
fi

echo "✅ Railway CLI found and logged in"
echo ""

# Deploy
echo "🚢 Deploying to Railway..."
railway up

echo ""
echo "🎉 Deployment initiated!"
echo "📊 Check your Railway dashboard for deployment status"
echo "🌐 Your app will be available at: https://your-app-name.railway.app"
