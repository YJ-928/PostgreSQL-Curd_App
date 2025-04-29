# ------------------------------ Code Start ------------------------------
from psycopg2 import connect
from time import sleep

# Constant config string with all the database information
CONFIG = "dbname=curdappdb user=postgres password=928187 host=localhost port=5432"

# ------------------------------ Class PostgreSQL ------------------------------
try:
    class PostgreSQL():
        '''Class to make a connection, create cursor, execute queries, 
        commit changes, fetch response/records,
        close cursor and close connection'''

        # Class variables
        Connection = connect(CONFIG) # Making connection
        Cursor = Connection.cursor() # Creating cursor

        # ------------------------------ Make Connection Function ------------------------------
        def MakeConnection(self):
            '''Function to display at start of the curd application'''
            print('----- Welcome to "The Curd Application" ------')
            print('Connecting to database...')
            sleep(1)
            print('Database connected, creating cursor...')
            sleep(1)
            print('Cursor created, ready to execute queries')
    
        # ------------------------------ Cursor Execute Function ------------------------------
        def CursorExecute(self,Query):
            '''Function to execute queries using cursor'''
            #print(f'\nCursor executing the given query...')
            #sleep(1)
            PostgreSQL.Cursor.execute(Query)
            #print('Cursor execution finished')
    
        # ------------------------------ Cursor Fetchall Function ------------------------------
        def CursorFetchall(self):
            '''Function to fetch all the records/responses from database'''
            #print('\nCursor fetching records...')
            #sleep(1)
            Records = PostgreSQL.Cursor.fetchall()
            #print('Records fetched')
            return Records

        # ------------------------------ Commit Changes Function ------------------------------
        def CommitChanges(self):
            '''Function to commit the changes to database to save them'''
            #print('\nCommiting the changes to database...')
            sleep(1)
            PostgreSQL.Connection.commit() # Commit changes
            #print('Changes commited')
        
        # ------------------------------ Cursor Close Function ------------------------------
        def CursorClose(self):
            '''Function to close the cursor after query execution'''
            print('\nClosing the cursor...')
            sleep(1)
            PostgreSQL.Cursor.close()
            print('Cursor closed')

        # ------------------------------ Close Connection Function ------------------------------ 
        def CloseConnection(self):
            '''Function to close connection to the database'''
            print('\nDisconnecting from the Database...')
            sleep(1)
            PostgreSQL.Connection.close()
            print('----- Thank you for using "The Curd Application" -----')

except Exception as E:
    print(f'\n{E}\nException occured in PostgreSQL class..')

# Create Databse object
Database = PostgreSQL()

# ------------------------------ Code End ------------------------------