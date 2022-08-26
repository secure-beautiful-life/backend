import uuid
from typing import Optional

from app.beauty.model import Beauty
from app.beauty.repository import BeautyRepo
from app.product.service import ProductService
from app.user.service import UserService
from core.config import config
from core.exceptions import ForbiddenException
import os
import subprocess
import random
import shutil

import os
import subprocess
import random
import shutil


class BeautyService:
    def __init__(self):
        self.beauty_repo = BeautyRepo()

    async def get_beauty_list_desc(self, limit: int = 10, offset: Optional[int] = None):
        return await self.beauty_repo.get_list_desc(limit=limit, offset=offset)

    async def get_beauty(self, beauty_id: int):
        beauty = await self.beauty_repo.get_by_id(beauty_id)

        if not beauty:
            raise ValueError("해당하는 뷰티 아이디를 찾을 수 없습니다.")

        return beauty

    async def create_beauty(self, user_id: int, product_id: int):
        user = await UserService().get_user_by_id(user_id)
        product = await ProductService().get_product_by_id(product_id)
        self.makeup(product.beauty_image[0].saved_name, user.profile_image[0].saved_name)

        saved_file_name = str(uuid.uuid4()) + ".png"
        shutil.copyfile("/home/hbk/backend/result.png", "/home/hbk/backend/media/beauty_images/" + saved_file_name)

        beauty = await self.beauty_repo.save(
            Beauty(
                user_id=user_id,
                product_id=product_id,
                saved_name="/media/beauty_images/" + saved_file_name,
            )
        )

        return beauty

    async def delete_beauty(self, user_id: int, beauty_id: int):
        await UserService().get_user_by_id(user_id)

        beauty = self.get_beauty(beauty_id)

        if user_id != beauty.user_id:
            raise ForbiddenException("본인의 가상 뷰티 이미지만 삭제할 수 있습니다.")

        self.beauty_repo.delete_by_id(beauty.id)

    def makeup(self, product_file_name, profile_file_name):
        cmd = f'CUDA_VISIBLE_DEVICES=0 /home/hbk/anaconda3/envs/cpm/bin/python3.7 ./CPM/main.py  ' \
              f'--style {config.PRODUCT_IMAGE_DIR}/{product_file_name} ' \
              f'--input {config.USER_PROFILE_IMAGE_DIR}/{profile_file_name} ' \
              f'--savedir {config.BEAUTY_IMAGE_DIR}'
        process = subprocess.Popen(cmd,stdout=subprocess.PIPE, shell=True)