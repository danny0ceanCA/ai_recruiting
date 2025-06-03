# Student-Profile SaaS Platform 🚀

A multi-tenant web application that lets **schools** securely manage student profiles, view placement metrics, and match students to job postings using **OpenAI‑powered embeddings** stored in a **Redis vector database**.

---

## 1 Key User Flows

| Role | Dashboard Tiles | What they can do |
|------|-----------------|------------------|
| **Career-Services Staff** | **Student Profiles** · **My Metrics** · **CSV Bulk Upload** | • Create / edit a single profile (embedding created via ChatGPT API, stored in Redis)<br>• Upload a CSV of profiles<br>• View KPI dashboards |
| **Admin** | *All the above* · **Admin Panel** · **Job Postings** | • See every student across schools<br>• Filter & export summaries<br>• Create / edit job postings<br>• Click **Match** to rank students by cosine similarity of embeddings |

> **Dashboard UX:** futuristic dark‑blue theme with subtle, light‑blue microchip line accents. Tiles animate in on login and route securely back to `/dashboard`.

---

## 2 Data & Matching Pipeline

1. **Profile Save** → Backend calls **OpenAI ChatGPT embeddings API** on the concatenated profile text.  
2. Vector is saved to **Redis 7 VECTOR** index (`HSET student:<id> embedding "<float32[1536]>"`).  
3. **Job Posting** → Admin clicks **Match**.  
4. Job description is embedded, then compared to student vectors with **Redis `VECTOR` cosine search**.  
5. Results are sorted by score and displayed to admin.

---

## 3 Simplified Schema

```
Student       Job           Match
-------       ---           -----
id            id            id
school_id →   title         student_id →
name          description   job_id →
background    created_at    score
education                    finalized
experience                   archived
qualities
embedding     (vector)
created_at
```

---

## 4 Tech Stack

| Layer | Choice |
|-------|--------|
| **Backend** | FastAPI · Uvicorn |
| **AI / Embeddings** | OpenAI ChatGPT (`text-embedding-3-small`) |
| **Vector store** | Redis 7 (`VECTOR` module) |
| **DB** | PostgreSQL + SQLAlchemy 2 · Alembic |
| **Auth** | JWT (PyJWT) with role-based decorators |
| **Task queue** | RQ for async embedding / match jobs |
| **Frontend** | React (Vite) + Tailwind CSS |
| **Testing** | Pytest (+ Playwright e2e) |
| **CI / CD** | GitHub Actions ➜ Render (Docker) |

---

## 5 Project Layout

```
.
├── app/
│   ├── api/
│   ├── core/
│   ├── models/
│   ├── services/      # embeddings.py, match.py
│   └── main.py
├── frontend/
├── scripts/
│   ├── create_admin.py
│   └── bulk_upload_csv_parser.py
├── tests/
├── vendor/
├── requirements.txt
└── README.md
```

---

## 6 Quick Start (local)

```bash
# Prereqs: Python 3.12 · Node 20 · Postgres 15 · Redis 7

git clone https://github.com/<you>/<repo>.git
cd <repo>

python -m pip install -r requirements.txt
createdb student_saas
alembic upgrade head

# Bootstrap admin
python scripts/create_admin.py --email admin@demo.com --name "Admin" --school "Demo U"

# Run API
uvicorn app.main:app --reload

# Frontend
(cd frontend && npm install && npm run dev)
```

---

## 7 Environment Variables

| Key | Example | Purpose |
|-----|---------|---------|
| `OPENAI_API_KEY` | `sk-…` | Create embeddings |
| `REDIS_URL` | `redis://:pw@localhost:6379/0` | Vector store |
| `DATABASE_URL` | `postgresql://user:pass@localhost:5432/student_saas` | SQLAlchemy connection |
| `SECRET_KEY` | `super-secret` | JWT signing |
| `STRIPE_API_KEY` | `sk_live_…` | Billing (optional) |

---

## 8 Codex Offline Setup

```bash
set -euo pipefail
python -m pip install --no-index --find-links vendor -r requirements.txt
npm --prefix frontend ci && npm --prefix frontend run build
alembic upgrade head
python scripts/create_admin.py --email admin@demo.com --name Admin --school Demo
```

---

## 9 Testing

Install dependencies from `vendor/` and run Pytest:

```bash
./scripts/install_offline_deps.sh
pytest
```

---

## 10 Roadmap

- [ ] Complete dashboard & navigation  
- [ ] Fine‑tune embedding prompt for better matches  
- [ ] Advanced metrics (placement rate, time‑to‑match)  
- [ ] Stripe metered billing per active student profile  
- [ ] Internationalization (ES / FR)

---

## 11 License

MIT — see [`LICENSE`](./LICENSE).

*Happy matching!* 🎉
