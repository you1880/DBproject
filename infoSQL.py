import mysql.connector
from mysql.connector import Error
from datetime import datetime
import playerinfo
import time

def showPlayerInfo(playername):
  try:
    con = mysql.connector.connect(
      host = "192.168.56.101",
      port = 4567,
      user = "yhkyu",
      password = "1234",
      database = "maple"
    )
    
    cursor = con.cursor()
    
    query = "SELECT * FROM User WHERE player_name=" + "\"" + playername + "\""
    cursor.execute(query)
    
    result = cursor.fetchall()
    
    insert_query = None
    values = None
    
    if not result:
      insert_query, values = updateInitialInfo(playername)
      if not insert_query:
        return -1
    else:
      days_diff = (datetime.now().date() - result[0][-1]).days   
      
      if days_diff > 1:
        insert_query, values = updateInfo(playername)
        if not insert_query:
          return -1
      
    cursor.execute(insert_query, values)
    con.commit()
      
    cursor.execute(query)
    result = cursor.fetchall()
      
    cursor.close()
    con.close()
    
    return result
  
  except Error as e:
    print(f'연결 에러 : {e}')
    return

def updateInitialInfo(playername):
  player_data = playerinfo.getPlayerPage(playername)
  
  if player_data == -1:
    return [0, 0]
  
  update_date = datetime.now().strftime("%Y-%m-%d")

  player_stat = player_data['스탯 정보']
  stat_list = player_stat['스탯 리스트']
  query = "INSERT INTO User VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
  values = (player_stat['닉네임'], player_stat['레벨'], player_stat['직업'], player_stat['이미지'],
            player_stat['스탯 공격력'], stat_list['STR'], stat_list['DEX'], stat_list['INT'], stat_list['LUK'],
            str(stat_list['Critical Damage']), str(stat_list['Boss Damage']), 
            str(stat_list['Ignore Defense']), update_date)

  return query, values

def updateInfo(playername):
  player_data = playerinfo.getPlayerPage(playername)
  
  if player_data == -1:
    return [0, 0]
  
  update_date = datetime.now().strftime("%Y-%m-%d")
  
  player_stat = player_data['스탯 정보']
  stat_list = player_stat['스탯 리스트']
  query = "UPDATE User SET player_lv=%s, player_job=%s, player_img=%s, player_attk=%s, player_str=%s, player_dex=%s, player_int=%s, player_luk=%s, player_crt_dmg=%s, player_bos_dmg=%s, player_ing_def=%s, update_date=%s WHERE player_name=%s"
  values = (player_stat['레벨'], player_stat['직업'], player_stat['이미지'], player_stat['스탯 공격력'], stat_list['STR'], stat_list['DEX'], stat_list['INT'], stat_list['LUK'], 
            str(stat_list['Critical Damage']), str(stat_list['Boss Damage']), str(stat_list['Ignore Defense']), update_date, player_stat['닉네임'])
  
  return query, values