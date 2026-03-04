# ChronoLogs AI  
## Tech Stack Document

---

## 1. Overview

This document explains the technology choices made for ChronoLogs AI, including backend, frontend, machine learning, AI integration, database, and deployment stack.

The stack is chosen based on:

- Rapid development capability
- Production readiness
- Scalability potential
- Clean architectural separation

---

## 2. Backend Stack

### 2.1 Django

**Why Django?**

- Mature and battle-tested framework
- Strong ORM with PostgreSQL support
- Built-in security features
- Modular app structure
- Industry-recognized in production systems

Django enables clean separation between:

- Models
- Views
- Serializers
- Services
- Settings (dev/prod split)

---

### 2.2 Django REST Framework (DRF)

**Why DRF?**

- RESTful API support
- Built-in serializers and validation
- Authentication support
- Clean API contracts
- Easy integration with frontend

DRF ensures frontend and backend remain loosely coupled.

---

### 2.3 JWT Authentication

**Why JWT?**

- Stateless authentication
- Scalable across services
- Secure token-based access
- Suitable for API-first systems

Used for:
- Login
- Signup
- Protected routes
- User-scoped data access

---

## 3. Database

### PostgreSQL

**Why PostgreSQL?**

- ACID-compliant relational database
- Strong indexing support
- Reliable foreign key integrity
- Widely used in production
- Compatible with Django ORM

Chosen over NoSQL because:

- Structured relationships (User → LogFile → Incident → Story)
- Strong relational modeling required
- Predictable query patterns

---

## 4. Machine Learning Stack

### 4.1 Scikit-learn

**Why Scikit-learn?**

- Lightweight
- Fast prototyping
- No heavy infrastructure required
- Reliable clustering & anomaly detection algorithms

Used for:

- TF-IDF vectorization
- KMeans clustering
- Isolation Forest anomaly detection

---

### 4.2 TF-IDF Vectorization

**Why TF-IDF?**

- Converts log text into numerical features
- Efficient for short textual events
- Simple and interpretable
- No large model downloads required

Used for:
- Semantic similarity
- Log event grouping

---

### 4.3 KMeans Clustering

**Purpose:**

- Group similar log events
- Form incident clusters
- Identify recurring patterns

Why chosen:
- Simple and fast
- Works well with TF-IDF embeddings
- No labeled dataset required

---

### 4.4 Isolation Forest

**Purpose:**

- Detect anomalous log entries
- Assign anomaly scores
- Identify rare events

Why chosen:
- Efficient for unsupervised anomaly detection
- Lightweight and production-friendly

---

## 5. AI Layer

### LLM Integration (OpenAI / Gemini / Equivalent API)

**Purpose:**

- Convert structured log clusters into human-readable incident narratives
- Generate:
  - Summary
  - Timeline explanation
  - Root cause hypothesis
  - Impact assessment
  - Recommendations

Why API-based instead of training custom model?

- Faster development
- Production-ready reliability
- No infrastructure overhead
- Focus on system integration, not model training

Structured JSON responses enforced for consistency.

---

## 6. Frontend Stack

### 6.1 React

**Why React?**

- Component-based architecture
- Large ecosystem
- Recruiter-recognized
- Easy state management
- Clean separation from backend

---

### 6.2 Vite

**Why Vite?**

- Fast build times
- Lightweight dev server
- Modern tooling

---

### 6.3 Tailwind CSS

**Why Tailwind?**

- Utility-first styling
- Clean, modern UI
- Rapid development
- No heavy CSS architecture required

Focus is clean professional UI, not flashy design.

---

### 6.4 Chart.js

**Purpose:**

- Timeline visualization
- Severity heatmap
- Incident distribution charts

Chosen because:
- Lightweight
- Easy integration with React
- Good enough for MVP dashboards

---

## 7. Containerization

### Docker

**Why Docker?**

- Environment consistency
- Easy deployment
- Separation of dev and prod environments
- Recruiter-recognized production discipline

Used for:
- Backend container
- Frontend container
- Optional docker-compose setup

---

## 8. Deployment Stack

### Backend Deployment

Recommended:
- Render
- Railway

Why:
- Managed PostgreSQL
- Docker support
- Environment variable configuration
- Easy CI/CD integration

---

### Frontend Deployment

Recommended:
- Vercel
- Netlify

Why:
- Optimized for React
- Simple environment configuration
- Fast global deployment

---

## 9. Environment Management

Environment variables used for:

- DJANGO_SECRET_KEY
- DEBUG flag
- DATABASE_URL
- JWT_SECRET
- LLM_API_KEY

Secrets are never committed to Git.

---

## 12. Future Upgrade Compatibility

The stack supports future improvements such as:

- Celery + Redis for async tasks
- Vector database (Pinecone / FAISS)
- Streaming ingestion
- Microservice split of ML engine
- Kubernetes deployment
- Monitoring with Prometheus/Grafana

---

## 13. Summary

ChronoLogs AI uses a carefully selected stack that balances:

- Development speed
- Production discipline
- ML integration
- AI narrative capabilities
- Clean full-stack architecture

The technology decisions are intentional and aligned with modern industry practices.