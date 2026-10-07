# PocketSmart AI — Your Smart Budget & Recommendation Assistant

A complete FastAPI + Jinja2 + Gemini application based on the supplied project documentation.

## Important model note
The original document specifies Gemini 1.5 Flash Pro. Gemini 1.5 Flash was shut down by Google on September 29, 2025, so this implementation keeps the same Gemini-powered architecture but defaults to a currently available model through `GEMINI_MODEL`. Change that value if your Google AI account has access to another current model.

## Features
- Registration, login, JWT authentication and logout
- Session info and session data endpoints
- Home Interior planner
- Party Budget planner
- Jewelry planner with optional outfit image upload
- Gemini text + image integration
- Deterministic fallback recommendations when no Gemini API key is configured or the AI call fails
- Mock cross-platform product/service catalog for Amazon, Flipkart, IKEA, Swiggy, Zomato and OYO-style links
- Recommendation history
- Responsive Jinja2 frontend
- API documentation at `/docs`
- Automated API tests

## Python 3.15
The project is written for Python 3.15 syntax/runtime. Current FastAPI and Pydantic releases are actively evolving around Python 3.15, while some third-party packages may lag. If `pip` reports that a dependency has no compatible wheel on your machine, use the newest available release of that dependency rather than downgrading the application code.

## Quick start on Windows PowerShell
```powershell
cd "C:\path\to\PocketSmart-AI-Complete"
py -3.15 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
Copy-Item .env.example .env
```

Open `.env` and add your Gemini API key. The app still runs in fallback/demo mode without a key.

Run:
```powershell
python run.py
```
Then open http://127.0.0.1:8000

## API test
In another terminal:
```powershell
.\.venv\Scripts\Activate.ps1
pytest -q
```

## Main API routes
- `POST /api/auth/register`
- `POST /api/auth/login`
- `POST /api/auth/logout`
- `GET /api/auth/session-info`
- `GET /api/auth/session-data`
- `POST /api/planners/generate-home`
- `POST /api/planners/generate-party`
- `POST /api/planners/generate-jewelry`
- `GET /api/history`
- `GET /api/history/{id}`
- `DELETE /api/history/{id}`
- `GET /api/health`

## Architecture
```text
Browser/Jinja2/JS
       |
       v
FastAPI routers
       |
       +--> Auth / JWT / SQLite
       |
       +--> Planner validation
       |
       +--> Gemini service ----> Gemini API
       |          |
       |          +------------> JSON recommendations
       |
       +--> Mock catalog fallback
       |
       +--> History service ----> SQLite
```

The platform catalog is deliberately mocked, matching the source document's instruction to use mock API calls/simulated sourcing rather than claiming live marketplace APIs.
