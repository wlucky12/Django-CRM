#Install Mysql on my computer
#create virtual envirment .virt/ (python -m venv [virt name])
#pip install django
#pip install mysql
#pip install mysql-connector
#pip install mysql-connector-python
#use django-admin startproject [project name]
#it crate a manage.py, use it to startapp [appname]
#change sitting: installed app add 'website'
#configure database
import mysql.connector

dataBase = mysql.connector.connect(
    host = 'localhost',
    port = 3307,
    user = 'root',
    passwd = 'password'
)


#prepare a cursor object
cursorObject = dataBase.cursor()

#Create a Database
try:
    cursorObject.execute("CREATE DATABASE bankdb")
except mysql.connector.Error as err:  
 if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:  
    print("Something is wrong with your user name or password")  
 elif err.errno == errorcode.ER_BAD_DB_ERROR:  
    print("Database does not exist")  
 else:  
    print(err)
print("All done!")