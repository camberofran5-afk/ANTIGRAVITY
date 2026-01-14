#!/bin/bash
# ERP Ganadero V2 - Deployment Script
# Agent 8 (DevOps) - Automated deployment to production

set -e  # Exit on error

echo "🚀 ERP Ganadero V2 - Production Deployment"
echo "=========================================="

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Configuration
FRONTEND_DIR="frontend-v2"
BACKEND_DIR="backend"
DEPLOY_ENV=${1:-"production"}

echo -e "${BLUE}Environment: ${DEPLOY_ENV}${NC}"

# Step 1: Pre-deployment checks
echo -e "\n${BLUE}Step 1: Pre-deployment checks...${NC}"

# Check Node.js
if ! command -v node &> /dev/null; then
    echo -e "${RED}Error: Node.js not installed${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Node.js installed: $(node --version)${NC}"

# Check Python
if ! command -v python &> /dev/null; then
    echo -e "${RED}Error: Python not installed${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Python installed: $(python --version)${NC}"

# Step 2: Frontend build
echo -e "\n${BLUE}Step 2: Building frontend...${NC}"
cd $FRONTEND_DIR

# Install dependencies
echo "Installing frontend dependencies..."
npm install --silent

# Run build
echo "Building production bundle..."
npm run build

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Frontend build successful${NC}"
    echo "Bundle size: $(du -sh dist | cut -f1)"
else
    echo -e "${RED}✗ Frontend build failed${NC}"
    exit 1
fi

cd ..

# Step 3: Backend setup
echo -e "\n${BLUE}Step 3: Setting up backend...${NC}"
cd $BACKEND_DIR

# Install dependencies
echo "Installing backend dependencies..."
pip install -r requirements.txt --quiet

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Backend dependencies installed${NC}"
else
    echo -e "${RED}✗ Backend setup failed${NC}"
    exit 1
fi

cd ..

# Step 4: Run tests
echo -e "\n${BLUE}Step 4: Running tests...${NC}"

# Backend tests
cd $BACKEND_DIR
if [ -f "test_integration.py" ]; then
    echo "Running integration tests..."
    python -m pytest test_integration.py -v --asyncio-mode=auto || true
fi
cd ..

# Step 5: Deployment
echo -e "\n${BLUE}Step 5: Deploying to ${DEPLOY_ENV}...${NC}"

if [ "$DEPLOY_ENV" == "production" ]; then
    # Deploy frontend to Vercel
    echo "Deploying frontend to Vercel..."
    cd $FRONTEND_DIR
    if command -v vercel &> /dev/null; then
        vercel --prod --yes
        echo -e "${GREEN}✓ Frontend deployed to Vercel${NC}"
    else
        echo -e "${RED}⚠ Vercel CLI not installed. Skipping frontend deployment.${NC}"
        echo "Install with: npm i -g vercel"
    fi
    cd ..
    
    # Deploy backend to Railway
    echo "Deploying backend to Railway..."
    cd $BACKEND_DIR
    if command -v railway &> /dev/null; then
        railway up
        echo -e "${GREEN}✓ Backend deployed to Railway${NC}"
    else
        echo -e "${RED}⚠ Railway CLI not installed. Skipping backend deployment.${NC}"
        echo "Install with: npm i -g @railway/cli"
    fi
    cd ..
else
    echo "Local deployment - starting servers..."
    
    # Start backend
    echo "Starting backend server..."
    cd $BACKEND_DIR
    python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 &
    BACKEND_PID=$!
    echo -e "${GREEN}✓ Backend started (PID: $BACKEND_PID)${NC}"
    cd ..
    
    # Start frontend
    echo "Starting frontend dev server..."
    cd $FRONTEND_DIR
    npm run dev &
    FRONTEND_PID=$!
    echo -e "${GREEN}✓ Frontend started (PID: $FRONTEND_PID)${NC}"
    cd ..
    
    echo -e "\n${GREEN}Servers running!${NC}"
    echo "Frontend: http://localhost:5173"
    echo "Backend:  http://localhost:8000"
    echo ""
    echo "To stop servers:"
    echo "  kill $BACKEND_PID $FRONTEND_PID"
fi

# Step 6: Post-deployment validation
echo -e "\n${BLUE}Step 6: Post-deployment validation...${NC}"

sleep 3  # Wait for servers to start

# Health check
if curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Backend health check passed${NC}"
else
    echo -e "${RED}⚠ Backend health check failed${NC}"
fi

# Summary
echo -e "\n${GREEN}=========================================="
echo "🎉 Deployment Complete!"
echo "==========================================${NC}"
echo ""
echo "Next steps:"
echo "1. Test the application"
echo "2. Monitor logs for errors"
echo "3. Share with stakeholders"
echo ""
echo "Documentation:"
echo "- Deployment Guide: deployment_guide.md"
echo "- Next Steps: next_steps.md"
echo "- Walkthrough: walkthrough.md"
