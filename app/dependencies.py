from fastapi import Cookie, Header, HTTPException, status
from app.db import get_db
from app.security import decode_token


def _token_from_request(authorization: str | None, access_token: str | None) -> str:
    if authorization and authorization.lower().startswith("bearer "):
        return authorization[7:].strip()
    if access_token:
        return access_token
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Login required")


def get_current_user(authorization: str | None = Header(default=None), access_token: str | None = Cookie(default=None)):
    token = _token_from_request(authorization, access_token)
    try:
        payload = decode_token(token)
        user_id = int(payload["sub"])
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token") from exc

    with get_db() as conn:
        user = conn.execute("SELECT id, name, email, created_at FROM users WHERE id=?", (user_id,)).fetchone()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return dict(user)
