import logging
from fastapi import Request
import time
import uuid
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)


#async def log_requests(request: Request, call_next):
    # Before FastAPI handles the request:
    #logger.info(f"Received: {request.method} {request.url.path}")

    # FastAPI handles the request
    #response = await call_next(request)

    # After FastAPI produces a response:
    #logger.info(f"Returned: status={response.status_code}")
    #return response

async def log_requests(request: Request, call_next):
    request_id = uuid.uuid4().hex[:8]
    request.state.request_id = request_id
    started = time.perf_counter()

    try:
        response = await call_next(request)
    except Exception:
        logger.error(f"Unexpected failure: request_id={request_id}",exc_info=True)
        response = JSONResponse(status_code=500,content={"detail": "Internal server error"})

    duration_ms = (time.perf_counter() - started) * 1000
    message = (
        f"request_id={request_id} {request.method} {request.url.path} "
        f"status={response.status_code} duration={duration_ms:.1f}ms"
    )

    if response.status_code >= 500:
        logger.error(message)
    elif 400 <= response.status_code < 500:
        logger.warning(message)
    else:
        logger.info(message)

    response.headers["X-Request-ID"] = request_id
    return response