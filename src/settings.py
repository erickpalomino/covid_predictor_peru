from dotenv import load_dotenv
import os

load_dotenv()

class Settings():

    def __init__(self):
        self.db_name = os.environ['DB_NAME']
        self.db_host = os.environ['DB_HOST']
        self.db_user = os.environ['DB_USER']
        self.db_password = os.environ['DB_PASSWORD']
        self.aws_accesskey_id=os.environ['AWS_ACCESSKEY_ID']
        self.aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY']
        self.aws_bucket_name=os.environ['AWS_BUCKET_NAME']

settings=Settings()