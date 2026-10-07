from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.entities import User
from app.models.schemas import HomeRequest, PartyRequest, PlannerResponse
from app.security import current_user
from app.services.gemini_utils import generate_home, generate_party, generate_jewelry
from app.services.recommender import home_fallback, party_fallback, jewelry_fallback, normalize_ai
from app.services.history import save_history

router=APIRouter()

def _finalize(planner, budget, request_data, ai_result, fallback_result, db, user):
    normalized=normalize_ai(ai_result,budget)
    data=normalized or fallback_result
    data.update({"planner":planner,"budget":budget,"allocated_total":round(sum(x["price"]*x["quantity"] for x in data["recommendations"]),2),"savings":0,"ai_used":bool(normalized)})
    data["savings"]=round(max(0,budget-data["allocated_total"]),2)
    row=save_history(db,user.id,planner,request_data,data); data["history_id"]=row.id
    return data

@router.post("/generate-home",response_model=PlannerResponse)
def generate_home_route(payload: HomeRequest, db: Session=Depends(get_db), user: User=Depends(current_user)):
    ai,catalog=generate_home(payload)
    data=_finalize("home",payload.budget,payload.model_dump(),ai,home_fallback(payload),db,user)
    return data

@router.post("/generate-party",response_model=PlannerResponse)
def generate_party_route(payload: PartyRequest, db: Session=Depends(get_db), user: User=Depends(current_user)):
    ai,catalog=generate_party(payload)
    data=_finalize("party",payload.budget,payload.model_dump(),ai,party_fallback(payload),db,user)
    return data

@router.post("/generate-jewelry",response_model=PlannerResponse)
async def generate_jewelry_route(budget: float=Form(...), occasion: str=Form(...), style: str=Form("modern"), outfit_notes: str=Form(""), outfit_image: UploadFile|None=File(None), db: Session=Depends(get_db), user: User=Depends(current_user)):
    if budget<=0 or budget>10_000_000: raise HTTPException(422,"Budget must be between 0 and 10,000,000")
    image_bytes=None; mime=None
    if outfit_image and outfit_image.filename:
        mime=outfit_image.content_type or "image/jpeg"
        if not mime.startswith("image/"): raise HTTPException(415,"Outfit upload must be an image")
        image_bytes=await outfit_image.read()
        if len(image_bytes)>5*1024*1024: raise HTTPException(413,"Image is too large; maximum is 5 MB")
    request_data={"budget":budget,"occasion":occasion,"style":style,"outfit_notes":outfit_notes,"image_uploaded":bool(image_bytes)}
    ai,_=generate_jewelry(request_data,image_bytes,mime)
    data=_finalize("jewelry",budget,request_data,ai,jewelry_fallback(request_data),db,user)
    return data
