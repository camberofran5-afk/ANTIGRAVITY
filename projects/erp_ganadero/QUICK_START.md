# ERP Ganadero - Quick Reference

## 📁 Project Location
`/Users/franciscocambero/Anitgravity/projects/erp_ganadero/`

## 📂 Folder Structure

```
erp_ganadero/
├── README.md                    # This file - project overview
├── directives/                  # Specs & plans (Markdown only)
│   └── team_structure.md       # 8-agent team definition ✅
├── resources/                   # Research materials
│   ├── market_research/        # Competitor analysis, reports
│   ├── domain_knowledge/       # Cattle ranching manuals, KPIs
│   ├── user_interviews/        # Interview transcripts, personas
│   ├── competitors/            # Screenshots, features, pricing
│   └── references/             # Articles, videos, images
├── docs/                        # Documentation
├── prototypes/                  # Wireframes, mockups
└── data/                        # Sample data, schemas
```

## 🎯 How to Add Resources

### Add market research:
```bash
cd /Users/franciscocambero/Anitgravity/projects/erp_ganadero
cp ~/Downloads/competitor_analysis.pdf resources/market_research/
```

### Add domain knowledge:
```bash
nano resources/domain_knowledge/cattle_vaccination_schedule.md
```

### Add user interview:
```bash
nano resources/user_interviews/rancher_interview_001.md
```

## 📋 Next Steps

1. **Discovery Phase**: Add research materials to `/resources/`
2. **Create Directives**: Agent outputs go to `/directives/`
3. **Document**: Keep `/docs/` updated

See main README for full details.
