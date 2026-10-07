from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field, field_validator

class RegisterRequest(BaseModel):
    full_name: str = Field(min_length=2, max_length=120)
    email: str = Field(min_length=5, max_length=255)
    password: str = Field(min_length=8, max_length=128)

    @field_validator("email")
    @classmethod
    def normalize_email(cls, v):
        return v.strip().lower()

class LoginRequest(BaseModel):
    email: str
    password: str

class HomeItem(BaseModel):
    category: str = Field(min_length=2, max_length=80)
    quantity: int = Field(ge=1, le=100)

class HomeRequest(BaseModel):
    budget: float = Field(gt=0, le=10_000_000)
    rooms: List[str] = Field(min_length=1)
    style: str = Field(default="modern", max_length=80)
    items: List[HomeItem] = Field(min_length=1)
    notes: Optional[str] = Field(default="", max_length=1000)

class PartyRequest(BaseModel):
    budget: float = Field(gt=0, le=10_000_000)
    guests: int = Field(ge=1, le=10000)
    event_type: str = Field(min_length=2, max_length=80)
    venue: str = Field(default="indoor", max_length=120)
    city: str = Field(default="", max_length=120)
    notes: Optional[str] = Field(default="", max_length=1000)

class RecommendationItem(BaseModel):
    name: str
    category: str
    platform: str
    price: float
    quantity: int = 1
    reason: str
    url: str

class PlannerResponse(BaseModel):
    model_config = ConfigDict(extra="allow")
    planner: str
    title: str
    budget: float
    allocated_total: float
    savings: float
    summary: str
    tips: List[str]
    allocations: dict
    recommendations: List[RecommendationItem]
    ai_used: bool
    history_id: Optional[int] = None
