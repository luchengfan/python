#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showinfo

def run():
    SOC_filename = file_text.get()
    if '.bin' in SOC_filename:
        SOC_filename = SOC_filename.strip().rstrip('.bin')

    if 'SOC' not in SOC_filename:
        showinfo(title='提示', message='请使用SOC软件生成xml')
        file_text.set('') #清除文件内容
        return 0

    file_path = r'C:\Users\user\Desktop'
    if not os.path.exists(file_path):
        file_path = r'D:'

    xml_path = file_path + '\\' + SOC_filename + '.xml'

    checksum_ymd = SOC_filename.split('_')[-2] #年、月、日
    checksum_hm = SOC_filename.split('_')[-1] #时、分
    checksum_date = checksum_ymd + '_' + checksum_hm

    if os.path.exists(xml_path):
        os.remove(xml_path)

    tcon_xml = open(xml_path , "w" , encoding='utf8')

    tcon_xml.write('<?xml version="1.0" encoding="utf-8"?>' + '\n')
    tcon_xml.write('<Root>' + '\n')
    tcon_xml.write(' '*4 + '<Confirmation>' + '\n')
    tcon_xml.write(' '*8 + '<SW_Items>' + '\n')
    tcon_xml.write(' '*12 + '<Attr Name="SW_CheckSum" Alias="SW_CheckSum" Ids="0" Atoms="' + checksum_date + '"/>' + '\n')
    tcon_xml.write(' '*12 + '<Attr Name="SW_DD_PCC" Alias="SW_DD_PCC" Ids="0" Atoms="NONE"/>' + '\n')
    tcon_xml.write(' '*8 + '</SW_Items>' + '\n')
    tcon_xml.write(' '*4 + '</Confirmation>' + '\n')
    tcon_xml.write('</Root>' + '\n')

    tips_message = 'xml文件已生成，请查看' + xml_path + '文件'
    showinfo(title='提示', message=tips_message)
    file_text.set('') #清除文件内容

if __name__ == "__main__":
    #可视化界面
    frameT = Tk()
    frameT.geometry('500x100+400+200')
    frameT.title('TCON xml')
    frame = Frame(frameT)
    frame.pack(padx=10 , pady=10) #设置外边框
    frame1 = Frame(frameT)
    frame1.pack(padx=10 , pady=10) #设置外边框

    file_text = StringVar()

    ent = Entry(frame,width=100,textvariable=file_text).pack(fill=X,side=LEFT) #X方向填充，靠左
    ext = Button(frame1,width=10,text='开始',font=('宋体',14),command=run).pack(fill=X,side=LEFT)
    etb = Button(frame1,width=10,text='退出',font=('宋体',14),command=frameT.quit).pack(fill=Y,padx=10)
    frameT.mainloop()
