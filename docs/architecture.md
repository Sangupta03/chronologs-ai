# ChronoLogs AI  
## System Architecture Document

---

## 1. Architecture Overview

ChronoLogs AI follows a modular, service-oriented architecture with clear separation of concerns between:

- Frontend (Presentation Layer)
- Backend API (Application Layer)
- Service Layer (Business Logic)
- ML Processing Layer
- AI Narrative Layer
- Database (Persistence Layer)

The system is designed to be:

- Scalable
- Maintainable
- Deployment-ready
- Extensible for future distributed processing

---

## 2. High-Level Architecture Diagram
            ┌─────────────────────────┐
            │        Frontend         │
            │  (React + Tailwind UI)  │
            └────────────┬────────────┘
                         │
                         ▼
            ┌─────────────────────────┐
            │     Django REST API     │
            │  Authentication Layer   │
            └────────────┬────────────┘
                         │
                         ▼
            ┌─────────────────────────┐
            │      Service Layer      │
            │ ─ Log Parser Service    │
            │ ─ ML Clustering Service │
            │ ─ Anomaly Detection     │
            │ ─ Timeline Builder      │
            │ ─ AI Story Generator    │
            └────────────┬────────────┘
                         │
                         ▼
            ┌─────────────────────────┐
            │      PostgreSQL DB      │
            │  Users / Logs / Reports │
            └─────────────────────────┘

---

## 3. Architectural Layers

### 3.1 Frontend Layer

Technology:
- React
- Tailwind CSS
- Chart.js

Responsibilities:
- Authentication UI
- Log upload interface
- Incident dashboard
- Story viewer
- Analytics visualization

The frontend communicates only with the Django REST API via HTTP.

It does NOT contain ML or business logic.

---

### 3.2 Backend API Layer (Django REST Framework)

Responsibilities:
- Authentication (JWT)
- File upload handling
- API endpoints
- Request validation
- Response formatting
- Orchestrating service calls

The API layer should remain thin and delegate processing to the service layer.

---

### 3.3 Service Layer (Core Business Logic)

The service layer isolates core logic from views and serializers.

Key services:

- LogParserService
- ClusteringService
- AnomalyDetectionService
- TimelineService
- StoryGenerationService

Benefits:
- Clean separation of concerns
- Easier unit testing
- Reusable processing logic
- Scalable to async tasks later

---

### 3.4 ML Processing Layer

This layer handles incident detection using unsupervised learning.

Pipeline:

1. Text normalization
2. Tokenization
3. TF-IDF vectorization
4. KMeans clustering
5. Isolation Forest anomaly detection
6. Incident grouping
7. Severity scoring

This logic resides inside the service layer but is logically isolated.

No model training server required for MVP.

---

### 3.5 AI Narrative Layer

Responsible for converting structured incident data into:

- Chronological story
- Root cause hypothesis
- Impact analysis
- Recommended actions

This layer:
- Uses structured prompts
- Enforces JSON output format
- Handles LLM failure cases
- Validates response schema

---

### 3.6 Persistence Layer (Database)

Database: PostgreSQL

Core Entities:
- User
- LogFile
- LogEvent
- Incident
- IncidentStory

Design Principles:
- Foreign key integrity
- Indexed timestamps
- Incident-to-log relationships
- User-scoped data access

---

## 4. Data Flow

### 4.1 Log Processing Flow

1. User uploads log file
2. File stored temporarily
3. LogParserService extracts structured events
4. Events stored in database
5. ML pipeline clusters events into incidents
6. Anomaly detection assigns anomaly scores
7. Timeline reconstruction groups incident windows
8. AI Story Generator produces structured narrative
9. IncidentStory stored
10. Frontend retrieves processed results

---

## 5. Deployment Architecture

            ┌─────────────────────────┐
            │        Frontend         │
            │        (Vercel)  │
            └────────────┬────────────┘
                         │
                         ▼
            ┌─────────────────────────┐
            │        Backend          │
            │  (Render / Railway)     │
            └────────────┬────────────┘
                         │
                         ▼
            ┌─────────────────────────┐
            │       PostgresSQL       │
            │      (Managed DB)       │
            └─────────────────────────┘

Docker containers used for:
- Backend
- Frontend

Environment variables used for:
- Secret keys
- DB credentials
- LLM API key

---

## 6. Security Considerations

- JWT authentication
- Environment-based secrets
- File upload validation
- User-scoped database queries
- No direct DB exposure

---

## 7. Scalability Considerations (Future)

The architecture supports future upgrades:

- Celery for async processing
- Redis for task queue
- Vector database for log embeddings
- Streaming log ingestion
- Microservice separation of ML engine

The modular service layer allows extraction into independent services if required.

---

## 8. Design Principles

ChronoLogs AI architecture is built on:

- Separation of concerns
- Modularity
- Clean API contracts
- Extensibility
- Deployment readiness
- Reproducible ML pipeline

This architecture reflects production-grade system thinking rather than a simple demo project.

---

## 9. Summary

ChronoLogs AI is architected as a layered, modular full-stack system integrating:

- RESTful backend services
- Unsupervised ML pipeline
- AI-driven narrative generation
- Structured relational persistence
- Clean frontend visualization

The architecture emphasizes maintainability, clarity, and production discipline.