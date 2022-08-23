from typing import List

from fastapi import FastAPI, Request, Depends
from fastapi.exceptions import RequestValidationError
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app import router
from core.config import config
from core.exceptions import CustomException, BadRequestException, UnauthorizedException
from core.fastapi.dependencies import PermissionDependency
from core.fastapi.middlewares import (
    AuthenticationMiddleware,
    AuthBackend,
    SQLAlchemyMiddleware,
)


def init_routers(app_: FastAPI) -> None:
    app_.include_router(router, dependencies=[Depends(PermissionDependency())])


def init_listeners(app_: FastAPI) -> None:
    @app_.exception_handler(CustomException)
    async def custom_exception_handler(request: Request, exc: CustomException):
        return JSONResponse(
            status_code=exc.code,
            content={"error_code": exc.error_code, "message": exc.message},
        )

    @app_.exception_handler(RequestValidationError)
    async def request_validation_error_handler(request: Request, exc: RequestValidationError):
        return JSONResponse(
            status_code=BadRequestException.code,
            content={"error_code": BadRequestException.error_code, "message": exc.errors()[0]["msg"]},
        )


def on_auth_error(request: Request, exc: Exception):
    status_code = UnauthorizedException.code
    error_code = UnauthorizedException.error_code
    message = UnauthorizedException.message
    raised_exception = exc.args[0] if len(exc.args) else None

    if (hasattr(raised_exception, "code") and hasattr(raised_exception, "error_code")
            and hasattr(raised_exception, "message")):
        status_code = int(raised_exception.code)
        error_code = raised_exception.error_code
        message = raised_exception.message

    return JSONResponse(
        status_code=status_code,
        content={"error_code": error_code, "message": message},
    )


def make_middleware() -> List[Middleware]:
    middleware = [
        Middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        ),
        Middleware(SQLAlchemyMiddleware),
        Middleware(
            AuthenticationMiddleware,
            backend=AuthBackend(),
            on_error=on_auth_error,
        ),
    ]
    return middleware


def create_app() -> FastAPI:
    app_ = FastAPI(
        title="FastAPI Test",
        description="FastAPI Test API",
        version="0.1.0",
        docs_url=config.DOCS_URL,
        redoc_url=config.REDOC_URL,
        middleware=make_middleware(),
    )
    init_routers(app_=app_)
    init_listeners(app_=app_)
    return app_


app = create_app()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app="main:app",
        host=config.APP_HOST,
        port=config.APP_PORT,
        reload=True if config.RUNNING_ENV != "production" else False,
        workers=4
    )
