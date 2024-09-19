import requests
import base64
import zipfile
import io
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()

class KaggleDatasetDownloader:
    def __init__(self):
        self.base_url = "https://www.kaggle.com/api/v1"
        self.username = os.environ["KAGGLE_USERNAME"]
        self.key = os.environ["KAGGLE_API_KEY"]
        self.headers = self._prepare_headers()

    def _prepare_headers(self):
        creds = base64.b64encode(bytes(f"{self.username}:{self.key}", "ISO-8859-1")).decode("ascii")
        return {"Authorization": f"Basic {creds}"}

    def download_dataset(self, owner_slug, dataset_slug, dataset_version, file_name):
        url = self._construct_url(owner_slug, dataset_slug, dataset_version)
        response = self._send_request(url)
        df = self._process_response(response, file_name)
        return df

    def _construct_url(self, owner_slug, dataset_slug, dataset_version):
        return f"{self.base_url}/datasets/download/{owner_slug}/{dataset_slug}?datasetVersionNumber={dataset_version}"

    def _send_request(self, url):
        return requests.get(url, headers=self.headers)

    def _process_response(self, response, file_name):
        zf = zipfile.ZipFile(io.BytesIO(response.content))
        return pd.read_csv(zf.open(file_name),sep='\t')

# # Usage example:
# if __name__ == "__main__":
#     downloader = KaggleDatasetDownloader()
#     df = downloader.download_dataset("shivamb", "netflix-shows", "5", "netflix_titles.csv")
#     print(df.head())