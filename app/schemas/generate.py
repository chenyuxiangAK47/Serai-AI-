from pydantic import BaseModel, Field


class GenerateRequest(BaseModel):
    brand: str = Field(min_length=1, max_length=100)
    event: str = Field(min_length=1, max_length=200)
    context: str = Field(min_length=1, max_length=4000)


class GenerateResponse(BaseModel):
    summary: str
    risks: list[str]
    recommendation: str


class ErrorDetail(BaseModel):
    code: str
    message: str
    request_id: str


class ErrorResponse(BaseModel):
    error: ErrorDetail