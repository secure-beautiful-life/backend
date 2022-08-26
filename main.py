from os import path
from typing import List

from fastapi import FastAPI, Request, Depends
from fastapi.exceptions import RequestValidationError
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles

from app import router
from core.config import config
from core.exceptions import CustomException, BadRequestException, UnauthorizedException
from core.fastapi.dependencies import PermissionDependency
from core.fastapi.middlewares import (
    AuthenticationMiddleware,
    AuthBackend,
    SQLAlchemyMiddleware,
)
from core.fastapi.middlewares.logger.service import LoggingMiddleware


def init_routers(app_: FastAPI) -> None:
    app_.include_router(router, dependencies=[Depends(PermissionDependency())])
    app_.mount("/media", StaticFiles(directory=path.join(config.BASE_DIR, "media")), name="media")
    app_.mount("/static", StaticFiles(directory=path.join(config.BASE_DIR, "templates", "static")), name="static")


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
    custom_exception = exc.args[0] if len(exc.args) else None
    status_code = int(custom_exception.code) if hasattr(custom_exception, "code") else UnauthorizedException.code
    error_code = custom_exception.error_code if hasattr(custom_exception,
                                                        "error_code") else UnauthorizedException.error_code
    message = custom_exception.message if hasattr(custom_exception, "message") else UnauthorizedException.message

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
        Middleware(LoggingMiddleware),
    ]
    return middleware


def create_app() -> FastAPI:
    app_ = FastAPI(
        title="Beautiful Life",
        description="Beautiful Life",
        version="0.1.0",
        docs_url=config.DOCS_URL,
        redoc_url=config.REDOC_URL,
        middleware=make_middleware(),
    )
    init_routers(app_=app_)
    init_listeners(app_=app_)
    return app_


app = create_app()


@app.get("/{full_path:path}")
async def render_spa(full_path: str):
    index_html_path = path.join(config.BASE_DIR, "templates", "index.html")

    with open(index_html_path, "rt", encoding="UTF-8") as f:
        index_html = f.read()

    return HTMLResponse(content=index_html, status_code=200)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app="main:app",
        host=config.APP_HOST,
        port=config.APP_PORT,
        reload=True if config.RUNNING_ENV != "production" else False,
        workers=4
    )
