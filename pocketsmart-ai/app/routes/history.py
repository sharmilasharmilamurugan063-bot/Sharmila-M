from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.entities import Recommendation, User
from app.security import current_user
from app.services.history import serialize_history

router=APIRouter()

@router.get("/history")
def history(db: Session=Depends(get_db), user: User=Depends(current_user)):
    rows=db.query(Recommendation).filter(Recommendation.user_id==user.id).order_by(Recommendation.created_at.desc()).limit(50).all()
    return {"items":[serialize_history(r) for r in rows]}

@router.get("/recommendations-details/{recommendation_id}")
def details(recommendation_id:int, db:Session=Depends(get_db), user:User=Depends(current_user)):
    row=db.query(Recommendation).filter(Recommendation.id==recommendation_id,Recommendation.user_id==user.id).first()
    if not row: raise HTTPException(404,"Recommendation not found")
    return serialize_history(row)
