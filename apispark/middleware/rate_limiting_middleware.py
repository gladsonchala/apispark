from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from collections import defaultdict
import time

class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, limit: int = 100, window: int = 60):
        super().__init__(app)
        self.limit = limit
        self.window = window
        self.clients = defaultdict(list)

    async def dispatch(self, request, call_next):
        client_ip = request.client.host
        current_time = time.time()
        if client_ip not in self.clients:
            self.clients[client_ip] = []
        self.clients[client_ip] = [t for t in self.clients[client_ip] if t > current_time - self.window]
        if len(self.clients[client_ip]) >= self.limit:
            return JSONResponse({"message": "Rate limit exceeded"}, status_code=429)
        self.clients[client_ip].append(current_time)
        response = await call_next(request)
        return response
