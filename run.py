import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('love-sandwiches') 


def get_sales_data():
    """
    Get sales figures input from the user.
    """
    while True:

        print("Please enter sales data from the last market.")
        print("Data should be six numbers, separated by commas.")
        print("Example: 10,20,30,40,50,60\n")

        data_str = input("Enter your data here: ")

        sales_data = data_str.split(",")
        
        
        if validate_data(sales_data):
            print("Data is valid!")
            break

    return sales_data       

def validate_data(values):
    """
    inside try, convert all strings to interger,
    raise valueError if strings cannot be converted into integer, 
    or if there arent exactly 6 values.
    """
    try:
        [int(value) for value in values]
        if len(values) != 6:
           raise ValueError(
                f"Exactly 6 values required, you provided {len(values)}"
           )
    except ValueError as e: 
        print(f"invalid data: {e}, please try again.\n")
        return False

    return True

def update_sales_Worksheet(data):
    """
    update worksheet data, add new row in data data list provided.
    """
    print("updating sales Worksheet...\n")
    sales_worksheet = SHEET.worksheet("sales")
    sales_worksheet.append_row(data)
    print("sales_worksheet updated succesfully.\n")

def calculate_surplus_data(sales_row):
    """
    Compare sales with stock and calculate the surplus for each item type.

    The surplus is defined as the sales figure subtracted from the stock:
    - Positive surplus indicates waste
    - Negative surplus indicates extra made when stock was sold out.
    """
    print("Calculating surplus data...\n")
    stock = SHEET.worksheet("stock").get_all_values()
    stock_row = stock[-1]
    print(stock_row)

def main():
    """
    run all functions
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_sales_Worksheet(sales_data)
    calculate_surplus_data(sales_data)

print("welcome to lovesandwiches automation")
main()