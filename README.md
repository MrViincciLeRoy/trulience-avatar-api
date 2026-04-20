# trulience-avatar-api

Trulience avatar integration — FastAPI backend on Render + static frontend on GitHub Pages. One repo, two deployments.

```
trulience-avatar-api/
├── app/
│   ├── main.py        ← FastAPI (LOGIN / CHAT / LOGOUT)
│   ├── llm.py         ← Groq async handler
│   └── sessions.py    ← In-memory session store
├── docs/
│   └── index.html     ← GitHub Pages frontend
├── Procfile
└── requirements.txt
```

---

## 1. Deploy backend → Render

1. Push this repo to GitHub
2. [render.com](https://render.com) → **New Web Service** → connect repo
3. Set:
   - **Build command:** `pip install -r requirements.txt`
   - **Start command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4. Add env vars:

| Variable | Value |
|---|---|
| `GROQ_API_KEY` | From [console.groq.com](https://console.groq.com) |
| `GROQ_MODEL` | `llama3-8b-8192` (default) |
| `AVATAR_SYSTEM_PROMPT` | Your avatar's persona |

Your API will be at: `https://your-service.onrender.com`

---

## 2. Configure Trulience avatar

In the Trulience dashboard → your avatar → **BRAIN** tab:
- Mode: **3rd Party AI**
- Provider: **External Voice Platforms**
- REST Endpoint: `https://your-service.onrender.com/trulience`

---

## 3. Deploy frontend → GitHub Pages

1. Repo → **Settings** → **Pages**
2. Source: **Deploy from branch** → branch: `main` → folder: `/docs`
3. Your frontend will be at: `https://<you>.github.io/trulience-avatar-api`

On first load it asks for your **Avatar ID**, **token** (optional), and **Render URL** — no build step needed.

---

## Local dev

```bash
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

Open `docs/index.html` directly in a browser or serve with `python -m http.server` from the `docs/` folder.
