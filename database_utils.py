import json
import sqlalchemy as alch

class DatabaseConnector:

    def read_db_creds(self):
        return json.load(open("db_creds.json"))
    
    def init_db_engine(self):
        c = self.read_db_creds()
        return alch.create_engine(
            f"postgresql+psycopg://{c['RDS_USER']}:{c['RDS_PASSWORD']}@{c['RDS_HOST']}:{c['RDS_PORT']}/{c['RDS_DATABASE']}")
    
    def list_db_tables(self):
        print(alch.inspect(self.init_db_engine()).get_table_names())

    def upload_to_db(self, df, name):
        c = self.read_db_creds()
        engine = alch.create_engine(
            f"postgresql+psycopg://{c['LOC_USER']}:{c['LOC_PASSWORD']}@{c['LOC_HOST']}:{c['LOC_PORT']}/{c['LOC_DATABASE']}")
        df.to_sql(name, engine)