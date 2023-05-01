import time
import base64
from app.repository.s3_repository import S3Repository
from app.controller.route_master import RouteMaster
from app.util.cryptography_util import CryptographyUtil
from PIL import Image
from io import BytesIO

class UploadsService:
    def __init__(self):
        pass

    @staticmethod
    def upload_photo(file, user_id):
        repository = S3Repository()
        try:
            image = Image.open(file)
            image.thumbnail((300, 300), Image.ANTIALIAS)
            RouteMaster.log("Image size: " + str(image.size))
            buffered = BytesIO()
            image.save(buffered, format="JPEG")
            RouteMaster.log("Buffered size: " + str(buffered.getbuffer().nbytes))
            content_type = "image/jpeg"
        except Exception as e:
            RouteMaster.log("Error uploading photo: " + str(e))
            return None

        return str(repository.upload_fileobj(buffered, str(user_id) + "/" + str(CryptographyUtil.generate_image_key()) + ".jpg", content_type))