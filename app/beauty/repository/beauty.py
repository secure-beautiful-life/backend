from core.repository import BaseRepoORM

from app.beauty.model import Beauty


class BeautyRepo(BaseRepoORM):
    model = Beauty
