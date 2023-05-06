import time
import base64
from app.repository.s3_repository import S3Repository
from app.controller.route_master import RouteMaster
from app.util.cryptography_util import CryptographyUtil
from app.config import Config
from PIL import Image, ImageOps
from io import BytesIO

class UploadsService:
    def __init__(self):
        pass

    @staticmethod
    def upload_photo(file, user_id):
        repository = S3Repository()
        try:
            #Save as png
            image = Image.open(file).convert('RGB')
            image = ImageOps.exif_transpose(image)
            RouteMaster.log("Image size: " + str(image.size))
            buffered = BytesIO()
            image.save(buffered, format="PNG")
            RouteMaster.log("Buffered size: " + str(buffered.getbuffer().nbytes))
            content_type = "image/png"
            buffered.seek(0)
        except Exception as e:
            RouteMaster.log("Error uploading photo: " + str(e))
            return None

        return repository.upload_fileobj(buffered, str(user_id) + "/" + str(CryptographyUtil.generate_image_key()) + ".png", content_type)

    @staticmethod
    def presign(key):
        repository = S3Repository()
        return repository.get_presigned_url(key)