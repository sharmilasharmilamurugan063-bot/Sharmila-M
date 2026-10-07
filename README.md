# PocketSmart AI — Your Smart Budget & Recommendation Assistant

A complete FastAPI + Jinja2 + Gemini application for smart budget planning and recommendations.

## Features

- Registration, login, JWT authentication and logout
- Session information and session data
- Home Interior Budget Planner
- Party Budget Planner
- Jewelry Budget Planner
- Optional outfit image upload for jewelry planning
- Gemini AI integration
- Fallback recommendations when Gemini is unavailable
- Mock product/service catalog
- Recommendation history
- Responsive Jinja2 frontend
- FastAPI REST APIs
- Interactive API documentation
- Automated API tests

## Python 3.15

This project is designed to run with Python 3.15.

## Project Structure

```text
PocketSmart-AI-Complete/
│
├── app/
│   ├── main.py
│   ├── config.py
│   ├── db.py
│   ├── security.py
│   ├── dependencies.py
│   │
│   ├── models/
│   │   └── schemas.py
│   │
│   ├── routers/
│   │   ├── auth.py
│   │   ├── planners.py
│   │   └── history.py
│   │
│   ├── services/
│   │   ├── catalog.py
│   │   ├── gemini_utils.py
│   │   └── history.py
│   │
│   ├── templates/
│   │   ├── index.html
│   │   ├── login.html
│   │   ├── register.html
│   │   ├── dashboard.html
│   │   ├── home_planner.html
│   │   ├── party_planner.html
│   │   ├── jewelry_planner.html
│   │   ├── recommendations.html
│   │   ├── history.html
│   │   └── testimonials.html
│   │
│   └── static/
│       ├── css/
│       │   └── style.css
│       └── js/
│           └── app.js
│
├── tests/
│   └── test_api.py
│
├── data/
├── uploads/
├── .env.example
├── .gitignore
├── .python-version
├── pyproject.toml
├── requirements.txt
├── run.py
├── setup.ps1
└── README.md# PocketSmart AI — Your Smart Budget & Recommendation Assistant

A complete FastAPI + Jinja2 + Gemini application for smart budget planning and recommendations.

## Features

- Registration, login, JWT authentication and logout
- Session information and session data
- Home Interior Budget Planner
- Party Budget Planner
- Jewelry Budget Planner
- Optional outfit image upload for jewelry planning
- Gemini AI integration
- Fallback recommendations when Gemini is unavailable
- Mock product/service catalog
- Recommendation history
- Responsive Jinja2 frontend
- FastAPI REST APIs
- Interactive API documentation
- Automated API tests

## Python 3.15

This project is designed to run with Python 3.15.

## Project Structure

```text
PocketSmart-AI-Complete/
│
├── app/
│   ├── main.py
│   ├── config.py
│   ├── db.py
│   ├── security.py
│   ├── dependencies.py
│   │
│   ├── models/
│   │   └── schemas.py
│   │
│   ├── routers/
│   │   ├── auth.py
│   │   ├── planners.py
│   │   └── history.py
│   │
│   ├── services/
│   │   ├── catalog.py
│   │   ├── gemini_utils.py
│   │   └── history.py
│   │
│   ├── templates/
│   │   ├── index.html
│   │   ├── login.html
│   │   ├── register.html
│   │   ├── dashboard.html
│   │   ├── home_planner.html
│   │   ├── party_planner.html
│   │   ├── jewelry_planner.html
│   │   ├── recommendations.html
│   │   ├── history.html
│   │   └── testimonials.html
│   │
│   └── static/
│       ├── css/
│       │   └── style.css
│       └── js/
│           └── app.js
│
├── tests/
│   └── test_api.py
│
├── data/
├── uploads/
├── .env.example
├── .gitignore
├── .python-version
├── pyproject.toml
├── requirements.txt
├── run.py
├── setup.ps1
└── README.md