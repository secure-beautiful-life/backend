from app.user.model import UserInfo
from core.repository import BaseRepoORM


class UserInfoRepo(BaseRepoORM):
    model = UserInfo
