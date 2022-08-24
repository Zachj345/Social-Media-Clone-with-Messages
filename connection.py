import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="*****",
    database="social"

)

cur = db.cursor()

# cur.execute('CREATE DATABASE social')

# cur.execute('DROP TABLE like')

cur.execute('SHOW TABLES')
for i in cur:
    print(i)
