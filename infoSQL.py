import mysql.connector
from mysql.connector import Error

def showPlayerInfo(playername):
  

try:
  con = mysql.connector.connect(
    host = "192.168.56.101",
    port = 4567,
    user = "yhkyu",
    password = "1234",
    database = "maple"
  )
  
  if con.is_connected():
    cursor = con.cursor()
  
except Error as e:
  print(f'연결 에러 : {e}')

con.close()
cursor.close()

print("ddddddd")