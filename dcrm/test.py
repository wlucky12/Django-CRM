import mysql.connector
#pip uninstall mysql-connector, and pip install mysql-connector-python
connection = mysql.connector.connect(  
 host='localhost',  
 user='root',  
 passwd='Wenzc123'  
 )  
print("Connection established!")  
connection.close()  