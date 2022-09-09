
from config import *

class BARNSadmin ():
    #class for Admin operations
    def __int__(self):
        pass

    def view_all_products(self):
        #Method to view all products by admin
        with open(Products_filename, 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            for row in csvreader:
                print(row)

    def add_product(self): #adding new product to  product file
        product_id = input('Enter new product id: ')
        product_section = input('Enter product section: ')
        product_type = input('Enter product type: ')
        product_color = input('Enter product color: ')
        product_size = input('Enter product size: ')
        product_price = input('Enter product price: ')
        #new_product = {'Product_Id':product_id,'SECTION':product_section,'TYPE':product_type,'COLOR':product_color,'SIZE':product_size,'PRICE':product_price}
        new_product = [product_id,product_section,product_type,product_color,product_size,product_price]
        print(new_product)
        #writing to csv file
        with open(Products_filename, 'a', newline="") as csvfile:
            # creating a csv writer object
            csvwriter = csv.writer(csvfile)
            # writing the fields
            csvwriter.writerow(new_product)

    def delete_product(self): #To delete a product from Product File
        product_id = input('Enter the product id of the product to delete: ')
        newlines = list()
        with open(Products_filename,'r', newline="")as readFile:
            reader = csv.reader(readFile)
            for row in reader:
                newlines.append(row)
                for field in row:
                    if field == product_id:
                        newlines.remove(row)
        with open(Products_filename,'w', newline="")as writeFile:
            writer = csv.writer(writeFile)
            writer.writerows(newlines)


def admin_transactcions():
    #Main function in Admin section
    print('Welcome to the admin Portal')
    admin_obj = BARNSadmin() #creating a object of BARNSadmin class
    print(' V ---  To view all the products ')
    print(' A ---  To add a product')
    print(' D --- To delete a product')
    print('X --- To exit')
    while (1):
        admin_choice = input('Please Enter one of the appropriate options to proceed : ').lower()

        if admin_choice == 'v':
            admin_obj.view_all_products()
        elif admin_choice == 'a':
            admin_obj.add_product()
        elif admin_choice == 'd':
            admin_obj.delete_product()
        elif admin_choice == 'x':
            exit(0)
        else:
            print('Please choose appropriate option: ')