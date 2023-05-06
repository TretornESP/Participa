from app.config import Config
import boto3
from app.controller.route_master import RouteMaster
import logging

class S3Repository:
    def __init__(self):
        cfg = Config()
        self.config = cfg.toDict()['aws']
        self.log = cfg.log
        self.session = boto3.Session(
            aws_access_key_id=self.config['key_id'],
            aws_secret_access_key=self.config['key'],
            region_name=self.config['region']
        )
        self.s3 = self.session.resource('s3')
        self.photo_bucket = self.config['photo_bucket']
        logging.getLogger('boto3').setLevel(logging.WARNING)
        logging.getLogger('botocore').setLevel(logging.WARNING)
        logging.getLogger('nose').setLevel(logging.WARNING)        
        
    def download_file(self, key, filename):
        self.s3.Bucket(self.photo_bucket).download_file(key, filename)
        return True

    def upload_file(self, filename, key):
        self.s3.Bucket(self.photo_bucket).upload_file(filename, key)
        return True

    def get_presigned_url(self, key):
        return self.s3.meta.client.generate_presigned_url(
            'get_object',
            Params={
                'Bucket': self.photo_bucket,
                'Key': key
            },
            ExpiresIn=3600
        )

    def upload_fileobj(self, fileobj, key, content_type):
        #Fileobj is a BytesIO object
        RouteMaster.log("Uploading file to S3: " + str(key))
        RouteMaster.log("AWS config: " + str(self.config))
        self.s3.Bucket(self.photo_bucket).put_object(Key=key, Body=fileobj, ContentType=content_type)
        
        return key