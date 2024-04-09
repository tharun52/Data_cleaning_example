import sqlite3
import pandas as pd
import os

# Asking user to enter db name
db_name = input("Enter database name : ")

# Establish a connection to the SQLite database
connection = sqlite3.connect(f'{db_name}.db')

# Get a list of all tables in the database
cursor = connection.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

# Loop through each table and read its data into a pandas DataFrame
for table in tables:
    table_name = table[0]
    query = f"SELECT * FROM {table_name}"
    df = pd.read_sql_query(query, connection)
    
    # Define the output CSV file path for each table
    csv_file = f'{table_name}.csv'
    
    # Write the DataFrame to a CSV file for each table
    df.to_csv(csv_file, index=False)

# Close the cursor and connection
cursor.close()
connection.close()

# Open the CSV files in Excel if Excel is installed
try:
    for table in tables:
        table_name = table[0]
        csv_file = f'{table_name}.csv'
        os.system(f'start excel.exe {csv_file}')
except Exception as e:
    print(f"Error opening Excel: {e}")
