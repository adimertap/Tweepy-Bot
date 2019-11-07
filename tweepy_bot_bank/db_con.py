import pymysql

db=pymysql.connect("localhost","root","","db_tweepy_bank")
cursor_db =db.cursor()