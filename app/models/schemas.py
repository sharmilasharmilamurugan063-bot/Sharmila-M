from typing import Literal
from pydantic import BaseModel, Field, field_validator


class RegisterRequest(BaseModel):
    name: str = Field(min_length=2, max_length=80)
    email: str = Field(min_length=5, max_length=160)
    password: str = Field(min_length=6, max_length=128)

    @field_validator("email")
    @classmethod
    def normalize_email(cls, value: str) -> str:
        return value.strip().lower()


class LoginRequest(BaseModel):
    email: str
    password: str

    @field_validator("email")
    @classmethod
    def normalize_email(cls, value: str) -> str:
        return value.strip().lower()


class HomeRequest(BaseModel):
    budget: float = Field(gt=0)
    rooms: list[str] = Field(min_length=1)
    lights: int = Field(default=0, ge=0)
    fans: int = Field(default=0, ge=0)
    dining_tables: int = Field(default=0, ge=0)
    style: str = Field(default="modern", max_length=80)
    notes: str = Field(default="", max_length=500)


class PartyRequest(BaseModel):
    budget: float = Field(gt=0)
    guests: int = Field(gt=0, le=10000)
    event_type: Literal["birthday", "corporate", "wedding", "engagement", "other"] = "birthday"
    venue: str = Field(default="indoor", max_length=100)
    city: str = Field(default="", max_length=100)
    notes: str = Field(default="", max_length=500)


class RecommendationItem(BaseModel):
    title: str
    category: str
    estimated_price: float
    platform: str
    reason: str
    url: str


class RecommendationResponse(BaseModel):
    planner: str
    budget: float
    summary: str
    allocation: dict[str, float]
    recommendations: list[RecommendationItem]
    tips: list[str]
    source: Literal["gemini", "fallback"]
    history_id: int | None = None
