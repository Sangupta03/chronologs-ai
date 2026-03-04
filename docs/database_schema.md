# ChronoLogs AI
## Database Schema (Production-Ready Design)

---
# 1. Overview

Database: PostgreSQL  
Primary Key Strategy: UUID  
Timestamps: UTC  
Deletion Policy: Cascade on ownership  

The schema is designed for:

- Strong relational integrity
- Fast timeline queries
- Efficient clustering retrieval
- Clean user-level isolation
- Scalable ML processing

---

# 2. Entity Relationship Diagram

```
User
└── LogFile
├── LogEvent
└── Incident
└── IncidentStory
```

---

# 3. Tables

---

# 3.1 users (Custom User Model)

Purpose: Authentication & ownership

| Column | Type | Constraints |
|---------|------|-------------|
| id | UUID | PK, default=uuid4 |
| email | VARCHAR(255) | UNIQUE, NOT NULL |
| password_hash | VARCHAR(255) | NOT NULL |
| is_active | BOOLEAN | DEFAULT TRUE |
| is_staff | BOOLEAN | DEFAULT FALSE |
| created_at | TIMESTAMP | DEFAULT NOW() |
| updated_at | TIMESTAMP | AUTO UPDATE |

Indexes:
- UNIQUE(email)

Notes:
- Managed by Django auth system
- All data is user-scoped

---

# 3.2 log_files

Purpose: Store uploaded files metadata

| Column | Type | Constraints |
|---------|------|-------------|
| id | UUID | PK |
| user_id | UUID | FK → users(id) ON DELETE CASCADE |
| file_name | VARCHAR(255) | NOT NULL |
| file_size_bytes | INTEGER | NOT NULL |
| file_path | TEXT | NOT NULL |
| status | VARCHAR(50) | DEFAULT 'uploaded' |
| processing_time_ms | INTEGER | NULL |
| created_at | TIMESTAMP | DEFAULT NOW() |
| updated_at | TIMESTAMP | AUTO UPDATE |

Allowed status values:
- uploaded
- processing
- processed
- failed

Indexes:
- INDEX(user_id)
- INDEX(created_at)

---

# 3.3 log_events

Purpose: Structured individual log entries

| Column | Type | Constraints |
|---------|------|-------------|
| id | UUID | PK |
| log_file_id | UUID | FK → log_files(id) ON DELETE CASCADE |
| timestamp | TIMESTAMP | NOT NULL |
| severity | VARCHAR(20) | NOT NULL |
| message | TEXT | NOT NULL |
| service | VARCHAR(150) | NULL |
| anomaly_score | FLOAT | NULL |
| cluster_id | INTEGER | NULL |
| created_at | TIMESTAMP | DEFAULT NOW() |

Severity values:
- INFO
- WARN
- ERROR
- DEBUG
- CRITICAL

Indexes:
- INDEX(log_file_id)
- INDEX(timestamp)
- INDEX(cluster_id)
- INDEX(severity)

Why cluster_id here?
- Assigned after KMeans
- Used to group events into incidents
- Faster than join-based clustering

---

# 3.4 incidents

Purpose: Grouped log events representing logical incident

| Column | Type | Constraints |
|---------|------|-------------|
| id | UUID | PK |
| log_file_id | UUID | FK → log_files(id) ON DELETE CASCADE |
| cluster_id | INTEGER | NOT NULL |
| start_time | TIMESTAMP | NOT NULL |
| end_time | TIMESTAMP | NOT NULL |
| duration_seconds | INTEGER | NOT NULL |
| severity_score | FLOAT | NOT NULL |
| anomaly_score_avg | FLOAT | NOT NULL |
| total_events | INTEGER | NOT NULL |
| created_at | TIMESTAMP | DEFAULT NOW() |

Indexes:
- INDEX(log_file_id)
- INDEX(start_time)
- COMPOSITE INDEX(log_file_id, cluster_id)

Severity Score Calculation Example:
- Weighted error count
- Anomaly density
- Event frequency

This allows sorting incidents by impact.

---

# 3.5 incident_stories

Purpose: AI-generated narrative for each incident

| Column | Type | Constraints |
|---------|------|-------------|
| id | UUID | PK |
| incident_id | UUID | FK → incidents(id) ON DELETE CASCADE |
| summary | TEXT | NOT NULL |
| narrative | TEXT | NOT NULL |
| root_cause | TEXT | NULL |
| impact | TEXT | NULL |
| recommendations | TEXT | NULL |
| generated_at | TIMESTAMP | DEFAULT NOW() |

Indexes:
- UNIQUE(incident_id)

Only one story per incident.

---

# 4. Data Flow Mapping

Upload → log_files  
Parse → log_events  
Cluster → log_events.cluster_id  
Aggregate → incidents  
Generate AI → incident_stories  

---

# 5. Performance Considerations

Optimized for:

- Timeline queries (timestamp index)
- Cluster grouping (cluster_id index)
- User isolation (user_id index)
- Dashboard metrics (log_file_id index)

Expected scale for MVP:
- < 100k log events per file
- < 500 incidents per file

---

# 6. Cascade Rules

Deleting a user deletes:
- log_files
- log_events
- incidents
- incident_stories

Ensures clean ownership model.

---

# 7. Future Extensions (Schema Ready)

Possible additions:

incident_embeddings
- incident_id
- vector (for similarity search)

processing_metrics
- log_file_id
- parse_time
- cluster_time
- ai_generation_time

organizations
- multi-tenant support

---

# 8. Why This Schema Is Strong

This schema demonstrates:

- Proper normalization
- Clear ownership boundaries
- Efficient clustering model
- AI separation from raw data
- Scalable indexing strategy
- Production-ready thinking

It is not a toy schema — it reflects real backend system design.