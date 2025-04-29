# ------------------------------ Code Start ------------------------------
from postgresql import Database
from time import sleep

# ------------------------------ Curd App Class ------------------------------
try:
    class CurdApp():
        '''Class to create curd sql queries and return them to cursor for execution'''
    
        # ------------------------------ Class Constructor with Tablename ------------------------------
        def __init__(self,tablename):
            self.tablename = tablename

        # ------------------------------ Fetch Column Datatype Function ------------------------------
        def FetchColumnDatatype(self):
            '''Function to fetch all the columns and datatypes from the given table'''
            # SQL query to fetch all the column_names,data_types from a given table
            QUERY = f"SELECT COLUMN_NAME,DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = N'{self.tablename}';"
            Database.CursorExecute(QUERY)
            ColDataTupList = Database.CursorFetchall() # Fetching list of tuples [(col1,dtype1),(col2,dtype2)..]
            # Declaring as self, to access throughout class
            self.ColumnDatatype = dict(ColDataTupList) # Dict of format {Column:Datatype}
            self.ColumnList = [col[0] for col in ColDataTupList] # List of column_names
            self.DatatypeList = [col[1] for col in ColDataTupList] # List of datatypes
            self.cols = ','.join(self.ColumnList) # String of column_names for insert into operation
        
        # ------------------------------ Match Input Function ------------------------------
        def MatchInput(self,key):
            '''Function to take correct input by mapping input with column datatype'''
            try: # Here key is column name which is mapped to its value in ColumnDatatype dict
                if self.ColumnDatatype[key].lower() == 'integer':
                    return int(input(f'Enter a [integer/int] value for "{key}": '))
                elif self.ColumnDatatype[key].lower() == 'numeric':
                    return float(input(f'Enter a [decimal/float] value for "{key}": '))
                else:
                    return str(input(f'Enter a [text/string] value for "{key}": '))
            except Exception as E:
                print('Enter valid inputs with respect to the column datatypes !!!')
                self.MatchInput(key) # To return to same input if invalid input is given

        # ------------------------------ Confirm Function ------------------------------
        def Confirm(self):
            '''Function to confirm any given query or input using a boolean flag'''
            Flag = True # Flag initialised
            try: # Taking user input
                Confirm = input('yes or no: ').lower()
                if Confirm not in ('yes','no','y','n'): # Validating and raising exception
                    raise ValueError(f'Invalid Input:{Confirm}. Please enter "Yes" or "No" only!!')
            except ValueError as E:
                print(E)
                self.Confirm()
            if Confirm == "no" or Confirm == "n":
                Flag = False # If user says no
                return Flag
            else:
                return Flag # If user says yes
        
        # ------------------------------ Execute and Commit Function ------------------------------
        def ExecuteAndCommit(self,QUERY):
            '''Function to call the cursor and feed it query for execution'''
            Database.CursorExecute(QUERY) # Executing query
            Database.CommitChanges() # Commiting changes

        # ------------------------------ Print Records Function ------------------------------
        def PrintRecords(self):
            '''Function to print the retrieved/fetched records in proper format'''
            Records = Database.CursorFetchall()
            print(f'\nPrinting {len(Records)} Fetched Records...')
            for key in range(len(Records)):
                print(f'{key+1} : {Records[key]}') # Printing them as key:value pair

        # ------------------------------ Create Record Function Start ------------------------------
        def CreateRecord(self):
            '''Function to create sql query for create record operation'''
            print('\n--------- Create Record Operation Started ---------')
            N = int(input('Enter the number of records you want to create: ')) # Number of records to be created
            sleep(1)
            query = "" # Values query containing tuples
            i = 1
            while i != N+1:
                print(f'\n-- Enter values for record no.{i} --')
                temp = []
                for key in self.ColumnDatatype.keys():
                    Input = self.MatchInput(key) # Send column name as key to function
                    temp.append(Input)
                if i == N:
                    query += str(tuple(temp)) # For last value tuple to avoid 'comma' at end
                    break
                else:
                    query += str(tuple(temp)) + "," # For all other value tuples with 'comma' at end
                i += 1
            # Final sql query for the create record operation
            QUERY = f'INSERT INTO {self.tablename}({self.cols}) VALUES {query};'
            print(f'QUERY:\n{QUERY}\n')
            if self.Confirm(): # Calling function to confirm created query
                self.ExecuteAndCommit(QUERY)
            else:
                self.CreateRecord() # Re-creating query if user declines
            sleep(1)
            print(f'\nRecords created in "{self.tablename}" table\n--------- Create Record Operation Finished ---------')
        
        # ------------------------------ Create Record Function End ------------------------------

        # ------------------------------ Update Record Function Start ------------------------------
        def UpdateRecord(self):
            '''Function to create sql query for update record operation'''
            print('\n--------- Update Record Operation Started ---------')
            # SQL query to fetch all the records available in the table
            QUERY = f"SELECT * FROM {self.tablename};"
            print(f'\nFetching all records available in {self.tablename} table...')
            Database.CursorExecute(QUERY)
            self.PrintRecords() # Displaying the records
            print(f'\nRecords in {self.tablename} have following columns with datatypes\n{self.ColumnDatatype}\n')

            # Creating set_query - SET column = new_value
            set_query = ""
            Coltemp = []
            for columns in range(len(self.ColumnList)): # Displaying columns
                print(f'{columns}: {self.ColumnList[columns]}')
                Coltemp.append(columns)
            while True:
                NumCol = int(input('Please choose a column which will be updated with a new value: ')) # Taking user input
                if NumCol not in Coltemp: # Validating it
                    print('Invalid choice, please choose again..')
                else:
                    break
            print(f'\nEnter the new value for "{self.ColumnList[NumCol]}" column:') # New value for the selected column
            NewVal = self.MatchInput(self.ColumnList[NumCol])
            if type(NewVal) == type("String"):
                set_query = f"{self.ColumnList[NumCol]} = '{NewVal}'" # To convert to string format in the query
            else:
                set_query = f"{self.ColumnList[NumCol]} = {NewVal}"
            
            # Creating where_query - WHERE column = value
            where_query = ""
            print(f'\nPlease choose a column where the record will be updated with the new value:')
            Coltemp = []
            for columns in range(len(self.ColumnList)): # Displaying columns
                print(f'{columns}: {self.ColumnList[columns]}')
            Coltemp.append(columns)
            while True:
                NumCol = int(input('Please choose a column: ')) # Taking column input
                if NumCol not in Coltemp: # Validating it
                    print('Invalid choice, please choose again..')
                else:
                    break
            # SQL query to fetch selected column values
            QUERY = f'SELECT {self.ColumnList[NumCol]} FROM {self.tablename};'
            self.ExecuteAndCommit(QUERY)
            TupList = Database.CursorFetchall()
            Records = []
            for record in TupList: # Converting to a list of all records
                Records.append(record[0])
            Rowtemp = []
            for rows in range(len(Records)): # Displaying records
                print(f'{rows}: {Records[rows]}')
                Rowtemp.append(rows)
            while True:
                RowNum = int(input(f'Please choose a row value: ')) # Taking row input
                if RowNum not in Rowtemp: # Validating it
                    print(f'Invalid choice, please choose again..')
                else:
                    break
            OldVal = Records[RowNum]
            if type(OldVal) == type("String"):
                where_query = f"{self.ColumnList[NumCol]} = '{OldVal}'" # To convert to string format in query
            else:
                where_query = f"{self.ColumnList[NumCol]} = {OldVal}"
            
            # Final sql query for the update record operation
            QUERY = f"UPDATE {self.tablename} SET {set_query} WHERE {where_query};"
            print(f'\nDo you confirm Query:\n{QUERY}\n')
            if self.Confirm(): # Confirming and executing the query
                self.ExecuteAndCommit(QUERY)
            else:
                self.UpdateRecord()
            sleep(1)
            print(f'\nRecords updated in "{self.tablename}" table\n--------- Update Record Operation Finished ---------')

        # ------------------------------ Update Record Function End ------------------------------

        # ------------------------------ Retrieve Record Function Start ------------------------------
        def RetrieveRecord(self):
            '''Function to create sql query for retrieve record operation'''
            print('\n--------- Retrieve Record Operation Started ---------')
            query = ""
            print(f'\nRetrieve all records from "{self.tablename}"?')
            if self.Confirm():
                query += "*"
            else:
                print(f'\nThe "{self.tablename}" table has "{len(self.ColumnList)}" columns.\nPlease select the columns to fetch records from')
                for col in self.ColumnList:
                    print(f'\nDo you want to fetch records from "{col}" column?')
                    if self.Confirm():
                        query += f'{col},'
                query = query[:len(query)-1] # Removing that last extra 'comma'
            # Final sql query for retrieve record operation
            QUERY = f'SELECT {query} FROM {self.tablename};'
            print(f'\nDo you confirm the QUERY:\n{QUERY}')
            if self.Confirm():
                self.ExecuteAndCommit(QUERY)
                self.PrintRecords()
            else:
                self.RetrieveRecord()
            sleep(1)
            print(f'\nRecords retrieved from "{self.tablename}" table\n--------- Retrieve Record Operation Finished ---------')

        # ------------------------------ Retrieve Record Function End ------------------------------

        # ------------------------------ Delete Record Function Start ------------------------------
        def DeleteRecord(self):
            '''Function to one or some records from a given table'''
            print('\n--------- Delete Record Operation Started ---------')
            print(f'\nDelete all records from "{self.tablename}"?')
            if self.Confirm():
                self.ExecuteAndCommit(f'DELETE FROM {self.tablename};')
            else:
                print(f'\nThe "{self.tablename}" table has "{len(self.ColumnList)}" columns:')
                del_query = ""
                tempCol = []
                for columns in range(len(self.ColumnList)):
                    print(f'{columns}: {self.ColumnList[columns]}')
                    tempCol.append(columns)
                while True:
                    ColNum = int(input('Please choose a column using which records will be deleted: '))
                    if ColNum not in tempCol:
                        print('Invalid choice, please choose again..')
                    else:
                        break
                # SQL query to fetch selected column records from the table
                QUERY = f'SELECT {self.ColumnList[ColNum]} FROM {self.tablename};'
                self.ExecuteAndCommit(QUERY)
                Records = Database.CursorFetchall()
                print(f'\nYou choose to delete "{self.ColumnList[ColNum]}" column.\nIt has {len(Records)} values:')
                tempRow = []
                for rows in range(len(Records)):
                    print(f'{rows}: {Records[rows][0]}')
                    tempRow.append(rows)
                while True:
                    RowNum = int(input('Please choose a value to delete that whole corresponding row: '))
                    if RowNum not in tempRow:
                        print(f'Invalid choice, please choose again..')
                    else:
                        break
                DelVal = Records[RowNum][0]
                if type(DelVal) == type("String"):
                    del_query = f"{self.ColumnList[ColNum]} = '{DelVal}'" # To convert to string format in query
                else:
                    del_query = f"{self.ColumnList[ColNum]} = {DelVal}"
                # Final sql query for the delete record operation
                QUERY = f'DELETE FROM {self.tablename} WHERE {del_query};'
                print(f'\nDo you confirm the Query:\n{QUERY}')
                if self.Confirm():
                    self.ExecuteAndCommit(QUERY)
                else:
                    self.DeleteRecord()
                sleep(1)
            print(f'\nRecords deleted in "{self.tablename}" table\n--------- Delete Record Operation Finished ---------')

        # ------------------------------ Delete Record Function End ------------------------------

except Exception as E:
    print(f'\n{E}\nException occured in the CurdApp class..')

# ------------------------------ Code End ------------------------------