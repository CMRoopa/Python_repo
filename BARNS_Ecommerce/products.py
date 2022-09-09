from Product_order import *

from random import randint

from config import *

def products(cust_loginId):
    #Main function in Products Section
    products_df = products_display() #function to display all products to the user
    user_plist = product_selection(products_df)  # Selecting the product by user
    try:
        if len(user_plist) > 0: #check for products choosen by user
            order_section(products_df,user_plist,cust_loginId)
    except TypeError :
        print('No products are choosen to buy ')
        print('Thank you from BARNS')
    return


def products_display():
    #function to display products to the customer
    df = pd.read_csv(Products_filename)
    products_df = df.set_index('Product_Id')
    print(products_df)
    return products_df


def product_selection(products_df):
    #Function for product selection by the customer
    df_index = products_df.index
    product_id_list = []
    while (1):
        product_ld = input('Did you found anything intersting to buy. Please press Y/N : ')
        if product_ld == 'Y' or product_ld == 'y':
            while (1):
                try :
                    product_id = input('please select appropriate product number or press 0 to exit: ')
                    if int(product_id) in df_index:  #check whether the selected product id is present in the displayed products
                        sel_product = products_df.loc[int(product_id)]
                        print('The selected product is \n{} : '.format(sel_product))
                        product_id_list.append(product_id) #Adding to customer cart
                        print(product_id_list)
                        while (1):
                            CI = input('Do you like to buy another product. if Y/N : ') #check whether the customer likes to buy another product
                            if CI == 'y' or CI == 'Y':
                                products_display() #function call to display the products again
                                break
                            elif CI == 'N' or CI == 'n':
                                return product_id_list

                            else:
                                print('Please Enter appropriate option \n')
                    elif int(product_id) == 0:
                        break
                    else :
                        print('Please Enter correct Product Id Number.\n')
                except ValueError:
                    print('Please Enter Appropriate product Number.')
            break
        elif product_ld == 'N' or product_ld == 'n':
            print('Thank you from BARNS')
            break
        else:
            print('Please Enter Appropriate option.')
            # break



# def products(cust_loginId)
      #To generate products randomly without Admin section
#     Pcolor = ['white', 'black', 'green', 'blue', 'red', 'yellow', 'purple', 'violet', 'orange', 'grey']
#     Psection = ['MALE', 'FEMALE', 'UNISEX']
#     # price = randint(10,50)
#     Ptype = ['top', 'bottom', 'thermal', 'jacket']
#
#     category = {1: 'color', 2: 'section', 3: 'price', 4: 'type'}
#     product_list = []
#     for i in range(5):
#         color = Pcolor[randint(0, 9)]
#         section = Psection[randint(0, 2)]
#         price = randint(10, 50)
#         type = Ptype[randint(0, 3)]
#         product = [section, type, color, '${}'.format(price)]
#         product_list.append(product)
#     products_df = products_display(product_list)
#     user_plist = product_selection(product_list)
#     try:
#         if len(user_plist) > 0:
#             order_section(products_df,user_plist,cust_loginId)
#     except TypeError :
#         print('No products are choosen to buy ')
#         print('Thank you from BARNS')
#     return


