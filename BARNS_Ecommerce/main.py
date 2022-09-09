from Fileoperations import *
from products import *
from cust_details import *
from products import *


# main file to start the BARNS
print ("Welcome to BARNS") #Welcome note

# cust_fileinit() #Customers file initialization

while (1):
    cus_Login = input('Are you a Registered user press Y/N:')
    # To check whether the customer is registered or new
    if cus_Login == 'Y' or cus_Login == 'y':
        cust_loginId = input('Enter Email: ')
        cust_pwd = input('Enter password: ')
        login_success = login_verification(cust_loginId,cust_pwd) #Function call for login verification
        if(login_success == True):
            print('Login successful')
            products(cust_loginId)
            break
        else:
            print('Login unsuccessful. UserId and Password are case-sensitive')
            #break
    elif cus_Login == 'N' or cus_Login == 'n':
        print('sign up for Barns')
        cust_loginId = cust_registration() #New user Registration
        if cust_loginId :
            print('Registration Successful')
            products(cust_loginId)
        else :
            print('Registration Unsuccessful, Please try again')
        break
    else :
        print('please select Appropriate option') #checking for wrong option selection


