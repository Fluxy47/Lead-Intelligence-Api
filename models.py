from pydantic import BaseModel, EmailStr, Field
from datetime import datetime

class LeadRequest(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    company: str | None = Field(default=None, min_length=2, max_length=100)
    message: str = Field(min_length=10, max_length=2000)

class LeadResponse(BaseModel):
    lead_id: str
    name: str
    email: EmailStr
    company: str | None
    message: str
    received_at: datetime

class FieldError(BaseModel):
    field: str
    message: str

class ErrorResponse(BaseModel):
    error_code: str
    message: str
    details: list[FieldError] | None = None