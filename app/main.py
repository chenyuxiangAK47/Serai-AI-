import uuid
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from app.api.routes import router
from app.core.config import settings

app = FastAPI(title=settings.app_name, version=settings.version)
app.include_router(router)

import time
import logging
logger = logging.getLogger("serai")
logging.basicConfig(level=logging.INFO)

@app.middleware("http")
async def request_id_middleware(request: Request, call_next):
    rid = request.headers.get("X-Request-Id") or str(uuid.uuid4())
    request.state.request_id = rid

    start = time.time()
    response = await call_next(request)
    ms = int((time.time() - start) * 1000)

    response.headers["X-Request-Id"] = rid
    logger.info(f"{request.method} {request.url.path} {response.status_code} {ms}ms rid={rid}")
    return response

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    rid = getattr(request.state, "request_id", "unknown")
    return JSONResponse(
        status_code=400,
        content={
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "invalid request body",
                "request_id": rid,
            }
        },
    )

@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    rid = getattr(request.state, "request_id", "unknown")
    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "code": "INTERNAL_ERROR",
                "message": "internal error",
                "request_id": rid,
            }
        },
    )