import uuid
from datetime import datetime, timezone

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

from models import LeadRequest, LeadResponse, ErrorResponse

app = FastAPI(title="Lead Intelligence API", version="0.1.0")

# Known disposable/throwaway email providers — reject these as leads.
# Not exhaustive; extend as you find more.
DISPOSABLE_DOMAINS = {
    "mailinator.com",
    "tempmail.com",
    "guerrillamail.com",
    "10minutemail.com",
    "throwawaymail.com",
}


def is_disposable_email(email: str) -> bool:
    domain = email.split("@")[-1].lower()
    return domain in DISPOSABLE_DOMAINS


@app.post("/lead", response_model=LeadResponse, status_code=201)
def create_lead(lead: LeadRequest):
    # --- business logic (runs only after Pydantic validation passes) ---
    if is_disposable_email(lead.email):
        raise HTTPException(
            status_code=400,
            detail={
                "error_code": "DISPOSABLE_EMAIL",
                "message": "Disposable/throwaway email addresses are not accepted.",
            },
        )

    # --- create the lead ---
    return LeadResponse(
        lead_id=str(uuid.uuid4()),
        name=lead.name,
        email=lead.email,
        company=lead.company,
        message=lead.message,
        received_at=datetime.now(timezone.utc),
    )