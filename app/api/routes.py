from fastapi import APIRouter

from app.schemas.generate import (
    ErrorResponse,
    GenerateRequest,
    GenerateResponse,
)
from app.services.generator import generate

router = APIRouter()


@router.get("/health")
def health():
    return {"status": "ok", "version": "0.1.0"}


@router.post(
    "/generate",
    response_model=GenerateResponse,
    responses={
        400: {"description": "Validation error", "model": ErrorResponse},
        500: {"description": "Internal error", "model": ErrorResponse},
    },
)
def generate_api(payload: GenerateRequest):
    return generate(payload)