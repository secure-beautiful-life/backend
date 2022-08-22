from typing import Optional, Type, List, Union

from app.auth.model import AuthRole, AuthRoleHierarchy, AuthResource
from app.auth.repository import AuthResourceRepo, AuthRoleRepo, AuthRoleHierarchyRepo
from core.exceptions import NotFoundException, BadRequestException, DuplicatedDataException


class AuthService:
    def __init__(self):
        self.resource_repo = AuthResourceRepo()
        self.role_repo = AuthRoleRepo()
        self.role_hierarchy_repo = AuthRoleHierarchyRepo()

    async def convert_role_id_list_to_role_name_list(self, id_list: List[int]) -> List[str]:
        name_list = []
        for id in id_list:
            role = await self.role_repo.filter_by(params=dict(id=id))
            if not role:
                raise BadRequestException(message="권한 id 목록이 올바르지 않습니다.")
            if role.name in name_list:
                raise BadRequestException(message="권한 id 목록이 올바르지 않습니다.")
            name_list.append(role.name)

        return name_list

    async def convert_role_name_list_to_role_id_list(self, name_list: List[str]) -> List[int]:
        id_list = []
        for name in name_list:
            role = await self.role_repo.filter_by(params=dict(name=name))
            if not role:
                raise BadRequestException(message="권한 이름 목록이 올바르지 않습니다.")
            if role.id in id_list:
                raise BadRequestException(message="권한 이름 목록이 올바르지 않습니다.")
            id_list.append(role.id)

        return id_list

    async def get_role_hierarchy(self) -> List[Type[AuthRoleHierarchy]]:
        return await self.role_hierarchy_repo.get_list()

    async def get_role_priority(self, convert: bool = True) -> Optional[List[Union[str, int]]]:
        hierarchy = await self.get_role_hierarchy()
        role_priority = [1]
        child = 1
        while child:
            child = hierarchy[child - 1].child_role_id
            if child:
                role_priority.append(child)

        if convert:
            return await self.convert_role_id_list_to_role_name_list(id_list=role_priority)
        return role_priority

    async def update_role_hierarchy(self, priority_list: List[str]) -> None:
        priority_list = await self.convert_role_name_list_to_role_id_list(name_list=priority_list)

        if priority_list[0] != 1:
            raise BadRequestException(message="최상위 권한의 우선순위는 변경할 수 없습니다.")

        for priority, role_id in enumerate(priority_list):
            child_role_id = priority_list[priority + 1] if (priority + 1) < len(priority_list) else None
            await self.role_hierarchy_repo.update_by_id(id=role_id, params=dict(child_role_id=child_role_id))

    async def create_role(self, name: str, description: Optional[str] = None) -> Optional[int]:
        if await self.role_repo.filter_by(params=dict(name=name)):
            raise DuplicatedDataException("이미 존재하는 권한 이름입니다.")

        created_obejct = await self.role_repo.save(AuthRole(name=name, description=description))
        created_obejct_id = created_obejct.id
        parent = await self.role_hierarchy_repo.filter_by(params=dict(child_role_id=None))
        await self.role_hierarchy_repo.update_by_id(id=parent.id, params=dict(child_role_id=created_obejct_id))
        await self.role_hierarchy_repo.save(model=AuthRoleHierarchy(parent_role_id=created_obejct_id))
        return created_obejct_id

    async def get_role_by_id(self, id: int) -> Optional[Type[AuthRole]]:
        role = await self.role_repo.get_by_id(id=id)
        if not role:
            raise NotFoundException(message="존재하지 않는 권한 id입니다.")
        return role

    async def get_role_by_name(self, name: str) -> Optional[Type[AuthRole]]:
        role = await self.role_repo.filter_by(params=dict(name=name))
        if not role:
            raise NotFoundException(message="존재하지 않는 권한 이름입니다.")
        return role

    async def get_role_list(self, limit: int = 10, offset: Optional[int] = None) -> List[Type[AuthRole]]:
        return await self.role_repo.get_list(limit=limit, offset=offset)

    async def get_role_count(self) -> int:
        return await self.role_repo.count_all()

    async def update_role_by_id(self, id: int, name: Optional[str] = None, description: Optional[str] = None) -> \
            Optional[int]:
        if not (name or description):
            raise BadRequestException(message="수정할 정보가 없습니다.")

        await self.get_role_by_id(id=id)

        if await self.role_repo.filter_by(params=dict(name=name)):
            raise DuplicatedDataException("이미 존재하는 권한 이름입니다.")

        return await self.role_repo.update_by_id(id=id, params=dict(name=name, description=description))

    # async def delete_role_by_id(self, id: int) -> Optional[int]:
    #     if id == 1:
    #         raise BadRequestException(message="최상위 권한은 삭제할 수 없습니다.")
    #
    #     await self.get_role_by_id(id=id)
    #     parent_role_hierarchy = await self.role_hierarchy_repo.filter_by(params=dict(child_role_id=id))
    #     role_hierarchy = await self.role_hierarchy_repo.filter_by(params=dict(parent_role_id=id))
    #     role_hierarchy_id = role_hierarchy.id
    #     await self.role_hierarchy_repo.update_by_id(id=parent_role_hierarchy.id,
    #                                                 params=dict(child_role_id=role_hierarchy_id))
    #     await self.role_hierarchy_repo.delete_by_id(id=role_hierarchy_id)
    #
    #     return await self.role_repo.delete_by_id(id=id)

    async def create_resource(self, method: str, url: str, role_name: str) -> Optional[int]:
        if await self.resource_repo.filter_by(params=dict(method=method, url=url)):
            raise DuplicatedDataException(message="동일한 method와 url로 구성된 설정이 이미 존재합니다.")

        role = await self.get_role_by_name(name=role_name)

        created_obejct = await self.resource_repo.save(AuthResource(method=method, url=url, role_id=role.id))
        return created_obejct.id

    async def get_resource_by_id(self, id: int) -> Optional[Type[AuthRole]]:
        resource = await self.resource_repo.get_by_id(id=id)
        if not resource:
            raise NotFoundException(message="존재하지 않는 자원 id입니다.")
        return resource

    async def get_resource_list(self, limit: int = 10, offset: Optional[int] = None, method: Optional[str] = None):
        return await self.resource_repo.get_resource_list(limit=limit, offset=offset, method=method)

    async def get_resource_count(self) -> int:
        return await self.resource_repo.count_all()

    async def update_resource_by_id(self, id: int, method: Optional[str] = None, url: Optional[str] = None,
                                    role_name: Optional[str] = None) -> Optional[int]:
        if not (method or url or role_name):
            raise BadRequestException(message="수정할 정보가 없습니다.")

        await self.get_resource_by_id(id=id)
        role = await self.get_role_by_name(name=role_name)

        return await self.resource_repo.update_by_id(id=id, params=dict(method=method, url=url, role_id=role.id))

    async def delete_resource_by_id(self, id: int) -> Optional[int]:
        await self.get_resource_by_id(id=id)
        return await self.resource_repo.delete_by_id(id=id)
