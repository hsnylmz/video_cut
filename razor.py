import os
import subprocess
import datetime
import cv2

from tkinter import *
import tkinter.font as tkFont
from tkinter import messagebox

import ttkbootstrap as ttk
from ttkbootstrap.constants import *

from tkinter import filedialog, Tk, Button

window = ttk.Window(title="Razor by hsnylmz", themename="litera")
window.geometry("520x280")
window.resizable(True,True)

try:
    window.iconbitmap('razor.ico')
except:
    pass


source_video_path=""
target_video_file=""
file_ext=""
videos_folder = os.path.join(os.path.expanduser("~"), "Videos")
yolumuz=os.getcwd()

### frame rate alınması lazım...
def get_frame_rate(source_video_path):
    try:
        # Videoyu aç
        video_capture = cv2.VideoCapture(source_video_path)

        # Frame rate (FPS) değerini al
        fps = video_capture.get(cv2.CAP_PROP_FPS)

        # Videoyu kapat
        video_capture.release()

        return fps

    except Exception as e:
        print("Hata:", str(e))
        return None

def get_file_extension(file_path):
    # Dosya adını ve uzantısını ayırıyoruz
    file_name, file_extension = os.path.splitext(source_video_path)
    return file_extension

def cevir():
    global source_video_path, target_video_file
    
    source_video_path = filedialog.askopenfilename(initialdir=videos_folder)
        
    fps=get_frame_rate(source_video_path)
    print('Frame Rate : '+str(fps))
    
    print('Dosya Yolu : '+source_video_path)

    file_ext = get_file_extension(source_video_path)
    print('Kaynak dosya uzantısı : '+file_ext)
    
    source_file_name = source_video_path.split("/")[-1]
    print('Source File Name :'+ source_file_name)

    target_video_file = 'output_' + source_file_name
    print('Target File Name : '+target_video_file)

    secilen_video_label.config(text=f"Seçilen Video: {source_file_name}", font=("Arial", 14))
    secilen_video_frame_rate_label.config(text=f"Frame Rate : {fps}", font=("Arial", 14))

    olarak_kaydet_button.config(state=NORMAL)
    #convert_button.config(state=DISABLED)
       

def farkli_kaydet():
    
    global file_ext, source_file_name, yolumuz
    
    tc1=get_tc_1()
    tc_1=tc1.strip()
    print('tc1 : '+tc_1)

    tc2=get_tc_2()
    tc_2=tc2.strip()
    print('tc2 : '+tc_2)
    
    dest_file_path = filedialog.askdirectory()
    print('dest_file_path : '+dest_file_path)

    
    convert_command='{}/ffmpeg.exe -ss {} -i "{}" -c copy -t {} "{}/{}"'.format(yolumuz, tc_1, source_video_path, tc_2, dest_file_path, target_video_file)
    print('-')
    print('burası senin son uğraştığın yer : '+convert_command)


    os.system(convert_command)

    #biten klasörü aç
    os.chdir(dest_file_path)    
    print("Burası çıkış yeri şu an : "+dest_file_path)

    yolumuz_=os.getcwd()
    print("Burası da şu an bulunduğumuz yer : "+yolumuz_)
    subprocess.call('explorer ' + yolumuz_ + ', shell=True')
    
    #biten videoyu aç
    os.chdir(dest_file_path)
    subprocess.Popen([target_video_file], shell=True)


def get_tc_1():
    text_tc_1 = text_box_tc_1.get("1.0", ttk.END)
    print("Metin Kutusundaki Metin:")
    print(text_tc_1)
    return text_tc_1

def get_tc_2():
    text_tc_2 = text_box_tc_2.get("1.0", ttk.END)
    print("Metin Kutusundaki Metin:")
    print(text_tc_2)
    return text_tc_2


# USER INTERFACE
label_frame = ttk.LabelFrame(window, text="İşleminizi Seçiniz : ")
label_frame.pack(padx=5, pady=5)

label_frame_2 = ttk.LabelFrame(window, text="Video Özellikleri ")
label_frame_2.pack(padx=5, pady=5, fill=ttk.BOTH, expand=True)

head_label_tc1 = ttk.Label(label_frame, text="TC IN")
head_label_tc1.grid(row=0, column=1, padx=5, pady=5)

head_label_tc2 = ttk.Label(label_frame, text="TC DURATION")
head_label_tc2.grid(row=0, column=2, padx=5, pady=5)


convert_button = ttk.Button(label_frame, text="VİDEOYU SEÇİNİZ", command=cevir, width=15, bootstyle=SUCCESS)
#convert_button.pack(side='left', padx=5, pady=5)
convert_button.grid(row=1, column=0, padx=5, pady=5)

text_box_tc_1 = ttk.Text(label_frame, height=1, width=10,font=("Arial", 14))
text_box_tc_1.insert("1.0", "00:00:00.0")
#text_box_tc_1.pack(side='left', padx=5, pady=5)
text_box_tc_1.grid(row=1, column=1, padx=5, pady=5)

#label_tc2=ttk.Label(label_frame,text="TIMECODE DURATION : ")
#label_tc2.grid(row=4, column=0, padx=5, pady=5)

text_box_tc_2 = ttk.Text(label_frame, height=1, width=10,font=("Arial", 14))
text_box_tc_2.insert("1.0", "00:00:10.0")
#text_box_tc_2.pack(side='left', padx=5, pady=5)
text_box_tc_2.grid(row=1, column=2, padx=5, pady=5)

olarak_kaydet_button = ttk.Button(label_frame, text="K A Y D E T", command=farkli_kaydet, width=15, bootstyle=SUCCESS)
olarak_kaydet_button.config(state=DISABLED)
#olarak_kaydet_button.pack(side='left', padx=5, pady=5)
olarak_kaydet_button.grid(row=1, column=3, padx=5, pady=5)

secilen_video_label = ttk.Label(label_frame_2, text="")
secilen_video_label.place(x=5, y=5)

secilen_video_frame_rate_label = ttk.Label(label_frame_2, text="")
secilen_video_frame_rate_label.place(x=5, y=35)



window.mainloop()
