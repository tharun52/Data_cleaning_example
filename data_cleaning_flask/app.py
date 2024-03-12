from flask import Flask, render_template, request, redirect, url_for
import process_data  # Importing the file to process the data

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        host = request.form['host']
        username = request.form['username']
        password = request.form['password']
        database = request.form['database']
        
        # Call a function from another file to process the data
        process_data.clean_table(host, username, password, database)
        
        return redirect(url_for('success'))
    return render_template('index.html')

@app.route('/success')
def success():
    return 'Cleaned Database created successfully!'

if __name__ == '__main__':
    app.run(debug=True)
