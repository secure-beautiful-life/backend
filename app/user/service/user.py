import os
import uuid
from base64 import b64decode
from datetime import datetime, timedelta
from io import BytesIO
from typing import Optional, Type, List
from zoneinfo import ZoneInfo

import bcrypt
from PIL import Image

from app.auth.service import AuthService
from app.user.model import User, UserInfo, UserProfileImage
from app.user.repository import UserRepo, UserInfoRepo, UserProfileImageRepo
from core.config import config
from core.exceptions import (
    BadRequestException,
    NotFoundException,
    DuplicatedDataException,
    UserAuthenticationFailedException, UserLoginForbiddenException
)
from core.utils.token_helper import TokenHelper


class UserService:
    def __init__(self):
        self.user_repo = UserRepo()
        self.info_repo = UserInfoRepo()
        self.profile_repo = UserProfileImageRepo()

    async def create_user(self, username: str, password: str, role_id: int, type_: str, gender: str, email: str,
                          phone: str, address: str, brand_name: Optional[str] = None, **kwargs) -> Optional[int]:
        if await self.user_repo.filter_by(params=dict(username=username)):
            raise DuplicatedDataException(message="이미 존재하는 아이디입니다.")

        await AuthService().get_role_by_id(id=role_id)

        if await self.info_repo.filter_by(params=dict(email=email)):
            raise DuplicatedDataException(message="이미 사용 중인 이메일입니다.")

        if await self.info_repo.filter_by(params=dict(phone=phone)):
            raise DuplicatedDataException(message="이미 사용 중인 전화번호입니다.")

        if type_ == "brand":
            if not brand_name:
                raise BadRequestException(message="브랜드 이름을 입력해 주세요.")
            if await self.info_repo.filter_by(params=dict(brand_name=brand_name)):
                raise DuplicatedDataException(message="이미 사용 중인 브랜드 이름입니다.")

        user = await self.user_repo.save(
            model=User(
                username=username,
                password=bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8"),
                role_id=role_id
            )
        )
        user_id = user.id
        await self.info_repo.save(
            model=UserInfo(
                user_id=user.id,
                type=type_,
                brand_name=brand_name,
                gender=gender,
                email=email,
                phone=phone,
                address=address
            )
        )
        return user_id

    async def get_user_by_id(self, id: int) -> Optional[Type[User]]:
        user = await self.user_repo.get_by_id(id=id)
        if not user:
            raise NotFoundException("존재하지 않는 사용자 id입니다.")
        return user

    async def get_user_list(self, limit: int = 10, offset: Optional[int] = None) -> List[Type[User]]:
        return await self.user_repo.get_list(limit=limit, offset=offset)

    async def get_user_count(self) -> int:
        return await self.user_repo.count_all()

    async def update_password_by_id(self, id: int, prev_password: str, password: str, **kwargs) -> Optional[int]:
        user = await self.get_user_by_id(id=id)

        if not bcrypt.checkpw(prev_password.encode("utf-8"), user.password.encode("utf-8")):
            raise BadRequestException(message="비밀번호가 틀립니다.")

        return await self.user_repo.update_by_id(
            id=id,
            params=dict(password=bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()))
        )

    async def update_info_by_id(self, id: int, email: Optional[str] = None, phone: Optional[str] = None,
                                address: Optional[str] = None):
        if not (email or phone or address):
            raise BadRequestException(message="수정할 정보가 없습니다.")

        params = {}
        if email:
            if await self.info_repo.filter_by(params=dict(email=email)):
                raise DuplicatedDataException(message="이미 사용 중인 이메일입니다.")
            params["email"] = email

        if phone:
            if await self.info_repo.filter_by(params=dict(phone=phone)):
                raise DuplicatedDataException(message="이미 사용 중인 전화번호입니다.")
            params["phone"] = phone

        if address:
            params["address"] = address

        return await self.info_repo.update_by_id(id=id, params=params)

    async def delete_user_by_id(self, id: int) -> Optional[int]:
        if id == 1:
            raise BadRequestException(message="최고 관리자 계정은 삭제할 수 없습니다.")

        await self.get_user_by_id(id=id)

        user_profile = await self.profile_repo.filter_by(params=dict(user_id=id))
        if user_profile:
            await self.delete_user_profile_by_user_id(user_id=id)
        return await self.user_repo.delete_by_id(id=id)

    async def create_user_profile_by_user_id(self, user_id: int, image_string: str, file_name: str) -> Optional[int]:
        await self.get_user_by_id(id=user_id)

        try:
            image_string = image_string[image_string.find(",") + 1:]
            image = Image.open(BytesIO(b64decode(image_string)))
        except Exception:
            raise BadRequestException(message="유효하지 않은 이미지입니다.")

        image_type = image.format
        if image_type not in config.ALLOWED_IMAGE_TYPES:
            raise BadRequestException(message="허용되지 않은 이미지 형식입니다.")

        buffer = BytesIO()
        image.save(buffer, format=image_type)
        image_size = buffer.tell()

        if image_size > config.MAX_IMAGE_SIZE:
            raise BadRequestException(message="이미지 크기가 허용치를 초과하였습니다.")

        saved_name = f"{uuid.uuid4()}.{image_type}"
        saved_path = os.path.join(config.USER_PROFILE_IMAGE_DIR, saved_name)

        with open(saved_path, "wb") as f:
            f.write(buffer.getbuffer().tobytes())

        created_object = await self.profile_repo.save(
            model=UserProfileImage(user_id=user_id, uploaded_name=file_name, saved_name=saved_name, size=image_size,
                                   type=image_type))
        return created_object.id

    async def delete_user_profile_by_user_id(self, user_id: int) -> Optional[int]:
        await self.get_user_by_id(id=user_id)
        profile = await self.profile_repo.filter_by(params=dict(user_id=user_id))
        if not profile:
            raise NotFoundException(message="존재하지 않는 프로필입니다.")

        image_path = os.path.join(config.USER_PROFILE_IMAGE_DIR, profile.saved_name)
        if os.path.exists(image_path):
            os.remove(image_path)

        return await self.profile_repo.delete_by_id(id=profile.id)

    async def login(self, username: str, password: str) -> dict:
        user = await self.user_repo.filter_by(params=dict(username=username))
        if not user:
            raise UserAuthenticationFailedException

        user_id = user.id
        user_login_failed_count = user.login_failed_count
        now = datetime.now(tz=ZoneInfo(config.APP_TIMEZONE))

        if user.login_forbidden_time:
            if now.replace(tzinfo=ZoneInfo("UTC")) < user.login_forbidden_time.replace(tzinfo=ZoneInfo("UTC")):
                raise UserLoginForbiddenException

        if not bcrypt.checkpw(password.encode("utf-8"), user.password.encode("utf-8")):
            user_login_failed_count += 1
            if user_login_failed_count >= config.MAX_LOGIN_ATTEMPT:
                await self.user_repo.update_by_id(id=user_id, params=dict(
                    login_forbidden_time=now + timedelta(minutes=config.LOGIN_FORBIDDEN_TIME)
                ))
            await self.user_repo.update_by_id(id=user_id, params=dict(
                login_failed_count=user_login_failed_count
            ))
            raise BadRequestException(message="비밀번호가 틀립니다.")

        await self.user_repo.update_by_id(id=user_id, params=dict(
            login_failed_count=0,
            login_forbidden_time=None
        ))

        access_token = TokenHelper.encode(payload={"user_id": user_id})
        refresh_token = TokenHelper.encode(payload={"user_id": user_id}, refresh=True)

        return dict(access_token=access_token, refresh_token=refresh_token)

    @staticmethod
    def refresh(refresh_token: str) -> dict:
        return dict(access_token=TokenHelper.refresh(refresh_token))
