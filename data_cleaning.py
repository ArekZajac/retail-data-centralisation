import data_extraction as extract
import database_utils as utils
import pandas as pd
import regex as re

class DataCleaning:
    def clean_user_data(self, df):
            # drop rows with all NULL values
        df = df.dropna(how='all')
            # drop redundant index column
        df.drop(columns=['index'], inplace=True)
            # filter out non date values then convert date columns to datetime format 
        df['date_of_birth'] = pd.to_datetime(df['date_of_birth'], errors='coerce')
        df['join_date'] = pd.to_datetime(df['join_date'], errors='coerce')
            # phone numbers
        df["phone_number"] = df["phone_number"].str.replace(r'[^0-9+\-()\s]', '', regex=True) # unwanted characters
        df["phone_number"] = df["phone_number"].str.strip().str.replace(r'\s+', ' ', regex=True) # extra spaces
            # replace newline characters in the address
        df['address'] = df['address'].str.replace('\n', ', ')
            # remove rows based on unexpected values after conversion
        df = df.dropna(subset=['date_of_birth', 'join_date'])
        return df
    
    def clean_card_data(self, df):
            # drop column names as rows
        misrepresented_rows = df[df.apply(lambda row: all(row == df.columns), axis=1)]
        df = df.drop(misrepresented_rows.index)
            # remove non-numeric from card numbers
        df['card_number'] = df['card_number'].str.replace(r'\D', '', regex=True)
            # date payment confirmed
        df['date_payment_confirmed'] = pd.to_datetime(df['date_payment_confirmed'], errors='coerce') 
            # remove rows based on unexpected values after conversion
        df = df.dropna(subset=['date_payment_confirmed'])
            # remove rows with expiry_date not matching format
        valid_expiry_rows = df['expiry_date'].str.match(r"^(0[1-9]|1[0-2])\/\d{2}$")
        df = df[valid_expiry_rows]
        return df
    
    def clean_store_data(self, df):
            # drop columns
        df = df.drop(columns=['message', 'lat', 'index'], errors='ignore')
            # clean addresses
        df['address'] = df['address'].str.replace('\n', ' ', regex=False)
            # ee
        df['continent'] = df['continent'].str.replace('^ee', '', regex=True)
            # opening date to datetime
        df['opening_date'] = pd.to_datetime(df['opening_date'], errors='coerce')
            # long to float
        df['longitude'] = pd.to_numeric(df['longitude'], errors='coerce')
            # lat to float
        df['latitude'] = pd.to_numeric(df['latitude'], errors='coerce')
            # staff no. to int
        df['staff_numbers'] = pd.to_numeric(df['staff_numbers'], errors='coerce', downcast='integer')
            # drop nulls
        df = df.dropna(how='any')
        return df
    
    def convert_product_weights(self, w):
        try:
            w = w.strip()
            if 'kg' in w:
                return float(w.replace('kg', ''))
            elif 'g' in w:
                return float(w.replace('g', '')) / 1000
            elif 'ml' in w:
                return float(w.replace('ml', '')) / 1000
            else:
                return float('nan')
        except:
            return float('nan')

    def clean_products_data(self, df):
        df = df.drop(columns=[0], errors='ignore')
            # set 1st row as header
        df.columns = df.iloc[0]
        df = df.drop(0)
        df = df.reset_index(drop=True)
            # convert to datetime
        df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')
            # convert weights to kg
        df['weight'] = df['weight'].apply(self.convert_product_weights)
            # drop nulls
        df = df.dropna(how='any')
        return df
    
    def clean_orders_data(self, df):
        df = df.drop(columns=['level_0', 'index', 'first_name', 'last_name', '1'], errors='ignore')
        return df
    
    def clean_date_data(self, df):
        df['month'] = pd.to_numeric(df['month'], errors='coerce', downcast='integer')
        df['year'] = pd.to_numeric(df['year'], errors='coerce', downcast='integer')
        df['day'] = pd.to_numeric(df['day'], errors='coerce', downcast='integer')
        df = df.dropna(how='any')
        return df