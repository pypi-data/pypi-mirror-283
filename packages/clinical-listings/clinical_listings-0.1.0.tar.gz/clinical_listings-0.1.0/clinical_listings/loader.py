# clinical_listings/loader.py
import pandas as pd
from sqlalchemy import create_engine

def load_csv(file_path):
    return pd.read_csv(file_path)

def load_excel(file_path):
    return pd.read_excel(file_path)

def load_sql(connection_string, query):
    engine = create_engine(connection_string)
    return pd.read_sql(query, engine)

def load_sas(file_path):
    return pd.read_sas(file_path)

