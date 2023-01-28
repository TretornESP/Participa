import time
import base64
from app.repository.mongo_repository import MongoRepository
from app.controller.route_master import RouteMaster
from PIL import Image
from io import BytesIO

class UploadsService:
    def __init__(self):
        pass

    @staticmethod
    def upload_photo(file, user_id):
        repository = MongoRepository()
        try:
            image = Image.open(file)
            image.thumbnail((300, 300), Image.ANTIALIAS)
            RouteMaster.log("Image size: " + str(image.size))
            buffered = BytesIO()
            image.save(buffered, format="JPEG")

            photo = {
                "expires": int(time.time()) + 3600,
                "user_id": str(user_id),
                "uses": 0,
                "data": base64.b64encode(buffered.getvalue()).decode('utf-8')
            }
        except Exception as e:
            RouteMaster.log("Error uploading photo: " + str(e))
            return None

        return str(repository.upload_photo(photo))