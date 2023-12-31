import os
import csv
import pandas as pd
import requests
import tabula
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor
import boto3


class DataExtractor:
    BASE_API_URL = "https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod"
    S3_BUCKET_NAME = "data-handling-public"
    S3_REGION = "eu-west-2"
    DATE_DETAILS_KEY = "date_details.json"
    PRODUCTS_KEY = "products.csv"

    def __init__(self) -> None:
        """Initializes the DataExtractor by loading environment variables."""
        load_dotenv()
        self.api_key = os.getenv("X_API_KEY")
        self.aws_access = os.getenv("AWS_ACCESS")
        self.aws_secret = os.getenv("AWS_SECRET")

    def _get_headers(self) -> dict:
        """Returns common request headers."""
        return {"x-api-key": self.api_key}

    def read_rds_table(self, connector, table: str) -> pd.DataFrame:
        """Reads a specified table from RDS and returns it as a DataFrame."""
        return pd.read_sql_table(table, connector.init_db_engine())

    def retrieve_pdf_data(self, url: str) -> pd.DataFrame:
        """Retrieves data from a specified PDF URL and returns it as a DataFrame."""
        return tabula.read_pdf(url, pages="all", multiple_tables=False)[0]

    def list_number_of_stores(self) -> int:
        """Returns the total number of stores from the API."""
        response = requests.get(
            f"{self.BASE_API_URL}/number_stores", headers=self._get_headers()
        )
        return response.json()["number_stores"]

    def retrieve_store_data(self, store_id: int) -> dict:
        """Retrieves detailed information for a specified store ID."""
        url = f"{self.BASE_API_URL}/store_details/{store_id}"
        return requests.get(url, headers=self._get_headers()).json()

    def retrieve_stores_data(self) -> pd.DataFrame:
        """Retrieves and aggregates data for all stores concurrently, returning it as a DataFrame."""
        with ThreadPoolExecutor() as executor:
            store_ids = range(self.list_number_of_stores())
            response = list(executor.map(self.retrieve_store_data, store_ids))
        return pd.DataFrame(response)

    def extract_from_s3(self) -> pd.DataFrame:
        """Extracts product data from a specified S3 bucket and returns it as a DataFrame."""
        s3 = boto3.client(
            's3',
            aws_access_key_id=self.aws_access,
            aws_secret_access_key=self.aws_secret,
            region_name=self.S3_REGION
        )
        obj = s3.get_object(Bucket=self.S3_BUCKET_NAME, Key=self.PRODUCTS_KEY)
        data = obj['Body'].read().decode('utf-8').splitlines()
        return pd.DataFrame(list(csv.reader(data)))

    def retrieve_date_details(self) -> pd.DataFrame:
        """Retrieves date details from an S3 URL and returns them as a DataFrame."""
        url = f"https://{self.S3_BUCKET_NAME}.s3.eu-west-1.amazonaws.com/{self.DATE_DETAILS_KEY}"
        return pd.DataFrame(requests.get(url, headers=self._get_headers()).json())
