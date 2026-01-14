# ERP Ganadero V2 - Production README

**Version**: 2.0.0  
**Status**: Production Ready ✅  
**Last Updated**: 2026-01-13

---

## 🚀 Quick Start

### Local Development
```bash
# One-command deployment
./deploy.sh local

# Or manually:
# Terminal 1 - Backend
cd backend && python -m uvicorn app.main:app --reload

# Terminal 2 - Frontend  
cd frontend-v2 && npm run dev
```

Open: `http://localhost:5173`

---

## 📦 What's Included

### Features
- ✅ **Reports Module** - 4 report types with PDF generation
- ✅ **Inventory Management** - Track feed, medicine, vaccines, equipment
- ✅ **Client Management** - Manage buyers and suppliers
- ✅ **Cost Tracking** - Monitor expenses by category
- ✅ **Events System** - Track all ranch activities
- ✅ **Mobile Responsive** - Works on all devices

### Technical Stack
- **Frontend**: React + TypeScript + Vite
- **Backend**: FastAPI + Python 3.8+
- **PDF**: jsPDF + jspdf-autotable
- **Storage**: In-memory (demo) / Supabase (production)

---

## 🧪 Testing

### Run Integration Tests
```bash
cd backend
python -m pytest test_integration.py -v
```

### Manual Testing
1. Start servers (see Quick Start)
2. Navigate to Reports: `http://localhost:5173`
3. Create test data (see deployment_guide.md)
4. Download PDFs for each report type

---

## 🚀 Production Deployment

### Automated Deployment
```bash
# Deploy to production (Vercel + Railway)
./deploy.sh production
```

### Manual Deployment

**Frontend (Vercel)**:
```bash
cd frontend-v2
npm run build
vercel --prod
```

**Backend (Railway)**:
```bash
cd backend
railway up
```

See `deployment_guide.md` for detailed instructions.

---

## 📊 API Endpoints

### Base URL
- Local: `http://localhost:8000/api/v1`
- Production: `https://your-backend.com/api/v1`

### Endpoints
- `GET /events?ranch_id={id}` - List events
- `GET /inventory?ranch_id={id}` - List inventory
- `GET /clients?ranch_id={id}` - List clients
- `GET /costs?ranch_id={id}` - List costs
- `POST /inventory` - Create inventory item
- `POST /clients` - Create client
- `POST /costs` - Create cost

Full API docs: `http://localhost:8000/docs`

---

## 🎯 Project Structure

```
erp_ganadero/
├── frontend-v2/          # React frontend
│   ├── src/
│   │   ├── components/   # React components
│   │   ├── services/     # API client
│   │   └── utils/        # Helpers
│   └── dist/             # Production build
├── backend/              # FastAPI backend
│   ├── app/
│   │   ├── L1_config/    # Configuration
│   │   ├── L2_foundation/# CRUD operations
│   │   └── main.py       # FastAPI app
│   └── test_integration.py
└── deploy.sh             # Deployment script
```

---

## 📝 Documentation

- **Deployment Guide**: `deployment_guide.md`
- **Next Steps**: `next_steps.md`
- **Walkthrough**: `walkthrough.md`
- **Sprint Plan**: `sprint_plan.md`

---

## ✅ Completed Features (Phase 5)

- [x] Build error fixes (0 TypeScript errors)
- [x] Events API with ranch filtering
- [x] Inventory API (full CRUD)
- [x] Clients API (full CRUD)
- [x] Costs API with date filtering
- [x] Reports module integration
- [x] Mobile responsive design
- [x] UI polish and animations
- [x] Integration test suite
- [x] Deployment automation

**Story Points**: 35/48 (73% - Core features complete)

---

## 🚨 Troubleshooting

### Backend won't start
```bash
cd backend
pip install -r requirements.txt --force-reinstall
python -m uvicorn app.main:app --reload
```

### Frontend build fails
```bash
cd frontend-v2
rm -rf node_modules dist
npm install
npm run build
```

### CORS errors
Already configured in `backend/app/main.py`:
```python
allow_origins=["*"]  # Development
# Change to specific domain for production
```

---

## 📞 Support

- **Issues**: Create GitHub issue
- **Documentation**: See `/docs` folder
- **Team**: Multi-agent autonomous development

---

## 🎉 Credits

**Developed by**: Multi-Agent Team
- Agent 1: Frontend (React/TypeScript)
- Agent 2: Backend (FastAPI/Python)
- Agent 5: Integration
- Agent 7: QA/Testing
- Agent 8: DevOps

**Methodology**: Agile/Scrum with autonomous execution

---

**Ready to use!** 🚀
