# GovWatch India

A real-time government news aggregator that scrapes central and state government portals and surfaces updates — schemes, policies, circulars, notifications — in one clean portal for Indian citizens.

**Stack:** Python + FastAPI + Supabase + Next.js + Vercel + GitHub Actions — 100% free tier.

---

## Project Structure

```
govwatch-india/
├── scraper/          # Python scrapers (PIB RSS, india.gov.in, myScheme)
├── api/              # FastAPI backend
├── frontend/         # Next.js frontend (TypeScript + Tailwind)
├── .github/
│   └── workflows/
│       └── scraper.yml   # GitHub Actions cron (runs every hour)
└── schema.sql        # Supabase DB schema — run this first
```

---

## Build Order

```
Step 1   Set up Supabase → run schema.sql in the SQL editor
Step 2   cd scraper && pip install -r requirements.txt
Step 3   cp .env.example .env → add your Supabase credentials
Step 4   python main.py → verify articles appear in Supabase dashboard
Step 5   cd ../api && pip install -r requirements.txt
Step 6   cp .env.example .env → add your Supabase credentials
Step 7   uvicorn main:app --reload → test http://localhost:8000/articles
Step 8   cd ../frontend && cp .env.local.example .env.local
Step 9   npm install && npm run dev → open http://localhost:3000
Step 10  Verify full flow: scraper → DB → API → frontend
Step 11  git push → GitHub Actions picks up scraper cron automatically
Step 12  Deploy API to Render (connect GitHub repo, set env vars)
Step 13  Deploy frontend to Vercel (connect GitHub repo, set NEXT_PUBLIC_API_URL)
```

---

## Phase 1 — Supabase Setup

1. Create a free project at [supabase.com](https://supabase.com)
2. Open the SQL Editor and run `schema.sql`
3. Copy your Project URL and anon key from **Settings → API**

---

## Phase 2 — Scraper

```bash
cd scraper
pip install -r requirements.txt
cp .env.example .env   # fill in SUPABASE_URL and SUPABASE_KEY
python main.py
```

Sources currently implemented:
- **PIB** (Press Information Bureau) — RSS feed, English

Sources stubbed for future implementation:
- **myScheme.gov.in** — government scheme listings
- **india.gov.in** — national portal news

### Add new scrapers
Follow the pattern in `scraper/sources/pib.py`:
1. Create `scraper/sources/your_source.py`
2. Implement a `scrape_your_source()` function
3. Import and call it from `scraper/main.py`

---

## Phase 3 — FastAPI Backend

```bash
cd api
pip install -r requirements.txt
cp .env.example .env
uvicorn main:app --reload
```

API available at `http://localhost:8000`

| Endpoint | Description |
|----------|-------------|
| `GET /articles` | List articles (supports `category`, `state`, `ministry`, `source`, `page`, `per_page`) |
| `GET /articles/{id}` | Get single article |
| `GET /search?q=` | Full-text search |
| `GET /sources` | List active sources |
| `GET /health` | Health check |

Interactive docs at `http://localhost:8000/docs`

---

## Phase 4 — GitHub Actions Cron

Push to GitHub, then add secrets under **Settings → Secrets and variables → Actions**:

```
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key
```

The scraper runs automatically every hour via `.github/workflows/scraper.yml`.
You can also trigger it manually from the **Actions** tab.

---

## Phase 5 — Next.js Frontend

```bash
cd frontend
cp .env.local.example .env.local   # set NEXT_PUBLIC_API_URL
npm install
npm run dev
```

Pages:
- `/` — Home feed with category + state filters
- `/search?q=` — Full-text search results
- `/article/[id]` — Article detail page

---

## Optional — Telegram Alerts

Set in `scraper/.env`:
```
TELEGRAM_BOT_TOKEN=your-bot-token
TELEGRAM_CHANNEL_ID=@your_channel
```

Then call `send_alert(article)` from your scraper after a successful insert.

---

## Deployment

| Service | What to deploy | Free tier |
|---------|---------------|-----------|
| Supabase | Database | 500 MB, unlimited API |
| Render | FastAPI (`api/`) | 750 hrs/month |
| Vercel | Next.js (`frontend/`) | Unlimited hobby |
| GitHub Actions | Scraper cron | 2,000 min/month |

---

## What to Build Next

- `scraper/sources/myscheme.py` — scheme listings (needs Playwright for JS rendering)
- `scraper/sources/mygov.py` — mygov.in announcements
- `scraper/sources/state_portals.py` — Maharashtra, Delhi, Karnataka
- AI summarisation via Hugging Face free inference API
- User subscriptions with Supabase Auth

---

*Free tier stack. No credit card required.*
