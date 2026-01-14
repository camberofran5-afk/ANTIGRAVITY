# Workflow Ideal para Crear Apps con Antigravity

## 📋 TU SETUP ACTUAL (Inventario)

### ✅ Infraestructura Existente
- **Database**: Supabase (configurado en `L1_config/supabase_client.py`)
- **LLMs**: Gemini + OpenAI (configurado en `L1_config/llm_client.py`)
- **Agent Frameworks**: Agno (Phidata) + OpenManus (Playwright)
- **MCP**: Cliente y servidor implementados (`execution/mcp_client.py`, `execution/mcp_server.py`)
- **Logging**: Structlog configurado (`L1_config/logging_config.py`)
- **Architecture**: 4-Layer Hierarchy (L1→L2→L3→L4)
- **Multi-Agent**: Roles definidos en `agents.md` (DB, AI, API, QA)

### ✅ Herramientas Disponibles
```
L1_config/          → Configuración centralizada
L2_foundation/      → Helpers de base (5 archivos)
L3_analysis/        → Lógica de negocio (2 archivos)
L4_synthesis/       → Orquestación (5 archivos)
execution/          → MCP client/server
```

---

## 🎯 WORKFLOW IDEAL: 5 FASES

### **FASE 1: DEFINIR (Directiva)**
**Objetivo**: Especificar QUÉ vas a construir  
**Duración**: 30-60 minutos  
**Output**: Documento de especificación

#### Pasos:
1. **Crear directiva en `/directives/`**
   - Nombre: `app_[nombre]_spec.md`
   - Contenido:
     - Problema que resuelve
     - Usuarios objetivo
     - Funcionalidades core (máximo 5)
     - Flujos de usuario (diagramas de texto)
     - Modelo de datos (tablas Supabase)
     - APIs necesarias (endpoints)

2. **Validar con Quality Rubric**
   - ¿Es horizontal leverage? (escala a 10,000 instancias)
   - ¿Tiene data hygiene clara?
   - ¿Respeta 4-layer hierarchy?

**Ejemplo**:
```markdown
# App: AI Research Assistant

## Problema
Investigadores pierden 3 horas/día buscando papers relevantes

## Funcionalidades Core
1. Búsqueda semántica de papers
2. Resumen automático con LLM
3. Organización en colecciones
4. Alertas de nuevos papers

## Modelo de Datos
- users (id, email, preferences)
- papers (id, title, abstract, embedding)
- collections (id, user_id, name)
- alerts (id, user_id, query, frequency)
```

---

### **FASE 2: DISEÑAR (Arquitectura)**
**Objetivo**: Mapear CÓMO se construye con 4-Layer Hierarchy  
**Duración**: 1-2 horas  
**Output**: Plan de implementación por capas

#### Pasos:
1. **Mapear a las 4 capas**
   ```
   L1: Configs (API keys, constantes, tipos)
   L2: Helpers (Supabase queries, LLM calls, validación)
   L3: Business Logic (búsqueda semántica, scoring)
   L4: API/Orchestration (endpoints FastAPI, workflows)
   ```

2. **Identificar agentes necesarios**
   - ¿Necesitas Agent-Database? (modelos Supabase)
   - ¿Necesitas Agent-AI? (embeddings, LLM)
   - ¿Necesitas Agent-API? (endpoints, integraciones)

3. **Definir flujo de datos**
   ```
   Usuario → L4 API → L3 Logic → L2 Helpers → L1 Config
                                    ↓
                                 Supabase
   ```

4. **Crear checklist en `/directives/app_[nombre]_plan.md`**

**Ejemplo**:
```markdown
# Plan: AI Research Assistant

## L1 (Config)
- [ ] `research_config.py`: API keys (Semantic Scholar, arXiv)
- [ ] `types.py`: Paper, Collection, Alert models

## L2 (Foundation)
- [ ] `paper_fetcher.py`: Fetch papers from APIs
- [ ] `embedding_generator.py`: Generate embeddings con Gemini
- [ ] `supabase_papers.py`: CRUD operations

## L3 (Analysis)
- [ ] `semantic_search.py`: Búsqueda por similitud
- [ ] `summarizer.py`: Resumen con LLM
- [ ] `relevance_scorer.py`: Score papers

## L4 (Synthesis)
- [ ] `research_api.py`: FastAPI endpoints
- [ ] `alert_workflow.py`: Workflow de alertas
```

---

### **FASE 3: CONSTRUIR (Implementación)**
**Objetivo**: Escribir código siguiendo el plan  
**Duración**: Variable (2-10 horas dependiendo complejidad)  
**Output**: Código funcional en `/tools/`

#### Pasos:
1. **Empezar por L1 (abajo hacia arriba)**
   - Crear configs y tipos primero
   - Sin dependencias externas

2. **Continuar con L2**
   - Helpers atómicos (una función = una responsabilidad)
   - Máximo 200 líneas por archivo
   - Solo depende de L1

3. **Implementar L3**
   - Lógica de negocio
   - Combina múltiples L2 helpers
   - Solo depende de L1 + L2

4. **Finalizar con L4**
   - API endpoints o workflows
   - Orquesta L3 logic
   - Depende de L1 + L2 + L3

5. **Usar multi-agent si es complejo**
   - Agent-Database: L1 config + L2 database helpers
   - Agent-AI: L2 LLM helpers + L3 AI logic
   - Agent-API: L4 synthesis

**Reglas**:
- ✅ Commits frecuentes con prefijo `[LAYER]`
- ✅ Logging estructurado en cada función
- ✅ Type hints en todo
- ✅ Docstrings con ejemplos
- ❌ No circular dependencies
- ❌ No magic numbers
- ❌ No archivos >200 líneas

---

### **FASE 4: INTEGRAR (Orquestación)**
**Objetivo**: Conectar todo con workflows o API  
**Duración**: 1-2 horas  
**Output**: App funcional end-to-end

#### Opción A: API App (Always-On Service)
```markdown
## Estructura
/apps/research_assistant/
├── main.py              # FastAPI app
├── routers/
│   ├── papers.py        # Paper endpoints
│   ├── collections.py   # Collection endpoints
│   └── alerts.py        # Alert endpoints
├── dependencies.py      # DI (Supabase, LLM clients)
└── Dockerfile           # Container config
```

#### Opción B: Workflow App (Task-Based)
```markdown
## Estructura
/workflows/research_workflow.yaml
name: daily_paper_digest
steps:
  - fetch_new_papers
  - generate_embeddings
  - find_relevant
  - summarize
  - send_email
```

#### Pasos:
1. **Crear entry point en `/apps/` o `/workflows/`**
2. **Configurar dependencias** (Supabase client, LLM client)
3. **Implementar endpoints/steps** usando L4 synthesis
4. **Agregar error handling** (retry, circuit breakers)
5. **Configurar logging** (structlog con execution_id)

---

### **FASE 5: DESPLEGAR (Production)**
**Objetivo**: Poner app en producción  
**Duración**: 1-2 horas  
**Output**: App desplegada y monitoreada

#### Pasos:
1. **Preparar para deploy**
   ```markdown
   - [ ] Crear Dockerfile
   - [ ] Configurar .env para producción
   - [ ] Crear requirements.txt específico
   - [ ] Agregar health check endpoint
   ```

2. **Elegir hosting según tipo de app**
   
   **API App** → Google Cloud Run
   ```bash
   # Build
   docker build -t research-assistant .
   
   # Deploy
   gcloud run deploy research-assistant \
     --source . \
     --region us-central1 \
     --allow-unauthenticated
   ```
   
   **Workflow App** → Cloud Functions + Cloud Scheduler
   ```bash
   # Deploy function
   gcloud functions deploy daily_digest \
     --runtime python311 \
     --trigger-http
   
   # Schedule
   gcloud scheduler jobs create http daily-digest-job \
     --schedule="0 9 * * *" \
     --uri="https://..."
   ```

3. **Configurar monitoreo**
   - Supabase Dashboard: Queries, RLS
   - Cloud Monitoring: Logs, métricas
   - Structlog: Trazabilidad por execution_id

4. **Documentar en `/docs/`**
   - Deployment guide
   - API documentation
   - Troubleshooting

---

## 🎨 PATRONES RECOMENDADOS CON TU SETUP

### Patrón 1: CRUD App con Supabase
**Cuándo usar**: Apps con datos estructurados (dashboards, admin panels)

**Stack**:
- L1: Supabase client config
- L2: CRUD helpers por tabla
- L3: Business rules (validación, permisos)
- L4: FastAPI endpoints

**Ejemplo**: Task manager, CRM, inventory system

---

### Patrón 2: AI-Powered App con LLM
**Cuándo usar**: Apps que procesan texto/datos con IA

**Stack**:
- L1: LLM client config (Gemini)
- L2: Prompt templates, embedding helpers
- L3: AI logic (summarize, classify, extract)
- L4: API o workflow

**Ejemplo**: Content generator, chatbot, document analyzer

---

### Patrón 3: Multi-Agent Workflow
**Cuándo usar**: Tareas complejas que requieren especialización

**Stack**:
- L1: Agent configs
- L2: MCP client (tools)
- L3: Agent logic por rol
- L4: Workflow orchestration (Agno + OpenManus)

**Ejemplo**: Research assistant, code reviewer, data pipeline

---

### Patrón 4: Hybrid (API + Workflows)
**Cuándo usar**: Apps con UI + background jobs

**Stack**:
- L4 API: FastAPI para UI
- L4 Workflows: Background tasks (Celery/Cloud Tasks)
- L3: Shared business logic
- L2: Shared helpers
- L1: Shared config

**Ejemplo**: Email marketing platform, analytics dashboard

---

## 📊 DECISION TREE: ¿Qué Tipo de App Construir?

```
¿Necesitas UI interactiva?
├─ SÍ → API App (FastAPI + Frontend)
│   └─ ¿Datos estructurados?
│       ├─ SÍ → Patrón 1 (CRUD)
│       └─ NO → Patrón 2 (AI-Powered)
│
└─ NO → Workflow App
    └─ ¿Tarea única o recurrente?
        ├─ Única → Cloud Function
        └─ Recurrente → Cloud Scheduler + Workflow
```

---

## 🚀 QUICK START: Tu Primer App (30 min)

### App Sugerida: "Daily AI News Digest"
**Tipo**: Workflow App  
**Complejidad**: Baja  
**Stack**: L2 (LLM) + L3 (summarize) + L4 (workflow)

**Workflow**:
1. Fetch latest AI news (API)
2. Summarize con Gemini
3. Store en Supabase
4. Send email digest

**Archivos a crear**:
```
/directives/daily_digest_spec.md       # FASE 1
/directives/daily_digest_plan.md       # FASE 2
/tools/L2_foundation/news_fetcher.py   # FASE 3
/tools/L3_analysis/news_summarizer.py  # FASE 3
/workflows/daily_digest.yaml           # FASE 4
```

**Deploy**: Cloud Function + Cloud Scheduler

---

## ✅ CHECKLIST FINAL

Antes de considerar tu app "completa":

### Funcionalidad
- [ ] Todas las features core funcionan
- [ ] Error handling implementado
- [ ] Logging estructurado en todas las funciones
- [ ] Type hints en todo el código

### Arquitectura
- [ ] Respeta 4-layer hierarchy
- [ ] Sin circular dependencies
- [ ] Archivos <200 líneas
- [ ] Configs centralizadas en L1

### Calidad
- [ ] Tests básicos (pytest)
- [ ] Documentación en `/docs/`
- [ ] README con setup instructions
- [ ] .env.example actualizado

### Producción
- [ ] Dockerfile creado
- [ ] Health check endpoint
- [ ] Monitoreo configurado
- [ ] Desplegado y accesible

---

## 🎯 PRÓXIMOS PASOS

**Opción 1**: Crear tu primera app siguiendo el Quick Start
**Opción 2**: Definir una app específica que necesites
**Opción 3**: Implementar los componentes faltantes de producción (Workflow Engine, State Manager, etc.)

**¿Qué prefieres hacer primero?**
