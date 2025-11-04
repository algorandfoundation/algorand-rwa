import clickhouse_connect
import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()
"""
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
"""
# Steamlit deployment
DB_HOST = st.secrets.db_credentials["DB_HOST"]
DB_PORT = st.secrets.db_credentials["DB_PORT"]
DB_USER = st.secrets.db_credentials["DB_USER"]
DB_PASS = st.secrets.db_credentials["DB_PASS"]



def get_client():
    client = clickhouse_connect.get_client(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASS,
            secure=False
        )
    return client

def run_query(query: str):
    client = get_client()
    result = client.query(query)
    return result.result_rows, result.column_names
