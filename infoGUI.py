from tkinter import *
from PIL import Image, ImageTk
from io import BytesIO
import requests
import infoSQL

def updateInfoButton():
  player_name = input_entry.get()
  
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
    #equip_info = player_data_list[1]
    
    getImage(player_info[3])
    updateInfo(player_info)
    
    input_button.config(state="normal")
    input_entry.config(state="normal")
      
  except TypeError as e:
    print(f"{e}")
    return
  
  except ValueError as e:
    initInfo(error_msg)
    return

def getImage(url):
  response = requests.get(url)

  if response.status_code == 200:
    image_data = response.content
    player_image = ImageTk.PhotoImage(Image.open(BytesIO(image_data)))
    
    player_img_label.config(image=player_image, bd=1, relief="solid", width=160, height=140)
    player_img_label.image = player_image


def updateInfo(player_info):
  str_player_info = [str(x) for i, x in enumerate(player_info) if i != 3]
  
  for idx, label in enumerate(info_label_list):
    label.config(text=label_name_list[idx] + " : " + str_player_info[idx+1])

def initInfo(msg):
  player_img_label.config(image="", bd=0, relief=None)
  
  for i in range(0, 10):
    info_label_list[i].config(text=label_name_list[i])
  
  info_label_list[10].config(text=msg, fg="red")

root = Tk()
root.geometry("720x600")
root.resizable(False, False)

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

update_button = Button(root, text="갱신", command=lambda:updateInfo(player_name))
update_button.place(x=8, y=225)

info_label_list = []
label_name_list = ["레벨", "직업", "스공", "힘", "덱스", "인트", "럭", "크리티컬 데미지", "보스 데미지", "방어율 무시", "갱신일"]

for i in range(10):
  label = Label(root, text=label_name_list[i] + " : ")
  label.place(x=8, y=255+25*i)
  info_label_list.append(label)

label = Label(root)
label.place(x=50, y=230)
info_label_list.append(label)

root.mainloop()