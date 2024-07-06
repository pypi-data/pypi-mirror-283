# download_pbi_xmla/main.py
import pyarrow.parquet as pq
import pyarrow.compute as pc
import msal
import os
import logging
import json
from datetime import datetime
from download_pbi_xmla.ssas_api import set_conn_string, get_DAX

logging.basicConfig(level=logging.DEBUG)

def fetch_and_save_table(table_name, conn_str, file_name, date_column=None, last_date=None):
    query = f'EVALUATE {table_name}'
    if date_column and last_date:
        query += f' WHERE {date_column} > DATE({last_date.year}, {last_date.month}, {last_date.day})'
    
    try:
        logging.info(f"Running DAX query for table {table_name}")
        table = get_DAX(conn_str, query)
        logging.info(f"Table '{table_name}' fetched successfully!")
        pq.write_table(table, file_name)
        logging.info(f"Table '{table_name}' saved to {file_name}")
        
        if date_column:
            # Get the latest date from the fetched data
            date_column_data = table.column(date_column)
            date_column_data = pc.cast(date_column_data, pa.timestamp('s'))
            latest_date = date_column_data.max().as_py()
            return latest_date
    except Exception as e:
        logging.error(f"Failed to fetch or save table '{table_name}'.")
        logging.error(str(e))
    return None

def get_access_token(client_id, client_secret, tenant_id):
    authority_url = f"https://login.microsoftonline.com/{tenant_id}"
    app = msal.ConfidentialClientApplication(
        client_id,
        authority=authority_url,
        client_credential=client_secret
    )
    scopes = ["https://analysis.windows.net/powerbi/api/.default"]
    result = app.acquire_token_for_client(scopes)
    if "access_token" in result:
        logging.info("Token acquired successfully")
        return result["access_token"]
    else:
        logging.error("Failed to acquire token")
        raise ValueError("Failed to acquire token")

def fetch_tables(config_file, path, client_id, client_secret, tenant_id):
    with open(config_file, 'r') as file:
        config = json.load(file)

    token = get_access_token(client_id, client_secret, tenant_id)
    conn_str = f"Provider=MSOLAP;Data Source={config['server']};Initial Catalog={config['database']};Persist Security Info=True;Impersonation Level=Impersonate;Password={token}"

    logging.debug(f"Connection string: {conn_str}")

    updated_tables = []
    for table_info in config['tables']:
        table_name = table_info['name']
        refresh_type = table_info['refresh_type']
        date_column = table_info.get('date_column')
        last_date = table_info.get('last_date')  # Expected to be in "YYYY-MM-DD" format

        if last_date:
            last_date = datetime.strptime(last_date, "%Y-%m-%d")

        file_path = os.path.join(path, f"{table_name}.parquet")
        
        if refresh_type == "incremental" and date_column:
            latest_date = fetch_and_save_table(table_name, conn_str, file_path, date_column, last_date)
            if latest_date:
                table_info['last_date'] = latest_date.strftime("%Y-%m-%d")
        else:
            fetch_and_save_table(table_name, conn_str, file_path)

        updated_tables.append(table_info)
    
    # Update the configuration file with the latest dates
    config['tables'] = updated_tables
    with open(config_file, 'w') as file:
        json.dump(config, file, indent=4)

def main():
    import argparse
    from dotenv import load_dotenv

    # Load environment variables from .env file
    load_dotenv()

    # Fetch secrets and other settings from environment variables
    CLIENT_ID = os.getenv('CLIENT_ID').strip()
    CLIENT_SECRET = os.getenv('CLIENT_SECRET').strip()
    TENANT_ID = os.getenv('TENANT_ID').strip()
    CONFIG_FILE = os.getenv('CONFIG_FILE').strip()
    SAVE_PATH = os.getenv('SAVE_PATH')

    if SAVE_PATH:
        SAVE_PATH = SAVE_PATH.strip()
    else:
        SAVE_PATH = ''  # Provide a default value or handle the absence appropriately

    # Debug print statements to verify environment variables
    logging.debug(f"CLIENT_ID: {CLIENT_ID}")
    logging.debug(f"CLIENT_SECRET: {'*' * len(CLIENT_SECRET) if CLIENT_SECRET else None}")
    logging.debug(f"TENANT_ID: {TENANT_ID}")
    logging.debug(f"Config File: {CONFIG_FILE}")
    logging.debug(f"Save Path: {SAVE_PATH}")

    fetch_tables(
        config_file=CONFIG_FILE,
        path=SAVE_PATH,
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        tenant_id=TENANT_ID
    )

if __name__ == "__main__":
    main()

