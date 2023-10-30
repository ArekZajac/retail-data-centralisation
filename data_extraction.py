import database_utils as utils
import pandas as pd
import tabula
import requests
import os
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor
import boto3
import csv

class DataExtractor:
    def __init__(self) -> None:
        load_dotenv()

    def read_rds_table(self, connector, table):
        return pd.read_sql_table(table, connector.init_db_engine())
    
    def retrieve_pdf_data(self, url):
        return tabula.read_pdf(url, pages="all", multiple_tables=False)[0]
    
    def list_number_of_stores(self):
        return requests.get(
            "https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/number_stores",
            headers={"x-api-key":os.getenv("X_API_KEY")}).json()["number_stores"]
    
    def retrieve_store_data(self, store_id):
        url = f"https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/store_details/{store_id}"
        headers = {"x-api-key": os.getenv("X_API_KEY")}
        return requests.get(url, headers=headers).json()

    def retrieve_stores_data(self):
        with ThreadPoolExecutor() as executor:
            store_ids = range(self.list_number_of_stores())
            response = list(executor.map(self.retrieve_store_data, store_ids))
        return pd.DataFrame(response) # ~40 sec
    
    def extract_from_s3(self):
        s3 = boto3.client(
            's3',
            aws_access_key_id=os.getenv("AWS_ACCESS"),
            aws_secret_access_key=os.getenv("AWS_SECRET"),
            region_name='eu-west-2'
        )
        obj = s3.get_object(Bucket='data-handling-public', Key='products.csv')
        data = obj['Body'].read().decode('utf-8').splitlines()
        return pd.DataFrame(csv.reader(data))
    
    def retrieve_date_details(self):
        url = "https://data-handling-public.s3.eu-west-1.amazonaws.com/date_details.json"
        headers = {"x-api-key": os.getenv("X_API_KEY")}
        return pd.DataFrame(requests.get(url, headers=headers).json())