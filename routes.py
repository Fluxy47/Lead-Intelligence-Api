import uuid
from datetime import datetime, timezone

from fastapi import APIRouter

from exceptions import DisposableEmailError, LowEffortMessageError
from models import ErrorResponse, LeadRequest, LeadResponse

import logging


logger = logging.getLogger("lead_api")

router = APIRouter(tags=["leads"])

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

def is_low_effort_message(message: str) -> bool:
    # Drop all whitespace, then check how many distinct characters remain.
    # 0 distinct = whitespace only, 1 distinct = one repeated character.
    compact = "".join(message.split())
    return len(set(compact)) <= 1


@router.post(
    "/lead",
    response_model=LeadResponse,
    status_code=201,
    responses={
        400: {"model": ErrorResponse, "description": "Business rule rejected the lead"},
        422: {"model": ErrorResponse, "description": "Request validation failed"},
    },
)
def create_lead(lead: LeadRequest):
    if is_disposable_email(lead.email):
        logger.warning("Rejected lead: disposable email (%s)", lead.email)
        raise DisposableEmailError()

    if is_low_effort_message(lead.message):
        logger.warning("Rejected lead: low-effort message from %s", lead.email)
        raise LowEffortMessageError()

    lead_id = str(uuid.uuid4())
    logger.info("Lead created: %s (%s)", lead_id, lead.email)

    return LeadResponse(
        lead_id=lead_id,
        name=lead.name,
        email=lead.email,
        company=lead.company,
        message=lead.message,
        received_at=datetime.now(timezone.utc),
    )