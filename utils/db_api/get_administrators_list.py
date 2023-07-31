import mysql.connector

mydb = mysql.connector.connect(
  host="127.0.0.1",
  user="root",
  password="Night@Witches!#@",
  database="el_telebot"
)

mycursor = mydb.cursor()

mycursor.execute("SELECT telegram_id FROM users WHERE is_admin = true")

myresult = mycursor.fetchall()

for x in myresult:
  print(x)