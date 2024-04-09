from flask import Flask, render_template, request, redirect, url_for, session
import secrets
import process_data  # Importing the file to process the data
import pymysql

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)  # Set a secret key for sessions

# Define a global variable to store the available tables
available_tables = []

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        host = request.form['host']
        username = request.form['username']
        password = request.form['password']
        database = request.form['database']
        
        # Store values in session
        session['host'] = host
        session['username'] = username
        session['password'] = password
        session['database'] = database
        
        # Call a function from another file to get available tables
        global available_tables
        available_tables = process_data.get_tables(host, username, password, database)

        return redirect(url_for('tables'))
    return render_template('index.html')

@app.route('/tables', methods=['GET', 'POST'])
def tables():
    global available_tables
    if request.method == 'POST':
        selected_table = request.form['selected_table']
        # Electric_report is the default table name
        table_name = request.form.get('table_name', 'Electric_report')

        # Retrieve values from session
        host = session.get('host')
        username = session.get('username')
        password = session.get('password')
        database = session.get('database')
        
        # Call clean_table function with provided arguments
        process_data.clean_table(host, username, password, database, selected_table, table_name)

        return redirect(url_for('success'))
    return render_template('tables.html', tables=available_tables)

@app.route('/success')
def success():
    return 'Cleaned Database created successfully!'

if __name__ == '__main__':
    app.run(debug=True)
