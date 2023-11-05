import json
import sqlalchemy as alch

class DatabaseConnector:
    
    def __init__(self, creds_file="db_creds.json"):
        self.creds = self.read_db_creds(creds_file)
    
    def read_db_creds(self, creds_file):
        with open(creds_file, 'r') as f:
            return json.load(f)
    
    def init_db_engine(self, creds_key_prefix='RDS'):
        return alch.create_engine(
            f"postgresql+psycopg://{self.creds[f'{creds_key_prefix}_USER']}:{self.creds[f'{creds_key_prefix}_PASSWORD']}@"
            f"{self.creds[f'{creds_key_prefix}_HOST']}:{self.creds[f'{creds_key_prefix}_PORT']}/"
            f"{self.creds[f'{creds_key_prefix}_DATABASE']}")
    
    def list_db_tables(self):
        return alch.inspect(self.init_db_engine()).get_table_names()

    def upload_to_db(self, df, name, creds_key_prefix='LOC'):
        engine = self.init_db_engine(creds_key_prefix)
        df.to_sql(name, engine, if_exists='replace')
