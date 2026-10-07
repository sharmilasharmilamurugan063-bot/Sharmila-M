from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.config import APP_NAME, STATIC_DIR, TEMPLATES_DIR
from app.db import init_db
from app.routers import auth, planners, history


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title=APP_NAME,
    version="1.0.0",
    lifespan=lifespan,
)

app.mount(
    "/static",
    StaticFiles(directory=STATIC_DIR),
    name="static",
)

templates = Jinja2Templates(directory=TEMPLATES_DIR)

app.include_router(auth.router)
app.include_router(planners.router)
app.include_router(history.router)


@app.get("/api/health")
def health():
    return {
        "status": "ok",
        "service": APP_NAME,
    }


@app.get("/", response_class=HTMLResponse)
def home_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"title": APP_NAME},
    )


@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={"title": "Login"},
    )


@app.get("/register", response_class=HTMLResponse)
def register_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="register.html",
        context={"title": "Register"},
    )


@app.get("/dashboard", response_class=HTMLResponse)
def dashboard_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={"title": "Dashboard"},
    )


@app.get("/planner/home", response_class=HTMLResponse)
def home_planner_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="home_planner.html",
        context={"title": "Home Planner"},
    )


@app.get("/planner/party", response_class=HTMLResponse)
def party_planner_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="party_planner.html",
        context={"title": "Party Planner"},
    )


@app.get("/planner/jewelry", response_class=HTMLResponse)
def jewelry_planner_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="jewelry_planner.html",
        context={"title": "Jewelry Planner"},
    )


@app.get("/recommendations", response_class=HTMLResponse)
def recommendations_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="recommendations.html",
        context={"title": "Recommendations"},
    )


@app.get("/history", response_class=HTMLResponse)
def history_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="history.html",
        context={"title": "History"},
    )


@app.get("/testimonials", response_class=HTMLResponse)
def testimonials_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="testimonials.html",
        context={"title": "Testimonials"},
    )