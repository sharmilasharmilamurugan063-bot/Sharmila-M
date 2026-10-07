from fastapi import APIRouter, Depends, HTTPException, Response, status
from app.db import get_db
from app.dependencies import get_current_user
from app.models.schemas import LoginRequest, RegisterRequest
from app.security import create_token, hash_password, verify_password

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


@router.post("/register", status_code=201)
def register(data: RegisterRequest):
    with get_db() as conn:
        exists = conn.execute("SELECT id FROM users WHERE email=?", (data.email,)).fetchone()
        if exists:
            raise HTTPException(409, "Email is already registered")
        cur = conn.execute("INSERT INTO users(name,email,password_hash) VALUES(?,?,?)", (data.name.strip(), data.email, hash_password(data.password)))
        user_id = int(cur.lastrowid)
    return {"message": "Registration successful", "user_id": user_id}


@router.post("/login")
def login(data: LoginRequest, response: Response):
    with get_db() as conn:
        user = conn.execute("SELECT * FROM users WHERE email=?", (data.email,)).fetchone()
    if not user or not verify_password(data.password, user["password_hash"]):
        raise HTTPException(401, "Invalid email or password")
    token = create_token(int(user["id"]))
    response.set_cookie("access_token", token, httponly=True, samesite="lax", max_age=60 * 24 * 60 * 60)
    return {"message": "Login successful", "access_token": token, "token_type": "bearer", "user": {"id": user["id"], "name": user["name"], "email": user["email"]}}


@router.post("/logout")
def logout(response: Response):
    response.delete_cookie("access_token")
    return {"message": "Logged out"}


@router.get("/session-info")
def session_info(user=Depends(get_current_user)):
    return {"logged_in": True, "user_id": user["id"], "name": user["name"], "email": user["email"]}


@router.get("/session-data")
def session_data(user=Depends(get_current_user)):
    with get_db() as conn:
        count = conn.execute("SELECT COUNT(*) AS c FROM recommendations WHERE user_id=?", (user["id"],)).fetchone()["c"]
    return {"user": user, "recommendation_count": count}
