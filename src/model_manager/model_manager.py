import boto3
from ..settings import settings
import tempfile


def get_s3_client():
    session=boto3.Session(
            aws_access_key_id=settings.aws_accesskey_id,
            aws_secret_access_key=settings.aws_secret_access_key
        )
    return session.resource('s3')

def handle_new_model(file):
    s3=get_s3_client()
    model_bucket=s3.Bucket(settings.aws_bucket_name)
    return model_bucket.upload_file(file,'model.h5')

def get_model():
    s3=get_s3_client()
    model_bucket=s3.Bucket(settings.aws_bucket_name)
    with tempfile.TemporaryFile(mode='w+b') as file:
        model_bucket.download_file('model.h5',file.name)
    return file