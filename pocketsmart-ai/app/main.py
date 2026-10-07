from pathlib import Path
from fastapi import Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.config import get_settings
from app.db import Base, engine
from app.models.entities import User, Recommendation
from app.routes.auth import router as auth_router
from app.routes.planners import router as planner_router
from app.routes.history import router as history_router
from app.security import current_user

settings=get_settings()
Base.metadata.create_all(bind=engine)
app=FastAPI(title=settings.app_name,version="1.0.0",description="Budget-aware GenAI recommendation assistant")
app.add_middleware(CORSMiddleware,allow_origins=settings.cors_origin_list,allow_credentials=True,allow_methods=["*"],allow_headers=["*"])
app.mount("/static",StaticFiles(directory=Path(__file__).parent/"static"),name="static")
templates=Jinja2Templates(directory=Path(__file__).parent/"templates")
app.include_router(auth_router)
app.include_router(planner_router)
app.include_router(history_router)

@app.get("/health")
def health():
    return {"status":"ok","app":settings.app_name,"ai_configured":bool(settings.gemini_api_key),"model":settings.gemini_model}

@app.get("/",response_class=HTMLResponse)
def home(request:Request):
    return templates.TemplateResponse("index.html",{"request":request,"user":None})

@app.get("/dashboard",response_class=HTMLResponse)
def dashboard(request:Request):
    return templates.TemplateResponse("dashboard.html",{"request":request})

@app.get("/login",response_class=HTMLResponse)
def login_page(request:Request): return templates.TemplateResponse("login.html",{"request":request,"mode":"login"})

@app.get("/register",response_class=HTMLResponse)
def register_page(request:Request): return templates.TemplateResponse("login.html",{"request":request,"mode":"register"})

@app.get("/planner/{planner}",response_class=HTMLResponse)
def planner_page(planner:str,request:Request):
    if planner not in {"home","party","jewelry"}: return RedirectResponse("/")
    return templates.TemplateResponse(f"{planner}.html",{"request":request})

@app.get("/history-page",response_class=HTMLResponse)
def history_page(request:Request): return templates.TemplateResponse("history.html",{"request":request})

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)

if __name__=="__main__":
    import uvicorn
    uvicorn.run("app.main:app",host="127.0.0.1",port=8000,reload=True)
