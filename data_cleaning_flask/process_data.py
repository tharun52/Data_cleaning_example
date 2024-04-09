import pandas as pd
import pymysql
import sqlite3

def clean_table(in_host, in_username, in_password, in_database_name, selected_table, table_name):
    # Connect to the MySQL database
    conn_source = pymysql.connect(
        host=in_host,
        user=in_username,
        password=in_password,
        database=in_database_name
    )

    # Import the table into a Pandas DataFrame
    query = f"SELECT * FROM {selected_table};"
    df = pd.read_sql(query, conn_source)

    # Closing the connection to the source database
    conn_source.close()

    # Renaming the columns
    new_column_names = {
        'Timestamp': 'Timestamp',
        'HVACCALCPNT': 'HVAC',
        'terrace_IC_PWRPNLTDAY': 'KITCHEN',
        'GF_MEPGF_416kwTDAY': 'LINAC',
        'RAW_CALCChstrypnt': 'RAW POWER',
        'LIGHTNG_CALCChstrypnt': 'LIGHTNG',
        'TerraceliftpanelTDAY': 'LIFT',
        'UPS_CALCChstrypnt': 'UPS',
        '1stfloorpowerpanelTDAY': 'PET/SPECT',
        'GF_EBINCOMERXPERT_PRO_SDC': 'EB_CONSUMPTION',
        'dgstdrycnsmptn': 'DG_CONSUMPTION'
    }

    df.rename(columns=new_column_names, inplace=True)

    # Converting Timestamp to date-time format and ignoring time
    df['Timestamp'] = pd.to_datetime(df['Timestamp'], dayfirst=True)
    df['Timestamp'] = df['Timestamp'].dt.date

    # Grouping other columns by date
    grouped_df = df.groupby(df['Timestamp']).first().reset_index()

    # If there are still multiple dates after grouping, we are grouping again by adding it up
    grouped_df = df.groupby(df['Timestamp']).sum().reset_index()

    # Adding Total and Total.1 columns
    total1 = grouped_df.iloc[:, 1:9].sum(axis=1)
    total2 = grouped_df[['EB_CONSUMPTION', 'DG_CONSUMPTION']].sum(axis=1)

    grouped_df.insert(9, 'TOTAL1', total1)  # inserting in specified location
    grouped_df['TOTAL2'] = total2  # creating a new column

    # Connect to the SQLite database
    conn_destination = sqlite3.connect(f"{table_name}.db")
    grouped_df.to_sql(table_name, conn_destination, index=False, if_exists='replace')

# for displaying tables in the "/tables" route
def get_tables(host, username, password, database_name):
    # Connect to the MySQL database
    conn = pymysql.connect(
        host=host,
        user=username,
        password=password,
        database=database_name
    )

    # Get the list of tables in the database
    cursor = conn.cursor()
    cursor.execute("SHOW TABLES")
    tables = [table[0] for table in cursor.fetchall()]

    # Close the connection
    cursor.close()
    conn.close()

    return tables
