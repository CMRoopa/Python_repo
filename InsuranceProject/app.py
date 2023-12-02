from fileinput import filename
import pandas as pd
from flask import *
import os
from werkzeug.utils import secure_filename
from bs4 import BeautifulSoup

import pyodbc

import csv
import json

import re
 
UPLOAD_FOLDER = os.path.join('my_sql_temp_data')

DATA_FOLDER = os.path.join('my_sql_temp_user_info', 'data.csv')
# Define allowed files
ALLOWED_EXTENSIONS = {'csv'}
 
UPLOAD_FOLDER = os.path.join('my_sql_temp_data')

DATA_FOLDER = os.path.join('my_sql_temp_user_info', 'data.csv')
# Define allowed files
ALLOWED_EXTENSIONS = {'csv'}
 
app = Flask(__name__)
 
# Configure upload file path flask
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
 
app.config['DATA_FOLDER'] = DATA_FOLDER

app.secret_key = 'This is your secret key to utilize session in Flask'
 

@app.route('/')
@app.route('/login', methods =['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        
        df = pd.read_csv(DATA_FOLDER)
        #print (df)
        #print (username)
        #print(df["USERNAME"] == username)
        #account = df["USERNAME"] == username
        
        if username in df['USERNAME'].values:
            session['loggedin'] = True
            session['id'] = username
            session['username'] = username
            msg = 'Logged in successfully !'
            return render_template('index.html', msg = msg)
        else:
            msg = 'Incorrect username / password !'
    return render_template('login.html', msg = msg)


 
@app.route('/', methods=['GET', 'POST'])
def uploadFile():
    if request.method == 'POST':
      # upload file flask
        f = request.files.get('file')
 
        # Extracting uploaded file name
        data_filename = secure_filename(f.filename)
        print(data_filename)
 
        f.save(os.path.join(app.config['UPLOAD_FOLDER'],
                            data_filename))
 
        session['uploaded_data_file_path'] = os.path.join(app.config['UPLOAD_FOLDER'], data_filename)
 
        return render_template('index2.html')
    return render_template("index.html")


@app.route('/register', methods =['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form  :
        username = request.form['username']
        password = request.form['password']

        df = pd.read_csv(DATA_FOLDER)
        print (df)
        print(DATA_FOLDER)
        #account = df.loc[df['USERNAME'] ==username][username, password]
       
        if username in df["USERNAME"]:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', username):
            msg = 'Invalid email address !'
        elif not username or not password:
            msg = 'Please fill out the form !'
        else:
            df.loc[len(df)] = [username,password]
            new_info = [username,password]
            #df.to_csv(DATA_FOLDER)
            # Appending new user information into the Customer File
            # writing to csv file
            with open(DATA_FOLDER, 'a', newline="") as csvfile:
                # creating a csv writer object
                csvwriter = csv.writer(csvfile)
                # writing the fields
                csvwriter.writerow(new_info)
            msg = 'You have successfully registered !'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html', msg = msg)

def missing_value_display():
    pass
 
@app.route('/show_data')
def showData():
    # Uploaded File Path
    data_file_path = session.get('uploaded_data_file_path', None)
    print(data_file_path)
    type_of_file = data_file_path.split('.')
    print(type_of_file[1])
    # read csv
    if (type_of_file[1] == "csv"):        

            uploaded_df = pd.read_csv(data_file_path,encoding='unicode_escape')
            data_columns = uploaded_df.columns.values.tolist()
            data_describe = uploaded_df.describe()
            data_describe_html = data_describe.to_html()
            missing_value_display()
            return render_template('show_csv_data.html',
                           data_var_col=data_columns,data_var_desc = data_describe_html )
        
    elif (type_of_file[1] == "xml"):  
        with open(data_file_path, 'r') as f:
            file = f.read() 
        # 'xml' is the parser used. For html files, which BeautifulSoup is typically used for, it would be 'html.parser'.
        soup = BeautifulSoup(file, 'xml')
        # Parse the XML with Beautiful Soup
        # Extract teacher information
        teachers = []
        for teacher_elem in soup.find_all('teacher'):
            teacher_info = {
                            'name': teacher_elem.find('name').text,
                            'age': teacher_elem.find('age').text,
                            'subject': teacher_elem.find('subject').text
                            }
            teachers.append(teacher_info)

        print ("rendering xml --------------------")
        print(teachers)
        return render_template('show_xml_data.html',teachers = teachers)


    elif (type_of_file[1] == "json"):
        with open(data_file_path, 'r') as file:
            data = json.load(file)
        return render_template('show_json_data.html', data=data)
    


@app.route('/tableau_dashboard')
def tableau_dashboard():
    return render_template('tableau_dashboard.html')

@app.route('/database_details')
def dbDetails():
    
    server = 'POLA_LAPTOP\SQLEXPRESS'
    database = 'EmployeeDB'
    username = r'POLA_LAPTOP\roopa'
    password = 4184
    trust ='yes'

    # Specify the ODBC driver in the connection string
    connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password};trusted_connection={trust};'

    # Establish a connection
    connection = pyodbc.connect(connection_string)

    # Create a cursor
    cursor = connection.cursor()

    # Example query
    cursor.execute("SELECT * FROM EmpDetails")
    rows = cursor.fetchall()

    print (rows)

    # Close the cursor and connection
    cursor.close()
    connection.close()
    return render_template('database_details.html', rows=rows)

 
 
if __name__ == '__main__':
    app.run(debug=True)