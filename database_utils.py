import json
import sqlalchemy as alch


class DatabaseConnector:
    def __init__(self, creds_file: str = "db_creds.json") -> None:
        """Initializes the DatabaseConnector with database credentials."""
        self.creds = self.read_db_creds(creds_file)
    
    def read_db_creds(self, creds_file: str) -> dict:
        """Reads database credentials from a JSON file."""
        with open(creds_file, 'r') as f:
            return json.load(f)
    
    def init_db_engine(self, creds_key_prefix: str = 'RDS') -> alch.engine.base.Engine:
        """Initializes and returns a SQLAlchemy engine using the specified credentials."""
        return alch.create_engine(
            f"postgresql+psycopg://{self.creds[f'{creds_key_prefix}_USER']}:{self.creds[f'{creds_key_prefix}_PASSWORD']}@"
            f"{self.creds[f'{creds_key_prefix}_HOST']}:{self.creds[f'{creds_key_prefix}_PORT']}/"
            f"{self.creds[f'{creds_key_prefix}_DATABASE']}")
    
    def list_db_tables(self) -> list:
        """Lists all tables in the database."""
        return alch.inspect(self.init_db_engine()).get_table_names()

    def upload_to_db(self, df, name: str, creds_key_prefix: str = 'LOC') -> None:
        """Uploads a DataFrame to the database with the specified name."""
        engine = self.init_db_engine(creds_key_prefix)
        df.to_sql(name, engine, if_exists='replace')
