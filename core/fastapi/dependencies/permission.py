from fastapi import Request
from fastapi.openapi.models import HTTPBearer
from fastapi.security.base import SecurityBase

from app.auth.service import AuthService
from core.exceptions import ForbiddenException
from core.utils import UrlMatcher


class PermissionDependency(SecurityBase):
    def __init__(self):
        self.model = HTTPBearer()
        self.scheme_name = self.__class__.__name__

    async def __call__(self, request: Request) -> None:
        if request.user.role_id == 1:
            return

        resources = await AuthService().get_resource_list(method=request.method)

        matched_resource = None
        for resource in resources:
            if UrlMatcher.match(resource.url, request.url.path):
                matched_resource = resource

        if not matched_resource:
            return

        if not request.user.id:
            raise ForbiddenException

        if request.user.role_id == matched_resource.role_id:
            return

        role_priority = await AuthService().get_role_priority(convert=False)

        if role_priority.index(matched_resource.role_id) < role_priority.index(request.user.role_id):
            raise ForbiddenException
