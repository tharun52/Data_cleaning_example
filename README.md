### Data Cleaning with Pandas and SQL

This program utilizes pandas to clean up a CSV file and generates an SQL file as the output. The example provided uses an electric report, but you can customize it to suit your requirements. Follow the comments in the code for instructions.

## Basic Python file

To run the raw Python file with only the basic functionality, type the following command in your terminal:

```bash
python main.py
```


## Flask Integration
To run the Flask program, follow these steps:

Navigate to the data_cleaning_flask directory and Run the Flask application with the command:
```bash
cd data_cleaning_flask
flask run
```
Open your web browser and go to the localhost link provided by Flask.

Enter the following details:

1. Host Link: If running locally, type "localhost"; otherwise, enter the actual host link. 
2. Username: If running locally, type "root"; otherwise, enter the actual username.
3. Password: Your database password.
4. Database Name: The name of your database.
Once connected successfully, the list of tables should be displayed along with the option to change the table name. If successful, a database with your table name should be created in the project folder.

## Viewing the Database as CSV in Excel (optional)

In the terminal, run the following Python script to convert the database data into a CSV file and open it in Excel:

```bash
python read_db.py
```
Follow the prompts to enter the name of your database. This script will convert the data from **table_name**.db into a CSV file named **table_name**.csv, which will be automatically opened in MS Excel.

Feel free to customize and extend this program as needed for your data cleaning tasks.
