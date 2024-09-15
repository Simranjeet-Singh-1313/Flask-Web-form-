import pyodbc
from flask import Flask, request, redirect, url_for, render_template_string

app = Flask(__name__)

# Azure SQL Database connection details
server = 'your-server-name.database.windows.net'  # Replace with your Azure SQL Server
database = 'MIS'  # Replace with your database name
username = 'your-username'  # Replace with your database username
password = 'your-password'  # Replace with your database password
driver = '{ODBC Driver 17 for SQL Server}'  # Ensure you have installed this driver

# Function to connect to the database
def connect_db():
    conn = pyodbc.connect(f'DRIVER={driver};SERVER={server};PORT=1433;DATABASE={database};UID={username};PWD={password};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')
    return conn

# HTML template as a string
html_form = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Flask Form</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        label { display: inline-block; width: 100px; }
        input { margin-bottom: 10px; }
    </style>
</head>
<body>
    <h1>Submit Your Info</h1>
    <form method="POST">
        <label for="name">Name:</label>
        <input type="text" id="name" name="name" required>
        <br><br>
        <label for="email">Email:</label>
        <input type="email" id="email" name="email" required>
        <br><br>
        <input type="submit" value="Submit">
    </form>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']

        # Connect to the database and insert the form data
        connection = connect_db()
        cursor = connection.cursor()

        # Insert form data into the database (replace 'YourTableName' with the actual table name)
        cursor.execute("INSERT INTO YourTableName (name, email) VALUES (?, ?)", (name, email))
        connection.commit()
        cursor.close()
        connection.close()

        return redirect(url_for('success'))
    return render_template_string(html_form)

@app.route('/success')
def success():
    return "Form submitted successfully!"

if __name__ == '__main__':
    app.run(debug=True)
