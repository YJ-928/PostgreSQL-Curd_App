# ------------------------------ Code Start ------------------------------
from postgresql import Database
from curdapp import CurdApp
from time import sleep
import os

# ------------------------------ Fetch Tables Function ------------------------------
def FetchTables():
    '''Function to fetch all the tables from the connected database'''
    # SQL query to fetch all tables
    QUERY = "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';"
    Database.CursorExecute(QUERY)
    TableList = []
    Records = Database.CursorFetchall() # List of tuples
    for Tablenum in range(len(Records)):
        TableList.append((Tablenum+1,Records[Tablenum][0])) # To extract only table from [(table1,),(table2,)..]
    TableDict = dict(TableList)
    return TableDict

# ------------------------------ Show Tables Function ------------------------------
def ShowTables():
    '''Function to display tables, input user's choice and validate it'''
    Tables = FetchTables()
    print('\n----- Tables in Server ------')
    for key,table in Tables.items(): # Display them in a proper choice list format
        print(f'{key}: {table}')
    try:
        Table = int(input("Please choose a table: ")) # Take user's input
    except Exception as E:
        print(f'Invalid input: {Table} for table, enter valid inputs !!')
        ShowTables()
    if Table not in Tables.keys(): # Validate user's choice
        print('Invalid choice, please choose again...')
        ShowTables()
    else:
        print(f'You choose the "{Tables[Table]}" table') # Print user's choice
        return Tables[Table] # Return the respective table name as per user's choice

# ------------------------------ Curd Operation Function ------------------------------
def CurdOperations():
    '''Function to display the curd operations, input user's choice and validate it'''
    print('\n----- The Curd Operations -----')
    # The curd operations dictionary
    CurdOpDict = {
        1:'Create Record',
        2:'Update Record',
        3:'Retrieve Record',
        4:'Delete Record',
        5:'Change Table',
        6:'Exit'}
    for key,operation in CurdOpDict.items(): # Displaying them in proper choice list format
        print(f'{key}: {operation}')
    try:
        Operation = int(input('Please choose a operation to perform on selected table: ')) # Taking user's input
    except Exception as E:
        print(f'Invalid input: {Operation} for operation, enter valid inputs !!')
        CurdOperations()
    if Operation not in CurdOpDict.keys(): # Validate user's choice
        print('Invalid choice, please choose again...')
        CurdOperations()
    else:
        print(f'You choose "{CurdOpDict[Operation]}" operation') # Print user's choice
        return Operation # Return choice number as operation
    
# ------------------------------ Switcher Function ------------------------------
def Switcher(Operation):
    '''Function to call and switch to various functions based on operation'''
    global App # To make it accessible inside the function
    if Operation == 1:
        App.CreateRecord()
        return
    
    if Operation == 2:
        App.UpdateRecord()
        return
    
    if Operation == 3:
        App.RetrieveRecord()
        return

    if Operation == 4:
        App.DeleteRecord()
        return

    if Operation == 5:
        App = CurdApp(ShowTables())
        App.FetchColumnDatatype()
        return
        
# ------------------------------ Main Function ------------------------------
if __name__ == "__main__":
    os.system('cls') # To clear the terminal screen
    sleep(1)
    Database.MakeConnection()
    App = CurdApp(ShowTables()) # To return the choosen table name to curdapp
    App.FetchColumnDatatype()
    while True: # Loop to make it run until exit
        try:
            sleep(1)
            Operation = CurdOperations() # Displaying operations and taking user's input
            if Operation == 6:
                Database.CursorClose()
                sleep(1)
                Database.CloseConnection()
                break
            else:
                Switcher(Operation)
        except Exception as E:
            print(f'\n{E}\nException occured in the main function..')

# ------------------------------ Code End ------------------------------