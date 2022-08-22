from app.auth.model import AuthRole
from core.repository import BaseRepoORM


class AuthRoleRepo(BaseRepoORM):
    model = AuthRole
