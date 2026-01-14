# ERP Inteligente para Ganaderos - Estructura de Equipo Multi-Agente

## 🎯 PROYECTO: Sistema ERP para Producción de Becerros (Ganadería Extensiva)

---

## 📋 FASE 0: ANÁLISIS DE TU PROPUESTA INICIAL

### Lo que propusiste:
1. Agente de Design Thinking
2. Agente de Investigación de Mercado
3. Experto en Ganado Extensivo (Producción de Becerros)
4. Agente que captura tus ideas principales
5. Agente de Diseño de Producto
6. Agente de Ingeniería
7. Agente Manejador de Proyecto

### ✅ Fortalezas de tu propuesta:
- Cobertura completa del ciclo de desarrollo
- Incluye expertise de dominio (ganadería)
- Separación clara entre diseño e ingeniería
- Reconoces necesidad de coordinación (project manager)

### ⚠️ Ajustes recomendados:
1. **Combinar roles duplicados**: Design Thinking + Diseño de Producto → Product Designer
2. **Agregar rol faltante**: QA/Testing para validación
3. **Clarificar secuencia**: Definir workflow entre agentes
4. **Especializar por fase**: Discovery → Design → Build → Deploy

---

## 🏗️ ESTRUCTURA PROPUESTA: EQUIPO DE 7 AGENTES

### Organización por Fases del Proyecto

```
DISCOVERY (Investigación)
├─ Agent-Stakeholder (tú + usuarios)
├─ Agent-Market-Research
└─ Agent-Domain-Expert (ganadería)
         ↓
DESIGN (Definición)
├─ Agent-Product-Designer
└─ Agent-System-Architect
         ↓
BUILD (Implementación)
├─ Agent-Engineer
└─ Agent-QA
         ↓
ORCHESTRATION (Coordinación)
└─ Agent-Project-Manager (coordina todo)
```

---

## 👥 DEFINICIÓN DETALLADA DE CADA AGENTE

### **1. Agent-Stakeholder** (Captura de Visión)
**Rol**: Interfaz entre tú (stakeholder) y el equipo  
**Responsabilidad**: Capturar, estructurar y priorizar tus ideas

**Tareas**:
- Entrevistarte para extraer requisitos
- Documentar pain points de ganaderos
- Crear user stories iniciales
- Priorizar features (MoSCoW: Must/Should/Could/Won't)
- Validar que el equipo entiende tu visión

**Input**: Tus ideas en lenguaje natural  
**Output**: Documento de requisitos estructurado (`/directives/erp_requirements.md`)

**Herramientas**:
- Templates de user stories
- Framework de priorización (RICE, MoSCoW)
- Técnicas de entrevista (5 Whys, Jobs-to-be-Done)

**Ejemplo de Output**:
```
USER STORY #1
Como ganadero, quiero registrar nacimientos de becerros en <2 minutos
para mantener inventario actualizado sin interrumpir trabajo de campo

PRIORIDAD: MUST HAVE
CRITERIOS DE ÉXITO:
- Registro desde móvil (sin internet)
- Captura: fecha, madre, peso, sexo
- Sincronización automática cuando hay conexión
```

---

### **2. Agent-Market-Research** (Investigación de Mercado)
**Rol**: Analista de mercado y competencia  
**Responsabilidad**: Validar oportunidad de negocio

**Tareas**:
- Investigar ERPs existentes para ganadería (competidores)
- Analizar precios y modelos de negocio
- Identificar gaps en soluciones actuales
- Estimar tamaño de mercado (ganaderos en México/región)
- Definir propuesta de valor única

**Input**: Requisitos del Agent-Stakeholder  
**Output**: Reporte de mercado (`/directives/market_analysis.md`)

**Herramientas**:
- Web scraping (competidores)
- Análisis SWOT
- Porter's Five Forces
- Encuestas a ganaderos (opcional)

**Ejemplo de Output**:
```
COMPETIDORES IDENTIFICADOS:
1. Ganadero Pro (México) - $50 USD/mes - Web only
2. Cattle Manager (USA) - $100 USD/mes - Complejo
3. Excel/Papel (80% del mercado) - Gratis - Ineficiente

GAP IDENTIFICADO:
- Ninguno tiene modo offline para campo
- Interfaces complejas (no para ganaderos tradicionales)
- Precios altos para pequeños productores

PROPUESTA DE VALOR:
ERP simple, móvil-first, offline-capable, $20 USD/mes
```

---

### **3. Agent-Domain-Expert** (Experto en Ganadería Extensiva)
**Rol**: Consultor especializado en producción de becerros  
**Responsabilidad**: Asegurar que el sistema refleja la realidad del campo

**Tareas**:
- Validar workflows de ganadería (ciclo reproductivo, destete, venta)
- Definir KPIs críticos (tasa de natalidad, peso al destete, mortalidad)
- Especificar reglas de negocio (ej: "becerro se desteta a 6-8 meses")
- Identificar eventos clave a trackear (servicio, parto, vacunación, pesaje)
- Revisar terminología y unidades (kg, arrobas, meses)

**Input**: User stories del Agent-Stakeholder  
**Output**: Modelo de dominio (`/directives/domain_model.md`)

**Herramientas**:
- Conocimiento de ganadería (puede ser LLM con RAG de manuales)
- Diagramas de ciclo de vida del ganado
- Benchmarks de la industria

**Ejemplo de Output**:
```
CICLO DE VIDA - PRODUCCIÓN DE BECERROS:

1. VACA ADULTA (2+ años)
   → Servicio (monta o inseminación)
   → Gestación (9 meses)
   → Parto
   
2. BECERRO (0-8 meses)
   → Nacimiento (registro peso, sexo, madre)
   → Lactancia (6-8 meses con madre)
   → Vacunaciones (calendario)
   → Destete (separación de madre)
   → Venta o retención

KPIs CRÍTICOS:
- Tasa de natalidad: >85% (becerros nacidos / vacas servidas)
- Mortalidad: <5% (becerros muertos / nacidos)
- Peso al destete: >180 kg a 7 meses
- Intervalo entre partos: <13 meses
```

---

### **4. Agent-Product-Designer** (Diseñador de Producto)
**Rol**: UX/UI + Product Strategy  
**Responsabilidad**: Diseñar la experiencia del usuario

**Tareas**:
- Crear user flows (cómo ganadero usa el sistema)
- Diseñar wireframes/mockups de interfaces
- Aplicar Design Thinking (empatía, ideación, prototipado)
- Definir arquitectura de información
- Priorizar features para MVP vs. roadmap futuro

**Input**: Requisitos + Market Research + Domain Model  
**Output**: Diseño de producto (`/directives/product_design.md`)

**Herramientas**:
- Design Thinking framework
- User journey mapping
- Wireframing (texto o herramientas)
- Priorización de features (Kano Model)

**Ejemplo de Output**:
```
MVP (Versión 1.0) - 3 MESES:
✅ Registro de ganado (vacas, becerros)
✅ Registro de eventos (nacimientos, muertes, ventas)
✅ Dashboard simple (inventario actual, KPIs básicos)
✅ Modo offline (sincronización automática)
✅ App móvil (iOS/Android)

ROADMAP FUTURO:
📅 V1.1 (Mes 4-6): Gestión de vacunaciones, calendario
📅 V1.2 (Mes 7-9): Reportes financieros, costos
📅 V2.0 (Mes 10-12): IA predictiva (mejor época de venta)

USER FLOW PRINCIPAL:
1. Ganadero abre app en campo (sin internet)
2. Toca "Registrar Nacimiento"
3. Escanea tag de madre (QR/NFC) o busca por número
4. Ingresa: fecha, peso, sexo
5. Toma foto (opcional)
6. Guarda → Se sincroniza cuando hay WiFi
```

---

### **5. Agent-System-Architect** (Arquitecto de Sistema)
**Rol**: Diseñador técnico  
**Responsabilidad**: Definir arquitectura técnica del ERP

**Tareas**:
- Mapear features a 4-Layer Hierarchy (L1→L2→L3→L4)
- Diseñar modelo de datos (tablas Supabase)
- Definir APIs y endpoints
- Especificar stack tecnológico
- Planificar escalabilidad y seguridad

**Input**: Diseño de producto  
**Output**: Arquitectura técnica (`/directives/system_architecture.md`)

**Herramientas**:
- 4-Layer Hierarchy (tu framework)
- Diagramas de arquitectura
- Database schema design
- API design (REST/GraphQL)

**Ejemplo de Output**:
```
STACK TECNOLÓGICO:
- Frontend: React Native (móvil iOS/Android)
- Backend: FastAPI (Python) en Cloud Run
- Database: Supabase (PostgreSQL)
- Offline: SQLite local + sync
- Auth: Supabase Auth
- Storage: Supabase Storage (fotos de ganado)

MODELO DE DATOS (Supabase):

TABLE: cattle
- id (uuid)
- ranch_id (fk)
- tag_number (string, unique)
- type (enum: cow, bull, calf)
- sex (enum: male, female)
- birth_date (date)
- mother_id (fk, nullable)
- status (enum: active, sold, dead)

TABLE: events
- id (uuid)
- cattle_id (fk)
- type (enum: birth, vaccination, weighing, sale, death)
- date (timestamp)
- data (jsonb) // peso, precio, etc.
- created_by (fk user)

TABLE: ranches
- id (uuid)
- owner_id (fk user)
- name (string)
- location (geography)

ARQUITECTURA 4-LAYER:

L1 (Config):
- supabase_client.py
- cattle_types.py (enums, constants)

L2 (Foundation):
- cattle_crud.py (CRUD operations)
- event_logger.py (registrar eventos)
- offline_sync.py (sincronización)

L3 (Analysis):
- kpi_calculator.py (calcular KPIs)
- inventory_manager.py (estado del hato)
- breeding_tracker.py (ciclo reproductivo)

L4 (Synthesis):
- cattle_api.py (FastAPI endpoints)
- dashboard_builder.py (generar dashboards)
```

---

### **6. Agent-Engineer** (Ingeniero de Software)
**Rol**: Desarrollador full-stack  
**Responsabilidad**: Implementar el sistema

**Tareas**:
- Escribir código siguiendo arquitectura definida
- Implementar L1 → L2 → L3 → L4 (bottom-up)
- Crear APIs y endpoints
- Desarrollar app móvil (React Native)
- Implementar sincronización offline
- Integrar con Supabase

**Input**: Arquitectura técnica  
**Output**: Código funcional (`/tools/`, `/apps/`)

**Herramientas**:
- Python (backend)
- React Native (frontend)
- Supabase SDK
- Git (control de versiones)

**Reglas de Implementación**:
- Commits con prefijo `[LAYER]` (ej: `[L2] Add cattle CRUD helpers`)
- Archivos <200 líneas
- Type hints en todo
- Logging estructurado
- Tests unitarios básicos

---

### **7. Agent-QA** (Quality Assurance)
**Rol**: Tester y validador  
**Responsabilidad**: Asegurar calidad del producto

**Tareas**:
- Crear test cases basados en user stories
- Probar funcionalidades (manual y automatizado)
- Validar que cumple requisitos del Agent-Stakeholder
- Verificar usabilidad (¿es simple para ganaderos?)
- Reportar bugs y sugerir mejoras

**Input**: Código del Agent-Engineer  
**Output**: Reporte de QA (`/docs/qa_report.md`)

**Herramientas**:
- pytest (tests automatizados)
- Test cases manuales
- Checklist de Quality Rubric (10 puntos)

**Ejemplo de Test Cases**:
```
TEST CASE #1: Registro de Nacimiento Offline
PASOS:
1. Desactivar WiFi/datos en móvil
2. Abrir app
3. Ir a "Registrar Nacimiento"
4. Ingresar datos: madre #123, peso 35kg, macho
5. Guardar
6. Activar WiFi
7. Esperar sincronización

RESULTADO ESPERADO:
✅ Registro se guarda localmente sin error
✅ Al conectar, se sincroniza a Supabase
✅ Becerro aparece en inventario
✅ KPIs se actualizan automáticamente
```

---

### **8. Agent-Project-Manager** (Coordinador/Orquestador)
**Rol**: Scrum Master + Product Owner  
**Responsabilidad**: Coordinar todo el equipo y asegurar entrega

**Tareas**:
- Crear y mantener roadmap del proyecto
- Coordinar handoffs entre agentes
- Resolver bloqueos y dependencias
- Priorizar trabajo en sprints
- Reportar progreso al stakeholder (tú)
- Asegurar que se sigue el workflow correcto

**Input**: Todos los agentes  
**Output**: Plan de proyecto (`/directives/project_plan.md`)

**Herramientas**:
- Gantt chart o timeline
- Task tracking (task.md)
- Daily standups (simulados)
- Sprint planning

**Ejemplo de Coordinación**:
```
SPRINT 1 (Semana 1-2): DISCOVERY
- Agent-Stakeholder: Capturar requisitos
- Agent-Market-Research: Analizar competencia
- Agent-Domain-Expert: Definir modelo de dominio
→ ENTREGABLE: Directivas completas

SPRINT 2 (Semana 3-4): DESIGN
- Agent-Product-Designer: Diseñar MVP y user flows
- Agent-System-Architect: Definir arquitectura técnica
→ ENTREGABLE: Specs de diseño y arquitectura

SPRINT 3-6 (Semana 5-12): BUILD
- Agent-Engineer: Implementar L1→L2→L3→L4
- Agent-QA: Testing continuo
→ ENTREGABLE: MVP funcional

SPRINT 7 (Semana 13): DEPLOY
- Agent-Engineer: Deploy a producción
- Agent-QA: Testing final
- Agent-Project-Manager: Documentación y handoff
→ ENTREGABLE: ERP en producción
```

---

## 🔄 WORKFLOW ENTRE AGENTES

### Secuencia Ideal (Waterfall Ágil):

```
1. KICKOFF
   Agent-Project-Manager define timeline
   ↓

2. DISCOVERY (Paralelo)
   Agent-Stakeholder ←→ Tú (entrevistas)
   Agent-Market-Research → Investigación
   Agent-Domain-Expert → Modelo de dominio
   ↓
   CHECKPOINT: Revisión de directivas
   ↓

3. DESIGN (Secuencial)
   Agent-Product-Designer (usa output de Discovery)
   ↓
   Agent-System-Architect (usa output de Product Designer)
   ↓
   CHECKPOINT: Revisión de diseño
   ↓

4. BUILD (Iterativo)
   Agent-Engineer implementa
   ↓
   Agent-QA prueba
   ↓
   ¿Bugs? → Agent-Engineer corrige
   ↓
   CHECKPOINT: Demo semanal
   ↓

5. DEPLOY
   Agent-Engineer despliega
   Agent-QA valida en producción
   Agent-Project-Manager documenta
   ↓
   ENTREGA FINAL
```

---

## 📊 MATRIZ DE RESPONSABILIDADES (RACI)

| Actividad | Stakeholder | Market | Domain | Product | Architect | Engineer | QA | PM |
|-----------|-------------|--------|--------|---------|-----------|----------|----|----|
| Definir visión | **R** | C | C | I | I | I | I | **A** |
| Investigar mercado | C | **R** | I | C | I | I | I | **A** |
| Validar workflows ganadería | C | I | **R** | C | C | I | I | **A** |
| Diseñar UX/UI | C | I | C | **R** | C | I | I | **A** |
| Definir arquitectura | I | I | C | C | **R** | C | I | **A** |
| Escribir código | I | I | I | I | C | **R** | C | **A** |
| Testing | I | I | I | I | I | C | **R** | **A** |
| Coordinar equipo | C | I | I | I | I | I | I | **R/A** |

**Leyenda**:
- **R** = Responsible (hace el trabajo)
- **A** = Accountable (aprueba/decide)
- **C** = Consulted (se le consulta)
- **I** = Informed (se le informa)

---

## 🎯 AJUSTES FINALES A TU PROPUESTA ORIGINAL

### Cambios realizados:

1. ✅ **Combiné**: "Design Thinking" + "Diseño de Producto" → **Agent-Product-Designer**
   - Razón: Design Thinking es metodología, no rol separado

2. ✅ **Agregué**: **Agent-System-Architect**
   - Razón: Necesitas puente entre diseño y código (arquitectura técnica)

3. ✅ **Agregué**: **Agent-QA**
   - Razón: Testing es crítico para calidad

4. ✅ **Renombré**: "Agente que captura ideas" → **Agent-Stakeholder**
   - Razón: Nombre más profesional y claro

5. ✅ **Mantuve**: Market Research, Domain Expert, Engineer, Project Manager
   - Razón: Roles bien definidos desde el inicio

### Resultado: 8 Agentes Especializados

**Discovery**: Stakeholder, Market Research, Domain Expert  
**Design**: Product Designer, System Architect  
**Build**: Engineer, QA  
**Orchestration**: Project Manager

---

## 📋 PRÓXIMOS PASOS

### Opción A: Empezar Discovery
1. Agent-Stakeholder te entrevista (yo simulo el agente)
2. Capturo tus requisitos detallados
3. Creo `/directives/erp_requirements.md`

### Opción B: Simular todo el equipo
1. Ejecuto todo el workflow (Discovery → Design → Build)
2. Genero todos los documentos de directivas
3. Implemento MVP del ERP

### Opción C: Enfoque híbrido
1. Haces Discovery manualmente (tú defines requisitos)
2. Yo ejecuto Design + Build con los agentes

**¿Qué prefieres?** 🎯
