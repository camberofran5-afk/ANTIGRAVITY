#!/bin/bash
# Post-Deployment Test Script
# Run this after deployment to verify the app is working

set -e

# Configuration
URL="${1:-https://leafy-florentine-759293.netlify.app}"

echo "🧪 Testing deployed app at $URL..."
echo ""

# 1. Check if site is reachable
echo "1️⃣  Checking site accessibility..."
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" "$URL")
if [ $HTTP_CODE -ne 200 ]; then
    echo "❌ Site returned HTTP $HTTP_CODE (expected 200)"
    exit 1
fi
echo "✅ Site is accessible (HTTP 200)"

# 2. Check HTTPS
echo ""
echo "2️⃣  Verifying HTTPS..."
if [[ $URL != https://* ]]; then
    echo "❌ Site not using HTTPS"
    exit 1
fi
echo "✅ HTTPS enabled"

# 3. Check for critical content
echo ""
echo "3️⃣  Checking app content..."
CONTENT=$(curl -s "$URL")

if [[ $CONTENT != *"ERP Ganadero"* ]]; then
    echo "❌ App title not found in HTML"
    exit 1
fi
echo "✅ App title found"

if [[ $CONTENT != *"root"* ]]; then
    echo "❌ React root element not found"
    exit 1
fi
echo "✅ React root element found"

# 4. Check for JavaScript bundle
echo ""
echo "4️⃣  Checking JavaScript bundle..."
if [[ $CONTENT != *".js"* ]]; then
    echo "❌ JavaScript bundle not found"
    exit 1
fi
echo "✅ JavaScript bundle loaded"

# 5. Check for CSS
echo ""
echo "5️⃣  Checking CSS..."
if [[ $CONTENT != *".css"* ]] && [[ $CONTENT != *"<style"* ]]; then
    echo "⚠️  Warning: No CSS found (app may not be styled)"
else
    echo "✅ CSS found"
fi

# 6. Check response time
echo ""
echo "6️⃣  Measuring response time..."
RESPONSE_TIME=$(curl -s -o /dev/null -w "%{time_total}" "$URL")
echo "⏱️  Response time: ${RESPONSE_TIME}s"

if (( $(echo "$RESPONSE_TIME > 3.0" | bc -l) )); then
    echo "⚠️  Warning: Response time >3s (may be slow on mobile)"
else
    echo "✅ Response time acceptable"
fi

# 7. Check for common errors
echo ""
echo "7️⃣  Checking for errors..."
if [[ $CONTENT == *"404"* ]] || [[ $CONTENT == *"Not Found"* ]]; then
    echo "❌ 404 error detected"
    exit 1
fi

if [[ $CONTENT == *"500"* ]] || [[ $CONTENT == *"Internal Server Error"* ]]; then
    echo "❌ 500 error detected"
    exit 1
fi
echo "✅ No errors detected"

echo ""
echo "✅ All post-deployment tests passed!"
echo ""
echo "📋 Summary:"
echo "  - Accessibility: ✅ HTTP 200"
echo "  - Security: ✅ HTTPS"
echo "  - Content: ✅ App loaded"
echo "  - Performance: ⏱️  ${RESPONSE_TIME}s"
echo ""
echo "🌐 App is live at $URL"
echo ""
echo "📱 Next steps:"
echo "  1. Test on mobile device"
echo "  2. Verify PWA installation"
echo "  3. Test offline mode"
echo "  4. Share with beta users"
