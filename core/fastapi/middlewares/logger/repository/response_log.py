from core.fastapi.middlewares.logger.model import ResponseLog

from core.repository import BaseRepoORM


class ResponseLogRepo(BaseRepoORM):
    model = ResponseLog
