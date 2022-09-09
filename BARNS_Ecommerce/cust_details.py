from Fileoperations import *
from admin import *
from config import *
import re


def check_email(email):
    # regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    # pass the regular expression
    # and the string into the fullmatch() method
    if (re.fullmatch(regex, email)):
        return True
    else:
        return False

#customer information

def cust_registration():  #New user Registration
    Cname = input('Enter Name: ')
    while(1):
        CuserEmail = input('Enter User Email: ')
        check = check_email(CuserEmail) #checking customer email
        if check :
            break
        else:
            print('Invalid User Email')

    Cpwd = input('Enter password: ')
    Caddress = input('Enter address: ')

    # CustInfo = {'NAME':Cname,'USERNAME':CuserEmail,'PASSWORD':Cpwd,'ADDRESS':Caddress}
    CustInfo = [Cname,CuserEmail,Cpwd,Caddress]
    cust_filewrite(CustInfo) #storing New user Information
    return CuserEmail


def cust_filewrite(data):
    # Appending new user information into the Customer File
    # writing to csv file
    with open(Customer_filename, 'a', newline="") as csvfile:
        # creating a csv writer object
        csvwriter = csv.writer(csvfile)
        # writing the fields
        csvwriter.writerow(data)

def login_verification(cust_loginId, cust_pwd):   #Login verification
    df = pd.read_csv(Customer_filename)
    #print(df)
    user_emails = df['USERNAME'].tolist()
    user_pwd = df['PASSWORD'].tolist()

    #Admin User checking
    if cust_loginId == user_emails[0]:
        # print('Welcome to the admin Portal')
        if cust_pwd == user_pwd[0]:
            admin_transactcions()
            return True
        else:
            print('Password Incorrect')
            return False

    if cust_loginId in user_emails : #checking for UsedId
       index= user_emails.index(cust_loginId)
       #print(index)
       if cust_pwd == user_pwd[index] : # checking UserId to password matching
           # cust_add = df['ADDRESS'].loc[index]
           # print(cust_add)
           #print('Login successful')
           return True
       else:
           print('Password Incorrect')
           return False
    else:
       print('UserId not found please Signup')
       return False


class Get_customer_info():

    def __init__(self):
        self.df = pd.read_csv(Customer_filename)
        self.Pdf = self.df.set_index('USERNAME')

    def get_customer(self, user_id):
        customer = self.Pdf.loc[user_id]
        return customer

    def get_customer_pwd(self, user_id):
        customer_pwd = self.Pdf.at[user_id, 'PASSWORD']
        # print(customer_pwd)
        return customer_pwd

    def get_customer_name(self, user_id):
        customer_name = self.Pdf.at[user_id, 'NAME']
        # print(customer_name)
        return customer_name

    def get_customer_address(self, user_id):
        customer_address = self.Pdf.at[user_id, 'ADDRESS']
        # print(customer_address)
        return customer_address



