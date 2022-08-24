import os.path
import uuid
from base64 import b64decode
from io import BytesIO
from typing import Tuple, Optional

from PIL import Image

from core.config import config
from core.exceptions import BadRequestException


class ImageHelper:
    @staticmethod
    def analyze_image(image_string: str) -> Optional[Tuple[str, int, BytesIO]]:
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

        return image_type, image_size, buffer

    @staticmethod
    def upload_image(image_string: str, saved_path: str) -> Tuple[int, str, str]:
        image_type, image_size, buffer = ImageHelper.analyze_image(image_string)
        saved_name = f"{uuid.uuid4()}.{image_type}"
        saved_path = os.path.join(saved_path, saved_name)

        with open(saved_path, "wb") as f:
            f.write(buffer.getbuffer().tobytes())

        return image_size, image_type, saved_name

    @staticmethod
    def upload_images(images: list, saved_path: str) -> Optional[Tuple[list, list, list]]:
        image_size_list, image_type_list, saved_name_list = [], [], []

        for image in images:
            image_string, file_name = image['image_string'], image['file_name']
            image_size, image_type, saved_name = ImageHelper.upload_image(image_string, saved_path)
            image_size_list.append(image_size), image_type_list.append(image_type), saved_name_list.append(saved_name)

        return image_size_list, image_type_list, saved_name_list
