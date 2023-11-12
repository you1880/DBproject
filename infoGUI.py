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
    player_info = infoSQL.showPlayerInfo(player_name)
    if player_info == -1:
      error_msg = "플레이어 검색 불가"
      raise ValueError(error_msg)
    
    getImage(player_info[0][3])
    updateInfo(player_info)
  except TypeError as e:
    print(f"{e}")
    return
  except ValueError as e:
    update_label.config(text=error_msg, fg="red")
    return

def on_enter(event=None):
  player_name = input_entry.get()
  if not len(player_name):
    return
  playername_label.config(text=f"닉네임 : {player_name}")
  input_entry.delete(0, END)
  
  try:
    player_info = infoSQL.showPlayerInfo(player_name)
    if player_info == -1:
      error_msg = "플레이어 검색 불가"
      raise ValueError(error_msg)
    input_entry.config(state=DISABLED)
    input_button.config(state=DISABLED)
    
    getImage(player_info[0][3])
    updateInfo(player_info)
    #updateEquipment(player_info)
    input_entry.after(0, lambda: input_entry.config(state=NORMAL))
  except TypeError as e:
    print(f"{str(e)}")
    return
  except ValueError as e:
    update_label.config(text=error_msg, fg="red")
    return

def getImage(url):
  response = requests.get(url)

  if response.status_code == 200:
    image_data = response.content
    player_image = ImageTk.PhotoImage(Image.open(BytesIO(image_data)))
    
    player_img_label.config(image=player_image, bd=1, relief="solid", width=160, height=140)
    player_img_label.image = player_image


def updateInfo(player_info):
  str_player_info = [str(x) for x in player_info[0]]
  
  update_label.config(text="갱신일 : " + str_player_info[-1])
  player_lv_label.config(text="레벨 : " + str_player_info[1])
  player_job_label.config(text="직업 : " + str_player_info[2])
  player_atk_label.config(text="스공 : " + str_player_info[4])
  player_str_label.config(text="힘 : " + str_player_info[5])
  player_dex_label.config(text="덱스 : " + str_player_info[6])
  player_int_label.config(text="인트 : " + str_player_info[7])
  player_luk_label.config(text="럭 : " + str_player_info[8])
  player_crt_label.config(text="크리티컬 데미지 : " + str_player_info[9])
  player_bos_label.config(text="보스 데미지 : " + str_player_info[10])
  player_ing_label.config(text="방어율 무시 : " + str_player_info[11])

root = Tk()
root.geometry("720x600")
root.resizable(False, False)

player_name = ""

nick_label = Label(root, text=" 닉네임입력 ", bd=1, relief="solid")
nick_label.grid(row=0, column=1, padx=2, pady=2)

input_entry = Entry(root, width=15)
input_entry.grid(row=1, column=1, padx=1, pady=2)
input_entry.bind("<Return>", on_enter)

input_button = Button(root, text="검색", command=updateInfoButton)
input_button.grid(row=1, column=2)

playername_label = Label(root, text="닉네임 : ", width=18)
playername_label.grid(row=2, column=1, padx=1, pady=3)

player_img_label = Label(root)
player_img_label.place(x=2, y=80)

update_button = Button(root, text="갱신", command=lambda:updateInfo(player_name))
update_button.place(x=8, y=225)

update_label = Label(root, text="갱신일 : ")
update_label.place(x=50, y=230)

player_lv_label = Label(root, text="레벨 : ")
player_lv_label.place(x=8, y=255)

player_job_label = Label(root, text="직업 : ")
player_job_label.place(x=8, y=280)

player_atk_label = Label(root, text="스공 : ", width=24)
player_atk_label.place(x=6, y=305)

player_str_label = Label(root, text="힘 : ")
player_str_label.place(x=8, y=330)

player_dex_label = Label(root, text="덱스 : ")
player_dex_label.place(x=8, y=355)

player_int_label = Label(root, text="인트 : ")
player_int_label.place(x=8, y=380)

player_luk_label = Label(root, text="럭 : ")
player_luk_label.place(x=8, y=405)

player_crt_label = Label(root, text="크리티컬 데미지 : ")
player_crt_label.place(x=8, y=430)

player_bos_label = Label(root, text="보스 데미지 : ")
player_bos_label.place(x=8, y=455)

player_ing_label = Label(root, text="방어율 무시 : ")
player_ing_label.place(x=8, y=480)

root.mainloop()