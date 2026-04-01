# 🚀 ChronoLogs AI — Intelligent Log Analysis System

ChronoLogs AI is a full-stack system that ingests raw logs, applies machine learning techniques to detect anomalies and clusters, generates incidents, and provides human-readable AI explanations.

---

## 🧠 Features

### 🔐 Authentication

* JWT-based login system
* Secure API access

### 📤 Log Upload

* Upload large log files
* Streaming parser (memory-efficient)
* Bulk database insertion

### ⚙️ Log Processing

* Regex-based log parsing
* Structured event extraction
* Event hashing (deduplication-ready)

### 🤖 AI Engine

* TF-IDF vectorization
* K-Means clustering
* Rule-based anomaly detection

### 🚨 Incident Detection

* Cluster-based incident grouping
* Severity scoring system
* Time-window aggregation

### 🧾 AI Storytelling

* Human-readable summaries
* Error analysis
* Service-level insights

### 🎨 Frontend Dashboard

* React + Tailwind UI
* Upload → Analyze → View flow
* Incident cards with severity colors
* Sidebar navigation (SaaS-style UI)

---

## 🏗️ Architecture

```text
Frontend (React)
   ↓
Django REST API
   ↓
Log Parser → ML Engine → Incident Engine → Storytelling
   ↓
PostgreSQL / SQLite
```

---

## 🧪 Tech Stack

### Backend

* Django
* Django REST Framework
* JWT Authentication
* PostgreSQL / SQLite

### AI / ML

* Scikit-learn
* TF-IDF Vectorizer
* K-Means Clustering

### Frontend

* React (Vite)
* Tailwind CSS
* Axios
* React Router

---

## 📂 Project Structure

```text
backend/
  apps/
    logs/
    incidents/
    ai_engine/
    accounts/

frontend/
  src/
    components/
    pages/
    services/
```

---

## ⚙️ Setup Instructions

### 🔹 Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

python manage.py migrate
python manage.py runserver
```

---

### 🔹 Frontend

```bash
cd frontend
npm install
npm run dev
```

---

## 🔐 Authentication

Login API:

```http
POST /api/auth/login/
```

Response:

```json
{
  "access": "JWT_TOKEN"
}
```

---

## 📤 Upload Logs

```http
POST /api/logs/upload/
```

---

## 🤖 Analyze Logs

```http
POST /api/ai/analyze/<log_id>/
```

---

## 🚨 Get Incidents

```http
GET /api/incidents/
```

---

## 🧠 Key Concepts

* Streaming log parsing for scalability
* Feature extraction using TF-IDF
* Unsupervised clustering for grouping logs
* Rule-based anomaly detection
* Incident abstraction layer
* AI-generated explanations

---

## 🔥 Highlights

* End-to-end ML pipeline integrated into production-like system
* Real-time log ingestion and analysis
* Human-readable insights (AI storytelling)
* Clean SaaS-style UI

---

## 📈 Future Improvements

* Real-time streaming with Kafka
* Advanced anomaly detection (Isolation Forest)
* Alerting system
* Role-based access
* Charts & analytics dashboard

---

## 👩‍💻 Author

Sanjoli Gupta

---

## ⭐ License

MIT License
