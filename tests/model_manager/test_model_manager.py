import unittest
import os

from src.model_manager.model_manager import *

class TestModelManager(unittest.TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        credPath = os.environ['GOOGLE_APPLICATION_CREDENTIALS']
        super().__init__(methodName)
        self.file_path = '/home/erick/covid_predictor_peru/models/model.h5'
        self.modelManager = ModelManager(credPath)
        self.modelManager.setup()


    def test_upload_download(self):
        with open(self.file_path,'rb') as file:
            file_bytes = file.read()
        uploaded_id = self.modelManager.upload_file_bytes(file_bytes,'test.h5')
        file_bytes_downloaded = self.modelManager.download_file_bytes(uploaded_id)
        self.assertEquals(file_bytes,file_bytes_downloaded)


if __name__ == '__main__':
    unittest.main()
