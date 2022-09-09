from typing import List, Any
from cust_details import *
from datetime import date
from datetime import timedelta
from products import *
from config import *

def order_section(products_df, user_plist, cust_loginId):
    #main function in order section
    product_price: list[Any] = []
    order_df = products_df
    order_series = order_df['PRICE'].squeeze()

    for i in user_plist:
        product_price.append(order_series.get(key=int(i)))

    tc = total_cost(product_price)  # To calculate total order Price
    Total_Price = '${}'.format(tc)
    while (1):
        check = input('Total cost is ${}. Do you like to checkout Y/N: '.format(tc))
        if check == 'Y' or check == 'y': #Order checkout permission
            order_checkout(cust_loginId, products_df, user_plist, Total_Price) #Going for order checkout
            break
        elif check == 'N' or check == 'n':
            print('Thank you from Barns')
            return 0
        else:
            print('please select appropriate option')


def total_cost(product_price):
    #Function to calculate total order price/cost
    tc = 0
    for x in product_price:
        tc = tc + int(x.replace('$', ''))
    return tc


def order_checkout(cust_loginId, products_df, user_plist, order_price):
    #Function for order checkout
    customer_info = Get_customer_info() #creating an object of Get_customer_info class
    while (1):
        Acheck = input('Is Delivery address is same as Registered Address. Enter Y/N :').lower()
        if Acheck == 'y':
            delivery_address = customer_info.get_customer_address(cust_loginId)
            break
        elif Acheck == 'n':
            delivery_address = input('Please Enter the order Delivery Address : \n')
            break
        else:
            print('Please Enter appropriate option\n')
    payment_card_details = payment_section() #  Function for payment section
    c_order = Cust_order(cust_loginId, user_plist, order_price, payment_card_details, delivery_address)
    #creating object of Cust_order class
    order_id = c_order.generate_orderid() #To generate new order id
    # print(order_id)
    c_order.generate_order() #New order creation
    c_order.display_order() #Displaying the order


def payment_section():
    # Function for payment section
    while (1):
        try:
            Card_no = input('Please Enter 10 digit Payment card Number: ')
            if 1000000000 < int(Card_no) < 10000000000: #checking for 10 digit card number
                while (1):
                    cvv = input('Enter cvv number : ')
                    if 100 < int(cvv) < 1000:
                        print('Payment successful\n')
                        return Card_no

                    else:
                        print('Enter proper cvv number \n ')
            else:
                print('Enter proper card number \n ')
        except ValueError :
            print('Enter proper card number \n ')

class Get_product_info():
    #class to get information on Product based on Product ID
    def __init__(self):
        self.df = pd.read_csv(Products_filename)
        self.Pdf = self.df.set_index('Product_Id')

    def get_product(self,product_no):
        product = self.Pdf.loc[product_no]
        # print(product)
        return product
    def get_product_size(self,product_no):
        product_size = self.Pdf.at[product_no, 'SIZE']
        # print(product_size)
        return product_size
    def get_product_color(self,product_no):
        product_color = self.Pdf.at[product_no, 'COLOR']
        # print(product_color)
        return product_color
    def get_product_type(self,product_no):
        product_type = self.Pdf.at[product_no, 'TYPE']
        # print(product_type)
        return product_type
    def get_product_section(self,product_no):
        product_section = self.Pdf.at[product_no, 'SECTION']
        # print(product_section)
        return product_section

class Cust_order(Get_product_info):
    #Class for Order section which is inheriting the Get_product_info class
    def __init__(self, cust_loginId, user_plist, order_price, payment_card_details, delivery_address):
        super().__init__()
        # print('cust_order class')
        self.cust_loginId = cust_loginId
        self.user_plist = user_plist
        self.order_price = order_price
        self.payment_card_details = payment_card_details
        self.delivery_address = delivery_address
        self.Order_id = 0
        self.newOrder = []

    def generate_orderid(self):
        odf = pd.read_csv(Order_filename)
        # orders_df = odf.set_index('Order_ID')
        last_orderId = odf['Order_ID'].iloc[-1]
        self.Order_id = int(last_orderId) + 1
        return self.Order_id

    def generate_order(self):
        Norder = [self.Order_id, self.user_plist, self.cust_loginId, self.order_price, self.payment_card_details,
                  self.delivery_address]
        # print(Norder)
        with open(Order_filename, 'a', newline="") as csvfile:
            # creating a csv writer object
            csvwriter = csv.writer(csvfile)
            # writing the fields
            csvwriter.writerow(Norder)

    def display_order(self):
        print('Order Details are:')
        print('Order Id: {}\n'.format(self.Order_id))
        print('Delivery Address: {}\n'.format(self.delivery_address))
        print('Product details are: \n')
        i=0
        for x in self.user_plist:
            i = i+1
            print('{}. {} \n '.format(i,self.get_product(int(x))))
        today = date.today() #to get system date to give delivery date
        date1 = today + timedelta(days=10)
        # Textual month, day and year
        date2 = date1.strftime("%B %d, %Y")
        print('Order successful')
        print('Order will be delivered on or before {}'.format(date2)) #To print order delivery date
        print('Thank you from BARNS. VISIT AGAIN')
