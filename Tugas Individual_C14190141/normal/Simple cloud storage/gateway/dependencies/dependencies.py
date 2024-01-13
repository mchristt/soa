import uuid

import mysql.connector
from mysql.connector import Error
from mysql.connector import pooling

from nameko.extensions import DependencyProvider

class DatabaseWrapper:

    connection = None

    def __init__(self, connection):
        self.connection = connection

    def add_user(self, nrp,userAccount,email, userPassword):
        ## checking if user already exist or not
        
        cursor = self.connection.cursor(dictionary=True)
        result = []
        cursor.execute("""
        SELECT * FROM users 
        WHERE userName = %s;
        """, (userAccount,))
        for row in cursor.fetchall():
            result.append({
                'id': row['id'],
                'userAccount': row['userName']
            })

        if result:
            cursor.close()
            return "User Already Exist!"
        
        ## if user doesnt exist yet, create the account
        
        else:
            cursor = self.connection.cursor(dictionary=True)
            generateUUID = str(uuid.uuid4())
            print(generateUUID)
            cursor.execute("""
            INSERT INTO users (id,userNRP,userName, userEmail,userPassword)
            VALUES (%s, %s, %s,%s,%s);
            """, ( generateUUID,nrp,userAccount,email, userPassword))
            cursor.close()
            self.connection.commit()
            return "User Added Succcessfully!"
        
    def add_file(self, userAccount, file):
        # check if user already exist
        cursor = self.connection.cursor(dictionary=True)
       
        cursor.execute("""
        INSERT INTO files (userid,file)
        VALUES (%s, %s);
        """, ( userAccount,file))
        cursor.close()
        self.connection.commit()
        return "File uploaded successfully!"
    
    # get user for login
    def get_user(self, email, userPassword):
        cursor = self.connection.cursor(dictionary=True)
        result = []
        cursor.execute("""
        SELECT * FROM users 
        WHERE userEmail = %s AND userPassword = %s;
        """, (email, userPassword))
        for row in cursor.fetchall():
            result.append({
                'session_id':'',
                'id': row['id'],
                'email': row['userEmail']
            })
        cursor.close()
        return result

class Database(DependencyProvider):

    connection_pool = None

    def __init__(self):
        try:
            self.connection_pool = mysql.connector.pooling.MySQLConnectionPool(
                pool_name="database_pool",
                pool_size=5,
                pool_reset_session=True,
                host='localhost',
                database='storage',
                user='root',
                password=''
            )
        except Error as e :
            print ("Error while connecting to MySQL using Connection pool ", e)
    
    def get_dependency(self, worker_ctx):
        return DatabaseWrapper(self.connection_pool.get_connection())