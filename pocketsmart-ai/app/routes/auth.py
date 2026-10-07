from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.entities import User
from app.models.schemas import RegisterRequest, LoginRequest
from app.security import create_access_token, current_user, hash_password, verify_password

router=APIRouter()

def _set_cookie(response, token):
    response.set_cookie("access_token", token, httponly=True, samesite="lax", secure=False, max_age=60*60*24)

@router.post("/register")
def register(payload: RegisterRequest, db: Session=Depends(get_db)):
    if db.query(User).filter(User.email==payload.email).first():
        raise HTTPException(409,"Email already registered")
    user=User(email=payload.email, full_name=payload.full_name.strip(), password_hash=hash_password(payload.password))
    db.add(user); db.commit(); db.refresh(user)
    return {"message":"Registration successful","user":{"id":user.id,"email":user.email,"full_name":user.full_name}}

@router.post("/login")
def login(payload: LoginRequest, db: Session=Depends(get_db)):
    user=db.query(User).filter(User.email==payload.email.strip().lower()).first()
    if not user or not verify_password(payload.password,user.password_hash): raise HTTPException(401,"Invalid email or password")
    token=create_access_token(user.id)
    response = {"message":"Login successful","access_token":token,"token_type":"bearer"}
    from fastapi.responses import JSONResponse
    out = JSONResponse(response)
    _set_cookie(out, token)
    return out

@router.post("/logout")
def logout():
    response=RedirectResponse("/",status_code=303); response.delete_cookie("access_token"); return response

@router.post("/token")
def token(payload: LoginRequest, db: Session=Depends(get_db)):
    return login(payload,db)

@router.get("/session-info")
def session_info(user: User=Depends(current_user)):
    return {"logged_in":True,"user_id":user.id,"email":user.email,"full_name":user.full_name}

@router.get("/session-data")
def session_data(user: User=Depends(current_user), db: Session=Depends(get_db)):
    count=len(user.recommendations)
    return {"user_id":user.id,"recommendation_count":count,"preferences":{"planner_history":True}}
