import json
from app.db import get_db


def save_history(user_id: int, planner: str, request_data: dict, response_data: dict) -> int:
    with get_db() as conn:
        cur = conn.execute(
            "INSERT INTO recommendations(user_id, planner, request_json, response_json) VALUES(?,?,?,?)",
            (user_id, planner, json.dumps(request_data), json.dumps(response_data)),
        )
        return int(cur.lastrowid)


def list_history(user_id: int):
    with get_db() as conn:
        rows = conn.execute(
            "SELECT id, planner, request_json, response_json, created_at FROM recommendations WHERE user_id=? ORDER BY id DESC",
            (user_id,),
        ).fetchall()
    return [dict(r) for r in rows]


def get_history(user_id: int, item_id: int):
    with get_db() as conn:
        row = conn.execute(
            "SELECT id, planner, request_json, response_json, created_at FROM recommendations WHERE id=? AND user_id=?",
            (item_id, user_id),
        ).fetchone()
    return dict(row) if row else None


def delete_history(user_id: int, item_id: int) -> bool:
    with get_db() as conn:
        cur = conn.execute("DELETE FROM recommendations WHERE id=? AND user_id=?", (item_id, user_id))
        return cur.rowcount > 0
