# PocketSmart AI

A complete FastAPI + Jinja2 + SQLite + Gemini recommendation assistant based on the supplied project documentation.

## What is included
- Home interior budget planner
- Party budget planner
- Jewelry planner with optional outfit image analysis
- Registration/login/logout and JWT token endpoint
- Session info/session data
- Recommendation history
- Structured AI recommendations with deterministic fallback data
- Mock product/service catalog for Amazon, Flipkart, IKEA, Swiggy, Zomato and OYO-style sources
- Responsive frontend
- Automated API tests

## Important model update
The source document specifies Gemini 1.5 Flash Pro. That model family is no longer available in the current Gemini API, so this implementation defaults to the current `gemini-3.8-flash` model and keeps the model configurable through `.env`.

The catalog is intentionally local/mock: the source document asks for third-party sourcing but does not provide Amazon/Flipkart/IKEA/Swiggy/Zomato/OYO API credentials or affiliate integrations. The app therefore never invents live prices. AI recommendations are constrained to the local catalog and every result carries a source URL.

## Quick start

### Windows PowerShell
```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
# edit .env and add GEMINI_API_KEY if you want live Gemini recommendations
uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000

### macOS/Linux
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# edit .env and add GEMINI_API_KEY if you want live Gemini recommendations
uvicorn app.main:app --reload
```

## API
- `GET /health`
- `POST /register`
- `POST /login`
- `POST /logout`
- `POST /token`
- `GET /session-info`
- `GET /session-data`
- `POST /generate-home`
- `POST /generate-party`
- `POST /generate-jewelry`
- `GET /recommendations-details/{id}`
- `GET /history`

Interactive API docs: http://127.0.0.1:8000/docs

## Gemini
Create a Gemini API key from Google AI Studio, put it in `.env` as `GEMINI_API_KEY=...`, then restart the server. If the key is missing or Gemini is unavailable, the app uses the local recommendation engine so the project remains runnable.

## Tests
```bash
pytest -q
```
