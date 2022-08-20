from app.auth.model import AuthRoleHierarchy
from core.repository import BaseRepoORM


class AuthRoleHierarchyRepo(BaseRepoORM):
    model = AuthRoleHierarchy
