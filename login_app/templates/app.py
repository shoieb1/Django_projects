from flask import Flask, render_template, request
import pyodbc

app = Flask(__name__)

# Database connection
conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};'
                      'SERVER=<your_server_name>;'
                      'DATABASE=<your_database_name>;'
                      'UID=<your_username>;'
                      'PWD=<your_password>')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Users (Name) VALUES (?)", name)
    conn.commit()
    return f"Hello, {name}!"

if __name__ == '__main__':
    app.run(debug=True)