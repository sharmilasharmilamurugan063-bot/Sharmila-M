import json
from sqlalchemy.orm import Session
from app.models.entities import Recommendation

def save_history(db: Session, user_id: int, planner: str, request_data: dict, response_data: dict):
    row=Recommendation(user_id=user_id, planner=planner, request_json=json.dumps(request_data, default=str), response_json=json.dumps(response_data, default=str))
    db.add(row); db.commit(); db.refresh(row); return row

def serialize_history(row):
    return {"id":row.id,"planner":row.planner,"created_at":row.created_at.isoformat(),"request":json.loads(row.request_json),"response":json.loads(row.response_json)}
