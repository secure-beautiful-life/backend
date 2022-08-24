from typing import Callable, Awaitable
from uuid import uuid4

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response, StreamingResponse

from core.fastapi.middlewares.logger.model import RequestLog, ResponseLog
from core.fastapi.middlewares.logger.repository import RequestLogRepo, ResponseLogRepo


# REDACTED_KEYS = ["password", "password_check", "prev_password"]


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(
            self, request: Request, call_next: Callable[[Request], Awaitable[StreamingResponse]],
    ) -> Response:
        response = await call_next(request)
        # response_body = [section async for section in response.body_iterator]
        # response.body_iterator = iterate_in_threadpool(iter(response_body))
        session_id = str(uuid4())

        # try:
        #     request_json = deepcopy(await request.json())
        #     for key in REDACTED_KEYS:
        #         if key in request_json:
        #             request_json[key] = "!==Redacted==!"
        #
        # except JSONDecodeError:
        #     request_json = None

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
            # "request_json": request_json
        }
        await RequestLogRepo().save(model=RequestLog(**reqeust_log))

        response_log = {
            "session_id": session_id,
            "status_code": response.status_code,
            # "response_json": json.loads(response_body[0].decode("utf-8"))
        }
        await ResponseLogRepo().save(model=ResponseLog(**response_log))

        return response
