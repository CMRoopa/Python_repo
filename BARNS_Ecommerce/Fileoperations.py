
from config import *


# user Information file initialization
def cust_fileinit():
    #To initialize few customers to the Customer list
    #Not required to call everytime
    fields = ['NAME', 'USERNAME', 'PASSWORD', 'ADDRESS']
    # data rows of csv file
    rows = [['Nikhil', 'Nikhil@gmail.com', 'Nikhilpwd', 'USA'],
            ['Sanchit', 'Sanchit@gmail.com', 'Sanchitpwd', 'USA'],
            ['Aditya', 'Aditya@gmail.com', 'Adityapwd', 'USA'],
            ['Sagar', 'Sagar@gmail.com', 'Sagarpwd', 'USA'],
            ['Prateek', 'Prateek@gmail.com', 'Prateekpwd', 'USA']]

    # writing to csv file
    with open(Customer_filename, 'w', newline="") as csvfile:
        #print(filename)
        # creating a csv writer object
        csvwriter = csv.writer(csvfile)
        # writing the fields
        csvwriter.writerow(fields)
        # writing the data rows
        csvwriter.writerows(rows)



