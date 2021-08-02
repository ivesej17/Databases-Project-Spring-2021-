import time
import mysql.connector
from mysql.connector import Error
conn = mysql.connector.connect(user = "root", password = "BaiWei1091", database = "Store", port = 3306)
cursor = conn.cursor()


tables = ["account", "accounts_payable", 
          "business_payments", "business_purchase", 
          "customer", "customer_purchase", "inventory",
          "shipment", "vendor"]

fields = ["acc_payable_id", "amount_paid", "amount_pending", "pay_due_date"]

#Functions to parse strings and get information from user
#Get string with specified number of characters
def get_string_lim(limit, field):
    user_input = input ("Please enter string (max " + limit + " char) for '" + field + "'\n")
    while True:
        if len(user_input) < int(limit):
            break
        user_input = input ("Exceeds Max, Please enter string (max " + limit + " char)\n")
    return user_input

#Get string that is an integer
def get_integer(field):
    user_input = input("Please enter positve integer for '"+ field +"':\n")
    if user_input == "NULL" or user_input == "null":
        return user_input
    while True:
        if user_input.isnumeric():
            break
        user_input = input("Not positive integer, Please enter positve integer:\n")
    return user_input

#Get string that is a dollar and cents amount
def get_dollars_cents(field):
    user_input1 = input("Please enter dollar amount for '" + field + "':\n")
    while True:
        if user_input1.isnumeric():
            break
        user_input1 = input("Not positive integer, Please enter dollar amount:\n")
    user_input2 = input("Please enter cent amount as two decimal digits '00' - '99':\n")
    while True:
        if user_input2.isnumeric() and len(user_input2) == 2:
            break
        user_input2 = input("Not positive integer or not length 2, Please enter cent amount:\n")
    return user_input1 + "." + user_input2

#Get date as string value
def get_date(field):
    print("For field '" +field +"'\n")
    user_input1 = input("Please enter a year as 4 decimals digits:\n")
    if user_input1 == 'NULL' or user_input1 == 'null':
        return user_input1
    while True:
        if user_input1.isnumeric() and len(user_input1) == 4:
            break
        user_input1 = input("Either not digits or not length 4: please enter year:\n")
    user_input2 = input("Please enter a month as 2 decimal digits:\n")
    while True:
        if user_input2.isnumeric() and len(user_input2) == 2:
            if int(user_input2) < 13:
                break
        user_input2 = input("Either not digits, not length 2, or exceeds range: please enter month:\n")
    user_input3 = input("Please enter day as two decimal digits:\n")
    while True:
        if user_input3.isnumeric() and len(user_input3) == 2:
            if int(user_input3) < 32:
                break
        user_input3 = input("Either not digits, not length 2, or exceeds range: please enter day:\n")
    return user_input1 + "-" + user_input2 + "-" + user_input3


#Get dateTime as a string value
def get_datetime(field):
    date = get_date(field) + " "
    user_input1 = input("Please enter hour as 2 decimal digits:\n")
    while True:
        if user_input1.isnumeric() and len(user_input1) == 2:
            if int(user_input1) < 24:
                break
        user_input1 = input("Either not digits, not length 2, or exceeds range: please enter hour:\n")
    user_input2 = input("Please enter a minutes as 2 decimal digits:\n")
    while True:
        if user_input2.isnumeric() and len(user_input2) == 2:
            if int(user_input2) < 60:
                break
        user_input2 = input("Either not digits, not length 2, or exceeds range: please enter minutes:\n")
    user_input3 = input("Please enter seconds as two decimal digits:\n")
    while True:
        if user_input3.isnumeric() and len(user_input3) == 2:
            if int(user_input3) < 60:
                break
        user_input3 = input("Either not digits, not length 2, or exceeds range: please enter seconds:\n")
    return date + user_input1 + ":" + user_input2 + ":" + user_input3
    
#Gets user input for generic menu
def get_user_option(low,high):
    while True:
        user_input = input('\nPlease Select a Number ( ' + low + ' - ' + high + ' )\n')
        if user_input.isnumeric():
            if int(user_input) >= int(low) and int(user_input) <= int(high):
                return user_input
        






#Pulling Sequal queries into python
#Displays a text based mysql query
def push_select_query(query):
    columns = query[0:query.find("FROM")]
    print(columns)
    cursor.execute("SELECT " + query)
    row = cursor.fetchone()
    while row is not None:
        print(row)
        row = cursor.fetchone()
    print("\n\n")

#Special code for accounts Payable for clarity
def push_select_query_account_payable(query):
    i = 0
    j = 0
    columns = query[0:query.find("FROM")]
    print(columns)
    cursor.execute("SELECT " + query)
    rows = cursor.fetchall()
    max = len(rows)
    for row in rows:
        while i < 4 and j < max:          
            print(fields[i] + ": " + str(rows[j][i]) + "   ", end='')
            i = i + 1
        i = 0
        j = j + 1
        print("")
    print("\n\n")
    return rows


    

#Displays a query and returns the rows
def search_select_query(query):
    columns = query[0:query.find("FROM")]
    print(columns)
    cursor.execute("SELECT " + query)
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    print("\n\n")
    return rows

#Displays a query but does not return the rows
def search_select_silent_query(query):
    cursor.execute("SELECT " + query)
    rows = cursor.fetchall()
    return rows

def insert_try(query, args):
    try:
        cursor.execute(query, args)
        print("Insert Completed!\n\n\n\n")
        conn.commit()
    except Error as error:
        print(error)

def call_proc(procedure,args):
    cursor.callproc(procedure,args)
    for result in cursor.stored_results():
        print("\n")
        print(result.fetchall())



#Insert functions for every table, takes a string or int for every column and inserts it
# into the defined table
def insert_account(account_number, account_owner, vendor_id, balance):
    query = "INSERT INTO account(account_number, account_owner, vendor_id, balance) " \
            "VALUES(%s,%s,%s,%s)"
    args = (account_number, account_owner, vendor_id, balance)
    insert_try(query, args)

def insert_inventory(product_id, product_name, quantity, retail_price):
    query = "INSERT INTO inventory(product_id, product_name, quantity, retail_price) " \
            "VALUES(%s,%s,%s,%s)"
    args = (product_id, product_name, quantity, retail_price)
    insert_try(query, args)

def insert_shipment(shipment_id, date_shipped, date_est_arrival, date_arrived):
    query = "INSERT INTO shipment(shipment_id, date_shipped, date_est_arrival, date_arrived) " \
            "VALUES(%s,%s,%s,%s)"
    args = (product_id, product_name, quantity, retail_price)
    insert_try(query, args)

def insert_vendor(vendor_id, vendor_name, product_name, product_id, wholesale_price):
    query = "INSERT INTO vendor(vendor_id, vendor_name, product_name, product_id, wholesale_price) " \
            "VALUES(%s,%s,%s,%s,%s)"
    args = (product_id, product_name, quantity, retail_price)
    insert_try(query, args)

def insert_accounts_payable(acc_payable_id,amount_paid,amount_pending,pay_due_date):
    query = "INSERT INTO accounts_payable(acc_payable_id,amount_paid,amount_pending,pay_due_date) " \
            "VALUES(%s,%s,%s,%s)"
    args = (acc_payable_id,amount_paid,amount_pending,pay_due_date)
    insert_try(query, args)


def insert_customer(customer_id, customer_name):
    query = "INSERT INTO customer(customer_id,customer_name) " \
            "VALUES(%s,%s)"
    args = (customer_id, customer_name)
    insert_try(query, args)


def insert_business_purchase(acc_payable_id, vendor_id, date_time, shipment_id, product_id, quantity, wholesale_price):
    query = "INSERT INTO business_purchase(acc_payable_id, vendor_id, date_time, shipment_id, product_id, quantity, wholesale_price)" \
            "VALUES(%s,%s,%s,%s,%s,%s,%s)"
    args = (acc_payable_id, vendor_id, date_time, shipment_id, product_id, quantity, wholesale_price)
    insert_try(query, args)


def insert_business_payments(acc_payable_id, trans_id, date_time, transfer_amount, from_account_number, account_number):
    query = "INSERT INTO business_payments(acc_payable_id, trans_id, date_time, transfer_amount, from_account_number, account_number)" \
            "VALUES(%s,%s,%s,%s,%s,%s)"
    args = (acc_payable_id, trans_id, date_time, transfer_amount, from_account_number, account_number)
    insert_try(query, args)


def insert_customer_purchase(purchase_id, customer_id, product_id, retail_price, quantity, total, payment_method, account_number, date_time):
    query = "INSERT INTO customer_purchase(purchase_id, customer_id, product_id, retail_price, quantity, total, payment_method, account_number, date_time)" \
            "VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    args = (purchase_id, customer_id, product_id, retail_price, quantity, total, payment_method, account_number, date_time)
    insert_try(query, args)







#Helper funtion for displaying table: changes number of rows shown
def display_table_loop_change_range():
    print("\n(20 rows is default and enter -1 for all rows)")
    user_num = input("Please input number of rows to be displayed:\n")
    while True:
        if user_num.isnumeric():
            break
        if user_num == '-1':
            break
        user_num = input("Please input number of rows to be displayed:\n")
    return user_num

  

#Displaying table contents Function
def display_table_loop(table_limit):

    while True:
        #prints tables and gives options
        print("0 main menu")
        for x in range(9):
            print(x+1, tables[x])
        print("10 Change number of rows shown (default: 20 Current: " + table_limit +" )\n")
        user_input = input("Select a table: ")
        print("\n")

        if user_input == '0':
            main_loop()

        #calls function to change number of rows displayed
        if user_input == '10':
            table_limit = display_table_loop_change_range()
            display_table_loop(table_limit)
    
        #Checks to ensure user_input an table index are valid integers
        if user_input.isnumeric():
            if int(user_input) < 10:
                table_index = int(user_input)
                print(tables[table_index-1])


        #displays modified number of rows
                if table_limit != '-1':
                    push_select_query("* FROM "+ tables[table_index-1] + " LIMIT 0," + table_limit)


        #displays all rows if table_limit == -1
                else:
                    push_select_query("* FROM "+ tables[table_index-1])
        print("\n")



#Helper function for displaying menu in record insert function
def insert_record_display_menu():
    while True:
        print("\n")
        print ("Please select a table to enter data into:\n")
        print("0 main menu")
        for x in range(9):
            print(x+1, tables[x])
        user_input = input("Select a table: ")
        print("\n")
        if user_input.isnumeric() or user_input == '-1':
            return user_input

#Insert Record Function
def insert_records():
    while True:
        user_option = insert_record_display_menu()
        if user_option == '0':
            main_loop()
        if user_option == '1':
            field1 = "A-" + get_integer("account_number")
            field2 = get_string_lim('100','account_owner')
            field3 = get_integer('vendor_id')
            field4 = get_integer('balance')
            insert_account(field1,field2,field3,field4)
        if user_option =='2':
            field1 = get_integer('acc_payable_id')
            field2 = get_dollars_cents('amount_paid')
            field3 = get_dollars_cents('amount_pending')
            field4 = get_date('payment_due_date')
            insert_accounts_payable(field1,field2,field3,field4)
        if user_option == '3':
            field1 = get_integer('acc_payable_id')
            field2 = get_integer('transaction_id')
            field3 = get_datetime('transaction date and time')
            field4 = get_dollars_cents('transfer amount')
            field5 = "A-" + get_integer('from account number (your account)')
            field6 = "A-" + get_integer('To account number (vendor account)')
            insert_business_payments(field1,field2,field3,field4,field5,field6)
        if user_option == '4':
            field1 = get_integer("accounts_payable_id")
            field2 = get_integer("vendor_id")
            field3 = get_datetime("time_of_purchase")
            field4 = get_integer("shipment_id")
            field5 = "P-" + get_integer("product_id")
            field6 = get_integer("quantity")
            field7 = get_dollars_cents("wholesale_price")
            insert_business_purchase(field1,field2,field3,field4,field5,field6,field7)
        if user_option == '5':
            field1 = get_integer("customer_id")
            field2 = get_string_lim('32', "customer_name")
            insert_customer(field1, field2)
        if user_option == '6':
            field1 = get_integer("purchase_id")
            field2 = get_integer('customer_id')
            field3 = 'P-' + get_integer('product_id')
            field4 = get_dollars_cents('retail_price')
            field5 = get_integer('quantity')
            field6 = float(field4) * float(field5)
            field7 = get_string_lim('20', 'payment method')
            field8 = 'A-' + get_integer('account payment will deposit into')
            field9 = get_datetime('date and time of transaction')
            insert_customer_purchase(field1,field2,field3,field4,field5,field6,field7,field8,field9)
        if user_option == '7':
            field1 = 'P-' + get_integer('product_id')
            field2 = get_string_lim('32', 'product name')
            field3 = get_integer('quantity')
            field4 = get_dollars_cents('retail_price')
            insert_inventory(field1,field2,field3,field4)
        if user_option == '8':
            field1 = get_integer('shipment_id')
            field2 = get_date('date shipped')
            field3 = get_date('estimated arrival date')
            field4 = get_date('arrival_date')
            insert_shipment(field1,field2,field3,field4)
        if user_option == '9':
            field1 = get_integer('vendor_id')
            field2 = get_string_lim('100', 'vendor name')
            field3 = get_string_lim('product name')
            field4 = 'P-' + get_integer('product_id')
            field5 = get_dollars_cents('wholesale price')
            insert_vendor(field1,field2,field3,field4,field5)

#Manage Inventory Function
def manage_inventory():    
    while True:
        print('Inventory Menu\n')
        print('0 Main Menu')
        print('1 Display all Inventory')
        print('2 Display products with less than N items remaining')
        print('3 Display Vendors that sell out of stock products')
        print('4 Display Vendors that sell low stock products (1 to 5 remaining)')
        print('5 Display all vendors and products they sell')
        print('6 Begin purchase order for product\n\n\n\n')
        user_option = get_user_option('0','7')
        if user_option == '0':
            break
        if user_option == '1':
            print("INVENTORY")
            push_select_query("product_id, product_name, quantity FROM inventory")
        if user_option == '2':
            number = get_user_option('0','10000')
            print("INVENTORY")
            push_select_query("product_id, product_name, quantity, retail_price FROM inventory WHERE quantity < " + number)
        if user_option == '3':
            print("VENDOR and INVENTORY")
            partial_query = (" vendor_id, v.product_id, v.product_name, wholesale_price FROM ")
            push_select_query(partial_query + "vendor AS v NATURAL JOIN inventory AS i WHERE quantity = 0")
        if user_option == '4':
            print("VENDOR and INVENTORY")
            partial_query = (" vendor_id, v.product_id, v.product_name, wholesale_price, quantity FROM ")
            push_select_query(partial_query + "vendor AS v NATURAL JOIN inventory AS i WHERE quantity > 0 AND quantity < 5")
        if user_option == '5':
            print("VENDOR")
            push_select_query(" vendor_id, vendor_name, product_name, product_id, wholesale_price FROM vendor")
        if user_option == '6':
            make_a_purchase()

#Function that defines making payments
def make_a_payment():
    t = time.localtime()  
    time_string = time.strftime("%Y-%m-%d %H:%M:%S", t)
    while True:
        print("OUTSTANDING ACCOUNTS PAYABLE")
        push_select_query_account_payable("acc_payable_id, amount_paid, amount_pending, pay_due_date FROM accounts_payable WHERE amount_pending > 0")
        print("Type 0 at any time to go back to main menu")
        print("Please enter an account payable ID to make a payment against")
        acc_payable_id = get_integer('acc_payable_id')
        acc_payable_row = search_select_silent_query("acc_payable_id FROM accounts_payable WHERE acc_payable_id = " + acc_payable_id)
        if(acc_payable_id == '0'):
            break
        if(len(acc_payable_row) == 1):
            print("Which account number would you like to pay from:\n\n")
            print("ACCOUNT")
            push_select_query("account_number, account_owner, balance FROM account WHERE TRUE = isnull(vendor_id)")
            from_account_number = "A-" + get_integer('from_account_number')
            from_account_number_row = search_select_silent_query("account_number, balance FROM account WHERE account_number = '" +from_account_number+"'")
            if(len(from_account_number_row) == 1):
                print("How much would you like to pay from the account?")
                transfer_amount = get_dollars_cents('transfer_account')
                if(float(from_account_number_row[0][1]) > float(transfer_amount)):
                    user_input = input("Would you like to continue with payment? (all inputs other than 'y' will cancel) (y/n)")
                    if(user_input == 'y'):
                        vendor_id_row = search_select_silent_query("vendor_id FROM business_purchase WHERE "+ acc_payable_id +" = acc_payable_id")
                        vendor_id = str(vendor_id_row[0][0])
                        account_number_row = search_select_silent_query("account_number FROM account WHERE vendor_id = " + vendor_id)
                        account_number = account_number_row[0][0]
                        trans_id_row = search_select_silent_query("max(trans_id) FROM business_payments")
                        trans_id = trans_id_row[0][0]
                        trans_id = trans_id + 1
                        insert_business_payments(acc_payable_id,trans_id, time_string, transfer_amount, from_account_number, account_number)
                    else:
                        print("Transaction cancelled\n")
                else:
                    print("payment amount higher than current balance, transaction cancelled.\n")
            else:
                print("account_number not found.\n")
        else:
            print("accounts payable id not found\n")


    

#make a purchase function
def make_a_purchase():
    t = time.localtime()  
    time_string = time.strftime("%Y-%m-%d %H:%M:%S", t)
    while True:
        print("\n\nPRODUCTS and WHOLESALE")
        push_select_query("v.product_id, i.product_name, wholesale_price FROM vendor AS v NATURAL JOIN inventory AS i ")
        print("Enter the product code to be purchased (number only no 'P-' necessary)")
        print("Type 0 to go back")
        product_id = "P-" + get_integer('product_id')
        print("\nVENDORS and SELECTED PRODUCT")
        product_rows = search_select_query("vendor_id, vendor_name, wholesale_price FROM vendor WHERE product_id = '"+ product_id + "'")
        if (product_id == "P-0"):
            break
        if len(product_rows) > 0:
            print("\n\n\n\nEnter one of the available vendor_ids")
            vendor_id = get_integer("vendor_id")
            vendor_row = search_select_silent_query("vendor_id, vendor_name, wholesale_price FROM vendor WHERE vendor_id = " + vendor_id)
            if len(vendor_row) == 1 :
                wholesale_price = vendor_row[0][2]
                print("Vendor Selected! Please enter quantity you wish to purchase")
                quantity = get_integer('quantity')
                if (int(quantity) > 0):
                    print("\n\nThe payment will be $")  
                    print(int(wholesale_price) * int(quantity))
                    print("\nACCOUNTS\n (Only shown here for reference, accounts will not be debited until payment is made")
                    push_select_query("account_number, account_owner, balance FROM account WHERE TRUE = isnull(vendor_id)")
                    print("\n\n")
                    user_input = input("\n\nWould you like to continue with purchase (press y to continue, all other inputs will end transaction)")
                    if(user_input == 'y'):
                        while True:
                            user_input = input("Would you like to manually input a payment due_date? (default date is tomorrow) (y/n)")
                            if(user_input == 'y'):
                                date_time = get_datetime('date_time')
                                break
                            if(user_input == 'n'):
                                break;
                            print("Transaction Processed\n\n\n\n")
                    else:
                        break
                    last_shipment_id = search_select_silent_query("max(shipment_id) FROM shipment")
                    last_acc_payable_id = search_select_silent_query("max(acc_payable_id) FROM accounts_payable")
                    acc_payable_id = last_acc_payable_id[0][0]
                    shipment_id = last_shipment_id[0][0]
                    shipment_id = shipment_id + 100
                    acc_payable_id = acc_payable_id + 10
                    insert_business_purchase(acc_payable_id, vendor_id, time_string, shipment_id,product_id, quantity, wholesale_price)
                    break
            else:
                 print("No Vendor with that ID found")
        else:
            print("No such product ID found")


def functions():
    t = time.localtime()  
    time_string = time.strftime("%Y-%m-%d %H:%M:%S", t)
    while True:
        print("\n\nSpecial Functions\n")
        print("0 main menu")
        print("1 function to return profit between two dates")
        print("2 procedure that returns all payments to a vendor between two dates")
        print("3 procedure shows all customer transactions between two dates")
        print("4 a query for all overdue accounts")
        user_input = get_user_option('0','4')
        if user_input == '0':
            break
        if user_input == '1':
            print("Net_Proft: Please enter the 1st date:")
            date1 = get_datetime('date1')
            user_input2 = input("Would you like to use to today's date for the second date (any input not 'y' will require date entry)")
            if(user_input2 =='y'):
                date2 = time_string
            else:
                date2 = get_datetime('date2')
            net_profit_row = search_select_silent_query("net_profit('"+date1+"','"+date2+"')")
            print("\nNet Profit between " + date1 + " and " + date2 + " was " + str(net_profit_row[0][0]))
        if user_input == '2':
            print("Vendor Payments: Please enter the 1st date:")
            date1 = get_datetime('date1')
            user_input2 = input("Would you like to use to today's date for the second date (any input not 'y' will require date entry)")
            if(user_input2 =='y'):
                date2 = time_string
            else:
                date2 = get_datetime('date2')
            call_proc("payments_to_vendor", [date1,date2])
        if user_input == '3':
            print("Customer_transactions: Please enter the 1st date:")
            date1 = get_datetime('date1')
            user_input2 = input("Would you like to use to today's date for the second date (any input not 'y' will require date entry)")
            if(user_input2 =='y'):
                date2 = time_string
            else:
                date2 = get_datetime('date2')
            call_proc("show_customer_transactions", [date1,date2])
        if user_input == '4':
            print("OVERDUE ACCOUNTS PAYABLE")
            push_select_query("acc_payable_id, amount_paid, amount_pending, pay_due_date FROM accounts_payable WHERE NOW() > pay_due_date AND amount_pending > 0")

            


#Main menu display string
def display_main_menu():
    print("\n\n\n\nWelcome to your inventory management solution\n") 
    print("Please select an option from the menu\n")
    print("1 Manage inventory\n")
    print("2 Make a business purchase\n")
    print("3 Make a payment on accounts payable\n")
    print("4 Select Table to be displayed \n")
    print("5 Enter Information directly into Database \n")
    print("6 Special Functions \n")
   

def main_loop():
    t = time.localtime()  
    time_string = time.strftime("%Y-%m-%d %H:%M:%S", t)
    print(time_string + "\n")
    
    while True:
        display_main_menu()
        user_input = input("\n\n\n\n Select an option: ")
        if user_input == '1':
            manage_inventory()
        if user_input == '2':
            make_a_purchase()
        if user_input == '3':
            make_a_payment()
        if user_input == '4':
            display_table_loop('20')
        if user_input == '5':
            insert_records()
        if user_input == '6':
            functions()





main_loop()













