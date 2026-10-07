from fastapi import APIRouter, Depends, File, Form, UploadFile, HTTPException
from app.dependencies import get_current_user
from app.models.schemas import HomeRequest, PartyRequest
from app.services.gemini_utils import generate_home, generate_party, generate_jewelry
from app.services.history import save_history
from app.config import MAX_UPLOAD_MB

router = APIRouter(prefix="/api/planners", tags=["Planners"])


def _with_history(user_id: int, planner: str, request_data: dict, result: dict):
    result["history_id"] = save_history(user_id, planner, request_data, result)
    return result


@router.post("/generate-home")
def home(data: HomeRequest, user=Depends(get_current_user)):
    payload = data.model_dump()
    return _with_history(user["id"], "home", payload, generate_home(payload))


@router.post("/generate-party")
def party(data: PartyRequest, user=Depends(get_current_user)):
    payload = data.model_dump()
    return _with_history(user["id"], "party", payload, generate_party(payload))


@router.post("/generate-jewelry")
async def jewelry(
    budget: float = Form(..., gt=0),
    occasion: str = Form(...),
    style: str = Form("classic"),
    outfit_color: str = Form(""),
    notes: str = Form(""),
    outfit_image: UploadFile | None = File(default=None),
    user=Depends(get_current_user),
):
    if len(occasion) > 100 or len(style) > 100 or len(outfit_color) > 100 or len(notes) > 500:
        raise HTTPException(400, "One or more fields are too long")
    image_bytes = None
    mime_type = None
    if outfit_image and outfit_image.filename:
        if outfit_image.content_type not in {"image/jpeg", "image/png", "image/webp"}:
            raise HTTPException(400, "Only JPG, PNG and WEBP images are supported")
        image_bytes = await outfit_image.read()
        if len(image_bytes) > MAX_UPLOAD_MB * 1024 * 1024:
            raise HTTPException(413, f"Image must be {MAX_UPLOAD_MB} MB or smaller")
        mime_type = outfit_image.content_type
    payload = {"budget": budget, "occasion": occasion, "style": style, "outfit_color": outfit_color, "notes": notes, "image_uploaded": bool(image_bytes)}
    return _with_history(user["id"], "jewelry", payload, generate_jewelry(payload, image_bytes, mime_type))
