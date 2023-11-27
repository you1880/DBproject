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
    query2 = "SELECT * FROM Equipment WHERE player_name=" + "\"" + playername + "\""
    cursor.execute(query)
    
    result = cursor.fetchall()
    
    insert_query = None
    values = None
    insert_equip_queries = None
    equip_values = None
    
    if not result:
      insert_query, values, insert_equip_queries, equip_values = updateInitialInfo(playername)
      if not insert_query:
        return -1
    else:
      days_diff = (datetime.now().date() - result[0][-1]).days   
      
      if days_diff > 1:
        insert_query, values, insert_equip_queries, equip_values = updateInfo(playername)
        if not insert_query:
          return -1
        
    if insert_query: 
      cursor.execute(insert_query, values)
      con.commit()

      for q, v in zip(insert_equip_queries, equip_values):
        cursor.execute(q, v)
        con.commit()
    
    cursor.execute(query)
    result = cursor.fetchall()
    
    cursor.execute(query2)
    result2 = cursor.fetchall()
    
    cursor.close()
    con.close()
    
    return result, result2
  
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
  values = [player_stat['닉네임'], player_stat['레벨'], player_stat['직업'], player_stat['이미지'],
            player_stat['스탯 공격력'], stat_list['STR'], stat_list['DEX'], stat_list['INT'], stat_list['LUK'],
            str(stat_list['Critical Damage']), str(stat_list['Boss Damage']), 
            str(stat_list['Ignore Defense']), update_date]
  
  equip_stat = player_data['장비 정보']
  equip_query_list=[]
  equip_value_list=[]
  
  for equip in equip_stat:
    equiplist = equip['스탯 리스트']
    equip_query = "INSERT INTO Equipment VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    
    temp_list = []
    equip_keys = ['장비 착용자', '아이템 이름', '분류', '등급', '아이템 이미지', '스타포스', '놀장강']
    equiplist_keys = ['공격속도' , 'STR', 'DEX', 'INT', 'LUK', 'MaxHP', 'MaxMP', '공격력', '마력',
                      '물리방어력', '이동속도', '점프력', '보스 몬스터공격 시', '몬스터 방어력 무시',
                      '올스탯', '착용 레벨 감소', '업그레이드 가능 횟수', '가위 사용 가능 횟수', '잠재옵션',
                      '에디셔널 잠재옵션', '소울옵션', '기타']
    
    for key in equip_keys:
      if key in equip:
        temp_list.append(equip[key])
      else:
        temp_list.append(None)
    
    for key in equiplist_keys:
      if key in equiplist:
        temp_list.append(equiplist[key])
      else:
        temp_list.append(None)

    equip_query_list.append(equip_query)
    equip_value_list.append(temp_list)

  return query, values, equip_query_list, equip_value_list

def updateInfo(playername):
  player_data = playerinfo.getPlayerPage(playername)
  
  if player_data == -1:
    return [0, 0]
  
  update_date = datetime.now().strftime("%Y-%m-%d")
  
  player_stat = player_data['스탯 정보']
  stat_list = player_stat['스탯 리스트']
  query = "UPDATE User SET player_lv=%s, player_job=%s, player_img=%s, player_attk=%s, player_str=%s, player_dex=%s, player_int=%s, player_luk=%s, player_crt_dmg=%s, player_bos_dmg=%s, player_ing_def=%s, update_date=%s WHERE player_name=%s"
  values = [player_stat['레벨'], player_stat['직업'], player_stat['이미지'], player_stat['스탯 공격력'], stat_list['STR'], stat_list['DEX'], stat_list['INT'], stat_list['LUK'], 
            str(stat_list['Critical Damage']), str(stat_list['Boss Damage']), str(stat_list['Ignore Defense']), update_date, player_stat['닉네임']]
  
  equip_stat = player_data['장비 정보']
  equip_query_list=[]
  equip_value_list=[]
  
  for equip in equip_stat:
    equiplist = equip['스탯 리스트']
    equip_query = "UPDATE Equipment SET equip_name=%s, equip_grade=%s, equip_image=%s, starforce=%s, is_aee=%s, wp_spd=%s, eq_str=%s, eq_dex=%s, eq_int=%s, eq_luk=%s, eq_hp=%s, eq_mp=%s, eq_att=%s, eq_ma=%s, eq_def=%s, eq_spd=%s, eq_jmp=%s, eq_bos_dmg=%s, eq_ing_def=%s, eq_all_stt=%s, eq_red_lv=%s, eq_upg_cnt=%s, eq_can_exch=%s, eq_ability=%s, eq_add_ability=%s, wp_soul=%s, eq_etc=%s WHERE equip_class=%s"
    
    equip_keys = ['아이템 이름', '등급', '아이템 이미지', '스타포스', '놀장강']
    equiplist_keys = ['공격속도' , 'STR', 'DEX', 'INT', 'LUK', 'MaxHP', 'MaxMP', '공격력', '마력',
                      '물리방어력', '이동속도', '점프력', '보스 몬스터공격 시', '몬스터 방어력 무시',
                      '올스탯', '착용 레벨 감소', '업그레이드 가능 횟수', '가위 사용 가능 횟수', '잠재옵션',
                      '에디셔널 잠재옵션', '소울옵션', '기타']
    temp_list = []
    
    for key in equip_keys:
      if key in equip:
        temp_list.append(equip[key])
      else:
        temp_list.append(None)
    
    for key in equiplist_keys:
      if key in equiplist:
        temp_list.append(equiplist[key])
      else:
        temp_list.append(None)
        
    temp_list.append(equip['분류'])

    equip_query_list.append(equip_query)
    equip_value_list.append(temp_list)

  return query, values, equip_query_list, equip_value_list