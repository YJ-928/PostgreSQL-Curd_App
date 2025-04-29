# PostgreSQL-Curd_App
### A simple Python application that connects with postgreSQL and allows us to perform CURD operations on it

## The Curd App:

### i. Connects python to postgresql database using psycopg2 module

### ii. Used to perform Create,Read,Update,Delete (CURD) operation on the database

## @In-code execution/Steps:-

CONFIG = "dbname= user= password= host= port="

QUERY = "SQL written query, eg:- SELECT * FROM table_name;"

--> from psycopg2 import connect
--> Connection = connect(CONFIG)
--> Cursor = Connection.cursor()
--> Cursor.execute(QUERY)
--> Cursor.commit()
--> Cursor.close()
--> Connection.close()
