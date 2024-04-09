import sqlite3
import pandas as pd
import os

# Establish a connection to the SQLite database
connection = sqlite3.connect('electric_report.db')

# Define your SQL query to select data from the E_report table
query = "SELECT * FROM Electric_report"

# Read the query result into a pandas DataFrame
df = pd.read_sql_query(query, connection)

# Define the output CSV file path
csv_file = 'electric_report.csv'

# Write the DataFrame to a CSV file
df.to_csv(csv_file, index=False)

# Close the connection
connection.close()

# Open the CSV file in Excel if Excel is installed
try:
    os.system('start excel.exe electric_report.csv')
except Exception as e:
    print(f"Error opening Excel: {e}")
