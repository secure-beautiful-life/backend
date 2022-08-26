from typing import Callable, Awaitable
from uuid import uuid4

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response, StreamingResponse

from core.fastapi.middlewares.logger.model import RequestLog, ResponseLog
from core.fastapi.middlewares.logger.repository import RequestLogRepo, ResponseLogRepo


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(
            self, request: Request, call_next: Callable[[Request], Awaitable[StreamingResponse]],
    ) -> Response:
        response = await call_next(request)
        session_id = str(uuid4())

        reqeust_log = {
            "session_id": session_id,
            "method": request.method,
            "url": request.url.path,
            "host": request.client.host,
            "port": request.client.port,
            "user_agent": request.headers.get("user-agent"),
            "content_type": request.headers.get("content-type"),
            "origin": request.headers.get("origin"),
            "referer": request.headers.get("referer"),
            "user_id": request.user.id,
            "user_token": request.user.token,
        }
        await RequestLogRepo().save(model=RequestLog(**reqeust_log))

        response_log = {
            "session_id": session_id,
            "status_code": int(response.status_code),
        }
        await ResponseLogRepo().save(model=ResponseLog(**response_log))

        return response
