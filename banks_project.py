import pandas as pd
from bs4 import BeautifulSoup
import numpy as np
import sqlite3
from datetime import datetime 
import requests

data_url = "https://web.archive.org/web/20230908091635 /https://en.wikipedia.org/wiki/List_of_largest_banks"
table_ext_attr = ["Name", "MC_USD_Billion"]
table_fin_attr = ["Name", "MC_USD_Billion", "MC_GBP_Billion", "MC_EUR_Billion", "MC_INR_Billion"]
csv_path = "./Largest_banks_data.csv"
db_name = 'Banks.db'
table_name = 'Largest_banks'

def log_progress(message):
    ''' This function logs the mentioned message of a given stage of the
    code execution to a log file. Function returns nothing'''
    timestamp_format = '%Y-%h-%d-%H-:%M:%S'
    now = datetime.now()
    timestamp = now.strftime(timestamp_format)
    with open("./code_log.txt", "a") as f:
        f.write(timestamp + ': ' + message + "\n")

def extract(url, table_attribs):
    ''' This function aims to extract the required
    information from the website and save it to a data frame. The
    function returns the data frame for further processing. '''
    page = requests.get(url).text
    data = BeautifulSoup(page, 'html.parser')
    df = pd.DataFrame(columns=table_attribs)
    tables = data.find_all('tbody')
    rows = tables[0].find_all('tr')
    for row in rows:
        col = row.find_all('td')
        if len(col) != 0:
            a_tag = col[1].find('a')
            if a_tag:
                data_dict = {"Name": col[1].get_text().strip(), "MC_USD_Billion": col[2].get_text()}
                df1 = pd.DataFrame(data_dict, index=[0])
                df = pd.concat([df, df1], ignore_index=True)
                df["MC_USD_Billion"] = df["MC_USD_Billion"].str.strip()
    df["MC_USD_Billion"] = df["MC_USD_Billion"].astype(float)

    return df


def transform(df, csv_path):
    ''' This function accesses the CSV file for exchange rate
    information, and adds three columns to the data frame, each
    containing the transformed version of Market Cap column to
    respective currencies'''
    df_ex_rate = pd.read_csv(csv_path)
    dict = df_ex_rate.set_index(df_ex_rate.columns[0]).to_dict()[df_ex_rate.columns[1]]

    df["MC_GBP_Billion"] = [np.round(x*dict['GBP'],2) for x in df['MC_USD_Billion']]
    df["MC_EUR_Billion"] = [np.round(x*dict['EUR'],2) for x in df['MC_USD_Billion']]
    df["MC_INR_Billion"] = [np.round(x*dict['INR'],2) for x in df['MC_USD_Billion']]

    return df


def load_to_csv(df, output_path):
    ''' This function saves the final data frame as a CSV file in
    the provided path. Function returns nothing.'''
    df.to_csv(output_path)

def load_to_db(df, sql_connection, table_name):
    ''' This function saves the final data frame to a database
    table with the provided name. Function returns nothing.'''
    df.to_sql(table_name, sql_connection, if_exists='replace', index=False)

def run_query(query_statement, sql_connection):
    ''' This function runs the query on the database table and
    prints the output on the terminal. Function returns nothing. '''
    print(pd.read_sql(query_statement, sql_connection))


''' Here, you define the required entities and call the relevant
functions in the correct order to complete the project. Note that this
portion is not inside any function.'''

log_progress("Preliminaries complete. Initiating ETL process")

log_progress("Extract Phase Started")

extracted_data = extract(data_url, table_ext_attr)

log_progress("Data extraction complete. Initiating Transformation process")

log_progress("Transformation Phase Started")

transformed_data = transform(extracted_data, 'exchange_rate.csv')

log_progress("Data transformation complete. Initiating Loading process")

log_progress("Load Phase Started")

load_to_csv(transformed_data, csv_path)

log_progress("Data saved to CSV file")

sql_connection = sqlite3.connect(db_name)
log_progress("SQL Connection initiated")

load_to_db(transformed_data, sql_connection, table_name)
log_progress("Data loaded to Database as a table, Executing queries")

# First Query
run_query(f"SELECT * FROM {table_name}", sql_connection)

# Second Query
run_query(f"SELECT AVG(MC_GBP_Billion) FROM {table_name}", sql_connection)

# Third Query
run_query(f"SELECT Name from {table_name} LIMIT 5", sql_connection)

log_progress("Process Complete")

sql_connection.close()
log_progress("Server Connection closed")
