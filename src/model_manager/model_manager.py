import boto3
from ..settings import settings
import tempfile
import io
from src.models.models import ModelInfo,ActualModel
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload,MediaIoBaseDownload
from google.oauth2 import service_account
from datetime import datetime


def get_service() :
    key_file_location='credentials/creds.json'
    scopes = 'https://www.googleapis.com/auth/drive'
    credentials = service_account.Credentials.from_service_account_file(
    key_file_location)
    scoped_credentials = credentials.with_scopes(scopes)
    service = build(api_name='drive', api_version='v3', credentials=scoped_credentials)
    return service

def upload_file(filepath):
    service = get_service()
    file_name=f'model{datetime.now().strftime("%d%m%y%h%m%s")}.h5'
    file_metadata= {"name": file_name, "parents":["1iI2je_bE9NPmWe4vOEpZpEMghwnVr3og"]}
    media = MediaFileUpload(mimetype='file/h5',filename=filepath)
    drive_file = (service.files().create(body =file_metadata ,media_body=media, fields="id").execute())
    file_id=drive_file.get("id")
    model_info = ModelInfo(model_id=file_id,model_name=file_name)
    model_info.save()
    actual_model=ActualModel(model_id=file_id)
    actual_model.save()
    return file_id


def download_file_bytes(file_id):
    service = get_service()
    request = service.files().get_media(fileId=file_id)
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

def handle_new_model(file):
    file_id = upload_file(file)
    print(file_id)

def get_model():
    return ''