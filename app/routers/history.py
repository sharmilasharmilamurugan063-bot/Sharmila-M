import json
from fastapi import APIRouter, Depends, HTTPException
from app.dependencies import get_current_user
from app.services.history import list_history, get_history, delete_history

router = APIRouter(prefix="/api/history", tags=["History"])


def _decode(row):
    row["request"] = json.loads(row.pop("request_json"))
    row["response"] = json.loads(row.pop("response_json"))
    return row


@router.get("")
def history(user=Depends(get_current_user)):
    return {"items": [_decode(r) for r in list_history(user["id"])]}


@router.get("/{item_id}")
def history_item(item_id: int, user=Depends(get_current_user)):
    row = get_history(user["id"], item_id)
    if not row:
        raise HTTPException(404, "History item not found")
    return _decode(row)


@router.delete("/{item_id}")
def history_delete(item_id: int, user=Depends(get_current_user)):
    if not delete_history(user["id"], item_id):
        raise HTTPException(404, "History item not found")
    return {"message": "Deleted"}
