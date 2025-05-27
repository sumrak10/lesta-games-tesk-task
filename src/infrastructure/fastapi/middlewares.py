from time import perf_counter

from fastapi.requests import Request
from starlette.middleware.base import BaseHTTPMiddleware


class ProcessTimeHeaderMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, service_name: str | None = None, header_name: str = 'X-Process-Time'):
        super().__init__(app)
        self.header_name = header_name if service_name is None else f'{header_name}-{service_name}'

    async def dispatch(self, request: Request, call_next):
        start_time = perf_counter()
        response = await call_next(request)
        time = str(round(float(perf_counter() - start_time), 6))
        response.headers[self.header_name] = time
        return response
