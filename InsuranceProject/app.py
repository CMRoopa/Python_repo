from fileinput import filename
import pandas as pd
from flask import *
import os
from werkzeug.utils import secure_filename

import csv

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
 
 
@app.route('/show_data')
def showData():
    # Uploaded File Path
    data_file_path = session.get('uploaded_data_file_path', None)
    # read csv
    uploaded_df = pd.read_csv(data_file_path,
                              encoding='unicode_escape')
    print(uploaded_df)
    # Converting to html Table
    #uploaded_df_html = uploaded_df.to_html()
    data_columns = uploaded_df.columns.values.tolist()
    data_describe = uploaded_df.describe()
    
    data_describe_html = data_describe.to_html()
    #return render_template('show_csv_data.html',
                          # data_var=uploaded_df_html)
    return render_template('show_csv_data.html',
                           data_var_col=data_columns,data_var_desc = data_describe_html )


@app.route('/tableau_dashboard')
def tableau_dashboard():
    return render_template('tableau_dashboard.html')

 
 
if __name__ == '__main__':
    app.run(debug=True)