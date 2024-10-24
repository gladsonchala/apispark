from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from apispark.utils.helpers import log_error

async def custom_exception_handler(request: Request, exc: Exception):
    log_error("An unexpected error occurred.", exc)
    return JSONResponse(
        status_code=500,
        content={"message": "An internal server error occurred."}
    )

async def http_exception_handler(request: Request, exc: HTTPException):
    log_error(f"HTTP Exception: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail}
    )
