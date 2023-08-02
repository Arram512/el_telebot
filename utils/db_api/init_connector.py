import mysql.connector

mydb = mysql.connector.connect(
  host="128.140.41.181",
  user="telebot",
  password="Night@Witches!#@",
  database="el_telebot"
)

mycursor = mydb.cursor()