from core.fastapi.middlewares.logger.model import RequestLog

from core.repository import BaseRepoORM


class RequestLogRepo(BaseRepoORM):
    model = RequestLog
