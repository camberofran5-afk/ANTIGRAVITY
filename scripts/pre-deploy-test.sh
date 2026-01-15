#!/bin/bash
# Pre-Deployment Test Script
# Run this before every deployment to catch issues early

set -e

echo "🧪 Running pre-deployment tests for ERP Ganadero V2..."
echo ""

# Navigate to frontend directory
cd "$(dirname "$0")/../projects/erp_ganadero/frontend-v2"

# 1. Check Node.js is installed
echo "1️⃣  Checking Node.js..."
if ! command -v node &> /dev/null; then
    echo "❌ Node.js not found. Please install Node.js"
    exit 1
fi
echo "✅ Node.js $(node --version)"

# 2. Check npm dependencies
echo ""
echo "2️⃣  Checking dependencies..."
if [ ! -d "node_modules" ]; then
    echo "⚠️  node_modules not found. Running npm install..."
    npm install
fi
echo "✅ Dependencies installed"

# 3. Run build
echo ""
echo "3️⃣  Building production bundle..."
npm run build
if [ $? -ne 0 ]; then
    echo "❌ Build failed"
    exit 1
fi
echo "✅ Build successful"

# 4. Check dist folder exists
echo ""
echo "4️⃣  Verifying build output..."
if [ ! -d "dist" ]; then
    echo "❌ dist folder not found"
    exit 1
fi
echo "✅ dist folder exists"

# 5. Check critical files
echo ""
echo "5️⃣  Checking critical files..."

if [ ! -f "dist/index.html" ]; then
    echo "❌ index.html not found"
    exit 1
fi
echo "✅ index.html found"

if [ ! -d "dist/assets" ]; then
    echo "❌ assets folder not found"
    exit 1
fi
echo "✅ assets folder found"

# 6. Check PWA files
echo ""
echo "6️⃣  Checking PWA files..."

if [ -f "public/sw.js" ]; then
    echo "✅ Service worker source found"
else
    echo "⚠️  Warning: Service worker not found (PWA features may not work)"
fi

if [ -f "public/manifest.json" ]; then
    echo "✅ PWA manifest source found"
else
    echo "⚠️  Warning: PWA manifest not found"
fi

# 7. Check bundle size
echo ""
echo "7️⃣  Checking bundle size..."
DIST_SIZE=$(du -sh dist | cut -f1)
echo "📦 Bundle size: $DIST_SIZE"

# 8. Count files
FILE_COUNT=$(find dist -type f | wc -l)
echo "📄 Total files: $FILE_COUNT"

echo ""
echo "✅ All pre-deployment tests passed!"
echo ""
echo "📋 Summary:"
echo "  - Build: ✅ Success"
echo "  - Critical files: ✅ Present"
echo "  - Bundle size: $DIST_SIZE"
echo "  - Total files: $FILE_COUNT"
echo ""
echo "🚀 Ready to deploy!"
