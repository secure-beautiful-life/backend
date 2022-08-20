from app.user.model import UserProfileImage
from core.repository import BaseRepoORM


class UserProfileImageRepo(BaseRepoORM):
    model = UserProfileImage
