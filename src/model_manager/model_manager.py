import boto3
import tempfile
import io
from src.models.models import ModelInfo,ActualModel
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload,MediaIoBaseDownload,MediaIoBaseUpload
from google.oauth2 import service_account
from datetime import datetime

class ModelManager():
    def __init__(self,credentials_path:str):
        self.service = None
        self.credentials = credentials_path
    
    def setup(self) :
        scopes = ['https://www.googleapis.com/auth/drive']
        credentials = service_account.Credentials.from_service_account_file(
        self.credentials)
        scoped_credentials = credentials.with_scopes(scopes)
        self.service = build("drive", "v3", credentials=scoped_credentials)
        print(f'Drive Service builded')

        print()
        return
    
    def upload_file_bytes(self,upload_bytes: bytes,file_name) -> str:
        media = MediaIoBaseUpload(io.BytesIO(upload_bytes), mimetype='application/octet-stream', resumable=True)
        file_metadata = {
            'name': file_name,
            #id carpeta models
            'parents': ["1iI2je_bE9NPmWe4vOEpZpEMghwnVr3og"]
        }
        file = self.service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        print(f'File uploaded. File ID: {file["id"]}')
        return file["id"]
    
    def download_file_bytes(self,file_id:str) -> bytes:
        request = self.service.files().get_media(fileId=file_id)
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh,request,204800)
        done = False
        try:
            while not done:
                status, done = downloader.next_chunk()
            fh.seek(0)
            return fh.getvalue()
        except:
            print("Error downloading")
            return None
        
    def handle_new_model(self,file:str):
        file_id = self.upload_file(file)
        print(file_id)

    def get_model():
        return ''









