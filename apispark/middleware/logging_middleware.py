import time
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        formatted_time = f"{process_time:.4f}s"
        log_details = {
            "method": request.method,
            "url": request.url.path,
            "status_code": response.status_code,
            "process_time": formatted_time
        }
        print(f"Request: {log_details['method']} {log_details['url']} | "
              f"Status: {log_details['status_code']} | Time: {log_details['process_time']}")
        return response
