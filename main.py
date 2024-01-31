import pandas as pd
import sqlite3

try:
    # Getting input from the user
    input_file_name = input("Enter file name (with path) : ")

    #loading the csv file
    df = pd.read_csv(input_file_name)

    output_file_name = "Electric_Report.csv"

    #renaming the columns
    new_column_names = {
        'Timestamp':'Timestamp',
        'HVACCALCPNT':'HVAC',
        'terrace_IC_PWRPNLTDAY':'KITCHEN',
        'GF_MEPGF_416kwTDAY':'LINAC',
        'RAW_CALCChstrypnt':'RAW POWER',
        'LIGHTNG_CALCChstrypnt':'LIGHTNG',
        'TerraceliftpanelTDAY':'LIFT',
        'UPS_CALCChstrypnt':'UPS',
        '1stfloorpowerpanelTDAY':'PET/SPECT',
        'GF_EBINCOMERXPERT_PRO_SDC':'EB_CONSUMPTION',
        'dgstdrycnsmptn':'DG_CONSUMPTION'
    }

    df.rename(columns=new_column_names, inplace=True)

    #Converting Timestamp to date-time format and ignoring time
    df['Timestamp'] = pd.to_datetime(df['Timestamp'], dayfirst=True)
    df['Timestamp'] = df['Timestamp'].dt.date

    #grouping other columns by date
    grouped_df = df.groupby(df['Timestamp']).first().reset_index()
    # the first() functions returns the first non null value of a column

    # If there are stil multiple dates after grouping, we are grouping again by adding it up
    grouped_df = df.groupby(df['Timestamp']).sum().reset_index()

    #Adding Total and Total.1 columns
    total1 = grouped_df.iloc[:, 1:9].sum(axis=1)
    total2 = grouped_df[['EB_CONSUMPTION', 'DG_CONSUMPTION']].sum(axis=1)

    grouped_df.insert(9, 'TOTAL1', total1) #inserting in specified location
    grouped_df['TOTAL2'] = total2 #creating new column

    #final_output
    print(grouped_df)

    # Creating the csv file
    grouped_df.to_csv(output_file_name, index=False)

    # Connect to the SQLite database
    conn = sqlite3.connect("Electric_Report.db")
    
    # Use the to_sql method to create a table and insert data
    grouped_df.to_sql("Electric_report", conn, index=False, if_exists='replace')

    # Commit changes and close the connection
    conn.commit()    
    conn.close()

except (FileExistsError, FileNotFoundError):
    print("No file named : "+input_file_name)
except:
    print("Sorry, some error has occured.")