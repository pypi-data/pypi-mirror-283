import sqlalchemy as db
import pandas as pd
from sqlalchemy.orm import sessionmaker

class Context:
    """Context class for connecting to SQL databases"""

    def __init__(self, server, username, password, database):

        self.server = server
        self.username = username
        self.password = password
        self.database = database

        engine = db.create_engine(f'mssql+pyodbc://{self.username}:{self.password}@{self.server}/{self.database}?driver=ODBC+Driver+17+for+SQL+Server')

        Session = sessionmaker(bind=engine)

        self.session = Session()

    def query(self, model):
        """Query a table"""
        return self.session.query(model)

    def query_join(self, model1, model2):
        """Query a table"""
        return self.session.query(model1, model2)

    def insert(self, record):
        self.session.add(record)

    def add_all(self, records):
        self.session.add_all(records)

    def merge(self, record):
        self.session.merge(record)

    def delete(self, record):
        self.session.delete(record)
        self.commit()

    def execute(self, statement, args=None):
        """Execute a raw SQL statement and return records"""
        if not args:
            return self.session.execute(statement)
        else:
            return self.session.execute(statement, args)


    def read_sql_query(self, statement):
        return pd.read_sql_query(statement, self.session.bind.engine)

    def save_changes(self):
        self.session.commit()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()

    def close(self):
        self.session.close()

