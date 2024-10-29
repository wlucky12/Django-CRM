import mysql.connector
connection = mysql.connector.connect(  
 host='localhost',  
 user='root',  
 passwd='Wenzc123'  
 )  
print("Connection established!")  
connection.close()  