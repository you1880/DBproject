from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as bs
from bs4 import BeautifulSoup as bs
from urllib.parse import quote
import requests
import re
import time

#getPlayerURL(nickname)
#---mapleRank_URL + enc_nick을 통해 request를 보내고, 가져온 정보를 bs로 변환, player_URL을 만들어냄

#getPlayerPage(player_URL)
#---player_URL을 bs로 변환하고, 이를 통해 정보가 비공개인지 아닌지를 탐색
#---비공개면 종료하고, 공개라면 getPlayerStats(soup)를 통해 player의 기본 stats을 가져옴
#---플레이어의 Equipment URL을 찾아 이를 bs로 변환하고 gePlayerEquipment(soup)를 통해 장비리스트를 가져옴

#getPlayerStats(soup)
#--- details에서 char_info에 있는 플레이어의 기본 스텟들을 파싱해서 가져옴

#getPlayerEquipment(soup)
#---플레이어가 착용한 장비의 이름, 별수, 스텟, 공격력, 잠재능력, 에디를 딕셔너리형태로 가져옴
#---장비 딕셔너리는 [name, starforce, str, dex, int, luk, att, matt, ability_grade, ability, add_ability_grade, add_ability, img_url]
#--ability = [1줄, 2줄, 3줄], add_ability = [1줄, 2줄, 3줄]
#--[Equip1, Equip2, Equip3...]형태가 될것

maple_URL = "https://maplestory.nexon.com"

#랭킹에서 플레이어 정보를 가져오는 과정
def getPlayerURL(nickname):
  #닉네임 변환 후 랭크페이지 URL과 합침
  encoded_nick = quote(nickname)
  mapleRank_URL = "https://maplestory.nexon.com/N23Ranking/World/Total?c="
  
  response = requests.get(mapleRank_URL + encoded_nick)
  
  if response.status_code != 200:
    print("웹에서 정보를 불러오는데 실패하였음 : " + response.status_code)
    return
  
  playerURL_soup = bs(response.text, "html.parser")
  #플레이어 페이지의 주소를 가져오는 과정
  try:
    find_player_page_URL = playerURL_soup.find(class_="search_com_chk").find_all("td")[1].find("a")
  except AttributeError as e:
    print("해당 플레이어를 찾을 수 없음")
    return
  
  player_page_URL = maple_URL + find_player_page_URL['href']
    
  return player_page_URL

def getPlayerPage(playername):
  nickname = playername
  player_page_URL = getPlayerURL(nickname)
  
  if not player_page_URL:
    return -1
  
  response = requests.get(player_page_URL)
  #웹 페이지 응답 없을시 종료
  if response.status_code != 200:
    print("웹에서 정보를 불러오는데 실패하였음 : " + response.status_code)
    return
  
  player_page_soup = bs(response.text, "html.parser")
  #정보 비공개일시 처리
  if player_page_soup.find(class_="private2"):
    print("해당 플레이어는 정보를 공개하지 않습니다")
    return -1
  
  player_stats = getPlayerStats(player_page_soup, nickname)
  #print(player_stats)
  
  find_equip = player_page_soup.find(class_="lnb_list").find('a', string="장비")
  equip_URL = maple_URL + find_equip['href']

  player_equip_list = getPlayerEquipment(equip_URL, nickname)

  return {"스탯 정보" : player_stats, "장비 정보" : player_equip_list}
  #print(player_equip_list)

#플레이어의 기본 스텟을 불러오는 함수
def getPlayerStats(player_page_soup, nickname): 
  #html태그 내 char_info부분을 가져오는 과정
  find_basic_info = player_page_soup.find(class_="char_info")
  basic_info_list = find_basic_info.find_all("dd")
  
  #player의 LV을 가져옴
  char_LV = basic_info_list[0].string
  char_LV = re.sub(r"LV.", "", char_LV)
  
  #player의 직업을 가져옴
  char_job = basic_info_list[1].string
  char_job = re.sub(r"^(.*?)\/", "", char_job)
  
  #player의 캐릭터 이미지를 가져옴
  char_img = player_page_soup.find(class_="char_img").find("img")['src']
  
  #player의 stat부분을 가져오는 과정
  find_stats_info = player_page_soup.select_one("#container > div.con_wrap > div.contents_wrap > div > div.tab01_con_wrap > table:nth-child(4) > tbody")
  stats_info_list = find_stats_info.find_all("td")
  
  #player 스공을 가져옴(최소스공 ~ 최대스공)
  char_DMG = stats_info_list[0].string.replace(',', '')
  
  #player의 힘
  char_STR = stats_info_list[3].string.replace(',', '')
  
  #player의 덱스
  char_DEX = stats_info_list[4].string.replace(',', '')
  
  #player의 인트
  char_INT = stats_info_list[5].string.replace(',', '')
  
  #player의 럭
  char_LUK = stats_info_list[6].string.replace(',', '')
  
  #player의 크뎀
  char_CRITICAL_DMG = stats_info_list[7].string
  
  #player의 보공
  char_BOSS_DMG = stats_info_list[8].string
  
  #player의 방무
  char_IGN_DEF = stats_info_list[9].string
  
  char_stat_dic = {"STR": char_STR, "DEX" : char_DEX, "INT" : char_INT, "LUK" : char_LUK,
                  "Critical Damage" : char_CRITICAL_DMG, "Boss Damage" : char_BOSS_DMG, "Ignore Defense" : char_IGN_DEF}
  
  #player 정보를 반환
  return {"닉네임" : nickname, "레벨" : char_LV, "직업" : char_job, "이미지" : char_img, "스탯 공격력" : char_DMG, "스탯 리스트" : char_stat_dic}

def getItemInfo(info_attr, nickname):
  info_soup = bs(info_attr, 'html.parser')
  
  #장비 이름 추출
  title_lines = [line for line in info_soup.find(class_="item_memo_title").get_text().splitlines() if line.strip()]
  
  if len(title_lines) == 3:
    equip_title = title_lines[0].strip() + ' ' + title_lines[1].strip()
    equip_starforce = title_lines[2].strip().replace('성 강화', '')
  else:
    equip_title = title_lines[0].strip()
    
  #스타포스 강화 가능한 장비여부 판단
  if len(title_lines) == 2:
    equip_starforce = title_lines[1].strip().replace('성 강화', '')
  elif len(title_lines) == 1:
    equip_starforce = ''
  
  #아이템 이미지 추출
  equip_img = info_soup.find(class_='item_img').find('img')['src']
  
  #장비 분류 추출
  equip_class = info_soup.find_all(class_="job_name")
  equip_class = equip_class[1].get_text().replace('장비분류 | ', '')
  
  #장비 잠재능력 등급 추출
  equip_grade = info_soup.find(class_="item_memo_sel")
  if equip_grade is not None:
    equip_grade = info_soup.find(class_="item_memo_sel").get_text().replace('아이템', '')
  else:
    equip_grade = 'None'
  
  
  #장비 스텟 리스트 추출(힘, 덱, 럭, 인, 공, 마, 잠재능력, 에디셔널 잠재능력)
  equip_info_list = info_soup.find(class_="stet_info").find_all("li")
  equip_info_dic = {}
  
  for info in equip_info_list:
    stet_name = info.find(class_="stet_th").get_text(strip=True)
    point_name = info.find(class_="point_td").get_text(separator='$')
    equip_info_dic[stet_name] = point_name
  
  #딕셔너리 내의 문자열을 다듬는 과정
  for key, value in equip_info_dic.items():
    if '잠재옵션' in key or '기타' in key:
      equip_info_dic[key] = value.replace('$', '\n')
    else:
      equip_info_dic[key] = value.replace('$', '')

  #기타에서 놀장강 사용템인지 아닌지 판단
  if "놀라운 장비강화 주문서" in equip_info_list[-1]:
    AEE = True
  else:
    AEE = False
  
  return {"장비 착용자" : nickname, "아이템 이름" : equip_title, "분류" : equip_class, "등급" : equip_grade, "아이템 이미지" : equip_img, "스타포스" : equip_starforce, "놀장강" : AEE, "스탯 리스트" : equip_info_dic}
  

def getPlayerEquipment(equip_url, nickname):
  option = Options()
  #option.add_argument('--headless')
  driver = webdriver.Chrome(options=option)
  driver.get(equip_url)
  
  #아이템 팟 장비 정보를 순서대로 보관할 장비 리스트
  player_equip_list = []
  #list = [1, 3, 5, 6, 7, 8, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 28, 29, 30]
  list = [3]
  
  for i in list:
    item_pot_link = driver.find_element(By.XPATH, '/html/body/div[3]/div[2]/div[2]/div[2]/div[2]/div/div[2]/div[1]/ul/li[' + str(i) + ']')
    item_pot_link.click()
    wait = WebDriverWait(driver, 10)
    item_info = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div[2]/div[2]/div[2]/div[2]/div/div[2]/div[2]/div')))
    iteminfo_html = item_info.get_attribute('outerHTML')
    player_equip_list.append(getItemInfo(iteminfo_html, nickname))
    time.sleep(5)
    
  return player_equip_list