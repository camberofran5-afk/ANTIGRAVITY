#!/bin/bash
# One-Command Deployment Script for Netlify
# Usage: ./scripts/deploy-netlify.sh

set -e

echo "🚀 ERP Ganadero V2 - Deployment Script"
echo "========================================"
echo ""

# Run pre-deployment tests
echo "📋 Step 1: Running pre-deployment tests..."
./scripts/pre-deploy-test.sh

echo ""
echo "📦 Step 2: Deploying to Netlify..."
cd projects/erp_ganadero/frontend-v2

# Check if netlify CLI is available
if ! command -v netlify &> /dev/null; then
    echo "Installing Netlify CLI..."
    npm install -g netlify-cli
fi

# Deploy
echo "Deploying to production..."
npx netlify-cli deploy \
  --dir=dist \
  --prod \
  --site=leafy-florentine-759293

echo ""
echo "✅ Deployment complete!"
echo ""

# Run post-deployment tests
cd ../../..
echo "🧪 Step 3: Running post-deployment tests..."
./scripts/post-deploy-test.sh https://leafy-florentine-759293.netlify.app

echo ""
echo "🎉 Deployment successful!"
echo "🌐 Your app is live at: https://leafy-florentine-759293.netlify.app"
