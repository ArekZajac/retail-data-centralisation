import database_utils as utils
import data_extraction as extract
import data_cleaning as clean
import pandas as pd


connector = utils.DatabaseConnector()
extractor = extract.DataExtractor()
cleaner = clean.DataCleaning()

# CSV files saved here for pre/post cleaning inspection.
file_path_prefix = "/Users/arek/Downloads/"

pd.set_option('display.max_columns', 2000)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', 2000)

data_processes = {
    "users": {
        "read": lambda: extractor.read_rds_table(connector, "legacy_users"),
        "clean": cleaner.clean_user_data,
        "db_table": "dim_users"
    },
    "cards": {
        "read": lambda: extractor.retrieve_pdf_data("https://data-handling-public.s3.eu-west-1.amazonaws.com/card_details.pdf"),
        "clean": cleaner.clean_card_data,
        "db_table": "dim_card_details"
    },
    "stores": {
        "read": extractor.retrieve_stores_data,
        "clean": cleaner.clean_store_data,
        "db_table": "dim_store_details"
    },
    "products": {
        "read": extractor.extract_from_s3,
        "clean": cleaner.clean_products_data,
        "db_table": "dim_products"
    },
    "orders": {
        "read": lambda: extractor.read_rds_table(connector, "orders_table"),
        "clean": cleaner.clean_orders_data,
        "db_table": "orders_table"
    },
    "dates": {
        "read": extractor.retrieve_date_details,
        "clean": cleaner.clean_date_data,
        "db_table": "dim_date_times"
    }
}

def process_data(name, process):
    raw_data = process["read"]()
    raw_data.to_csv(f"{file_path_prefix}{name}_dirty.csv")
    clean_data = process["clean"](raw_data)
    clean_data.to_csv(f"{file_path_prefix}{name}_clean.csv")
    connector.upload_to_db(clean_data, process["db_table"])

for name, process in data_processes.items():
    process_data(name, process)
