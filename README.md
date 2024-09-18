# Top 10 Largest Banks by Market Capitalization

This project automates the extraction, transformation, and storage of the top 10 largest banks in the world, ranked by market capitalization (MC) in billion USD. The system also converts the MC values into GBP, EUR, and INR based on provided exchange rates, and stores the final data in both CSV and SQLite database formats. The system is designed to be re-executed every financial quarter to update the report.

## Project Overview
The script automates the following tasks:
1. **Data Extraction**: Scrapes the list of banks and their market capitalization from a Wikipedia page.
2. **Data Transformation**: Converts market capitalization values to GBP, EUR, and INR using provided exchange rates.
3. **Data Loading**: Saves the transformed data to a CSV file and an SQLite database.
4. **Quarterly Report Generation**: Automates the entire process for repeated use every quarter.
5. **Logging**: Tracks the execution of each task in a log file for transparency and troubleshooting.

## Project Steps

### 1. Log Progress (`log_progress()`)
- Logs the progress of the code execution into a file called `code_log.txt`.
- Tracks key events, such as starting the extraction, transformation, and loading phases, as well as any errors encountered.

### 2. Extract Bank Data from Wikipedia (`extract()`)
- Scrapes the data under the "By market capitalization" heading from the Wikipedia page.
- Extracts the **Bank Name** and **Market Capitalization (USD)** into a Pandas DataFrame.
- URL: [Wikipedia page](https://web.archive.org/web/20230908091635/https://en.wikipedia.org/wiki/List_of_largest_banks).

### 3. Transform Data with Exchange Rates (`transform()`)
- Reads exchange rate information from a CSV file
- Converts the market capitalization from USD to **GBP**, **EUR**, and **INR** using the given exchange rates.
- Ensures that the converted values are rounded to two decimal places.
- Adds new columns for **MC_GBP_Billion**, **MC_EUR_Billion**, and **MC_INR_Billion** in the DataFrame.

### 4. Save Transformed Data to CSV (`load_to_csv()`)
- Saves the transformed data into a CSV file named `Largest_banks_data.csv`.
- This CSV file contains the bank names and market capitalization in four currencies (USD, GBP, EUR, INR).

### 5. Load Transformed Data to SQLite Database (`load_to_db()`)
- Loads the transformed data into an SQLite database (`Banks.db`).
- Creates a table called `Largest_banks` with columns for market capitalization in USD, GBP, EUR, and INR.
- This database allows for future queries and analysis.

### 6. Run SQL Queries on Database
- Executes SQL queries to verify the data stored in the `Largest_banks` table within the SQLite database.
- You can run custom queries to explore the data and generate reports as needed.

### 7. Log File Verification
- Ensures that all tasks are correctly logged in the `code_log.txt` file, providing a clear history of the script's execution.
- This log file serves as an audit trail and can be used to troubleshoot any issues.

## File Descriptions

- **banks_project.py**: The main Python script containing all functions to automate the entire process.
- **Largest_banks_data.csv**: The output CSV file with bank names and market capitalizations in USD, GBP, EUR, and INR.
- **Banks.db**: SQLite database containing the final transformed data in the `Largest_banks` table.
- **code_log.txt**: Log file that tracks the progress and status of each task in the script.

## How to Run the Project

1. Clone this repository to your local machine.
2. Ensure that you have the required Python libraries installed:
   ```bash
   pip install pandas beautifulsoup4 requests sqlite3
