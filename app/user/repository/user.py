from app.user.model import User
from core.repository import BaseRepoORM


class UserRepo(BaseRepoORM):
    model = User
