import mysql.connector

mydb = mysql.connector.connect(
  host="10.8.0.1",
  user="telebot",
  password="Night@Witches!#@",
  database="el_telebot"
)

mycursor = mydb.cursor()