import hashlib
import logging

from app.core.config import settings
from app.schemas.generate import GenerateRequest, GenerateResponse
from app.services.cache import cache

logger = logging.getLogger("serai")


def _cache_key(req: GenerateRequest) -> str:
    raw = f"{req.brand}|{req.event}|{req.context}".encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def generate(req: GenerateRequest) -> GenerateResponse:
    k = _cache_key(req)
    if k in cache:
        logger.info("cache_hit key=%s", k[:16])
        return cache[k]

    mode = settings.generator_mode.lower()
    if mode == "llm":
        if not settings.llm_api_key:
            out = GenerateResponse(
                summary="stub summary (llm mode but no key configured)",
                risks=["stub risk 1", "stub risk 2"],
                recommendation="stub recommendation",
            )
            cache[k] = out
            return out

    out = GenerateResponse(
        summary="stub summary",
        risks=["stub risk 1", "stub risk 2"],
        recommendation="stub recommendation",
    )
    cache[k] = out
    return out