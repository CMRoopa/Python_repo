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


# flask --app app  run --debug  
# py -m venv env      -- To create vitrual environment
# env\Scripts\activate   -- To activate the virtual environment