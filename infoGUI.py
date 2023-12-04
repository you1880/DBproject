from tkinter import *
from PIL import Image, ImageTk
from io import BytesIO
import requests
import infoSQL

error_msg = ""
equip_info = None
eq_info_label_list = []

#검색할 유저 이름 입력후 버튼 클릭 or 엔터 입력시 해당 플레이어 정보를 불러오는 함수
def updateInfoButton():
  player_name = input_entry.get()
  
  #아무것도 입력하지 않으면 버튼 클릭 or 엔터 입력 무시
  if not len(player_name):
    return

  playername_label.config(text=f"닉네임 : {player_name}")
  input_entry.delete(0, END)
  
  try:  
    input_button.config(state="disabled")
    input_entry.config(state="disabled")
    
    player_data_list = infoSQL.showPlayerInfo(player_name)
    
    if player_data_list == -1:
      error_msg = "플레이어 검색 불가"
      raise ValueError(error_msg)
    
    player_info = player_data_list[0]
    
    global equip_info
    equip_info = player_data_list[1]
    
    for label in eq_info_label_list:
      label.config(text="")
    
    getImage(player_info[0][3])
    updateInfo(player_info[0])
    
    for info in equip_info:
      getEquipImage(info[4], equip_button_list[info[2] - 1])
    
  except TypeError as e:
    print(f"{e}")
    return
  
  except ValueError as e:
    initInfo(error_msg)
    return
  
  finally:
    input_button.config(state="normal")
    input_entry.config(state="normal")

#플레이어 이미지를 불러오는 함수
def getImage(url):
  response = requests.get(url)

  if response.status_code == 200:
    image_data = response.content
    player_image = ImageTk.PhotoImage(Image.open(BytesIO(image_data)))
    
    player_img_label.config(image=player_image, bd=1, relief="solid", width=160, height=140)
    player_img_label.image = player_image

#플레이어가 장비한 장비의 이미지를 불러오는 함수
def getEquipImage(url, label):
  response = requests.get(url)

  if response.status_code == 200:
    image_data = response.content
    player_image = ImageTk.PhotoImage(Image.open(BytesIO(image_data)))
    
    label.config(image=player_image, bd=1, relief="solid", width=36, height=36, state="normal")
    label.image = player_image

#검색이 가능한 유저고, DB에 정보가 있을 시 불러오는 함수
def updateInfo(player_info):
  str_player_info = [str(x) for i, x in enumerate(player_info) if i != 3]
  
  for idx, label in enumerate(info_label_list):
    label.config(text=label_name_list[idx] + " : " + str_player_info[idx+1], fg="black")

#정보 초기화
def initInfo(msg):
  player_img_label.config(image="", bd=0, relief=None)
  
  for i in range(0, 10):
    info_label_list[i].config(text=label_name_list[i])
  
  info_label_list[10].config(text=msg, fg="red")
  
  for btn in equip_button_list:
    if btn is not None:
      btn.config(image="", state="disabled", bd=0)
  
  for label in eq_info_label_list:
    label.config(text="")
  
def displayEquipInfo(eq_class):
  equip_label_name_list = ['아이템 이름', '등급', '스타포스', '공격속도', 'STR', 'DEX', 'INT', 'LUK', 'MaxHP', 'MaxMP', '공격력', '마력',
                          '물리방어력', '이동속도', '점프력', '보스 몬스터공격 시', '몬스터 방어력 무시', '올스탯', '착용 레벨 감소', 
                          '업그레이드 가능 횟수', '가위 사용 가능 횟수', '잠재옵션', '에디셔널 잠재옵션', '소울옵션', '기타']
  
  eq_info = [elem for idx, elem in enumerate(equip_info[eq_class]) if idx not in [0, 2, 4, 6]]
  
  eq_info_label_list.clear()
  
  i = gap = 0
  for info in eq_info:
    if i == 0:
      label = Label(root, text=info)
      label.place(x=200, y=300)
      eq_info_label_list.append(label)
    elif i == 1:
      grade = '일반' if info is None else info
      label = Label(root, text=grade + " 아이템")
      label.place(x=200, y=320)
      eq_info_label_list.append(label)
    elif i == 2 and info != '0':
      label = Label(root, text='⭐x' + str(info))
      label.place(x=200, y=340)
      eq_info_label_list.append(label)
    elif i == 21:
      label = Label(root, text='잠재옵션')
      label.place(x=200, y=360)
      eq_info_label_list.append(label)
      
      label = Label(root, text=info)
      label.place(x=200, y=380)
      eq_info_label_list.append(label)
    elif i == 22:
      label = Label(root, text='에디셔널 잠재옵션')
      label.place(x=200, y=440)
      eq_info_label_list.append(label)
      
      label = Label(root, text=info)
      label.place(x=200, y=460)
      eq_info_label_list.append(label)
    elif info is not None and i != 24:
      label = Label(root, text=equip_label_name_list[i] + ' ' + str(info))
      label.place(x=400, y=300+20*gap)
      eq_info_label_list.append(label)
      gap = gap + 1
    i = i + 1

root = Tk()
root.geometry("720x600")
root.resizable(False, False)
root.title("PlayerInfo GUI")
player_name = ""

nick_label = Label(root, text=" 닉네임입력 ", bd=1, relief="solid")
nick_label.grid(row=0, column=1, padx=2, pady=2)

input_entry = Entry(root, width=15)
input_entry.grid(row=1, column=1, padx=1, pady=2)
input_entry.bind("<Return>", lambda event=None: updateInfoButton())

input_button = Button(root, text="검색", command=updateInfoButton)
input_button.grid(row=1, column=2)

playername_label = Label(root, text="닉네임 : ", width=18)
playername_label.grid(row=2, column=1, padx=1, pady=3)

player_img_label = Label(root)
player_img_label.place(x=2, y=80)

info_label_list = []
label_name_list = ["레벨", "직업", "스공", "힘", "덱스", "인트", "럭", "크리티컬 데미지", "보스 데미지", "방어율 무시", "갱신일"]

for i in range(10):
  label = Label(root, text=label_name_list[i] + " : ")
  label.place(x=8, y=250+25*i)
  info_label_list.append(label)

label = Label(root)
label.place(x=50, y=230)
info_label_list.append(label)

equip_button_list = []
dx = dy = 0

eq_c = 0
for idx in range(0, 30):
  if idx not in [1, 3, 8, 25, 26]:
    button = Button(root, command=lambda c = eq_c: displayEquipInfo(c), state="disabled", bd=0)
    button.place(x=320+45*dx, y=20+45*dy)
    equip_button_list.append(button)
    eq_c = eq_c + 1
    
  else:
    equip_button_list.append(None)
    
  dx+=1
  
  if dx==5:
    dx=0
    dy+=1

root.mainloop()