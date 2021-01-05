#!/usr/bin/python
# -*- coding: UTF-8 -*-

'''
此功能是将问卷中的关键举证按照整合分为自评和他评并按照特定的格式输出到新的excel中，方便评估确定
'''
import xlrd
import os
from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showinfo

def import_excel(excel_tables):
    '''
    打开excel表格，将excel表格内容导入到tables_list列表中
    '''
    for rown in range(excel_tables.nrows):
        array = {'是否生成xml':'' , '位号':'' , '板卡型号':'' , '配屏':'' , '输入信号':'' , '分辨率':'' , 'PMIC型号':'' , 'GAMMA型号':'' , 'SOC型号':'' , 'FLASH型号':'' , 'FlashSize':'' , '烧录需求':'' , 'CheckSum':'' , '特殊需求':'' , '日期':'' , '主芯片SVN':'' , '客制化':''}

        array['是否生成xml'] = excel_tables.cell_value(rown,0)
        array['位号'] = excel_tables.cell_value(rown,1)
        array['板卡型号'] = excel_tables.cell_value(rown,2)
        array['配屏'] = excel_tables.cell_value(rown,3)
        array['输入信号'] = excel_tables.cell_value(rown,4)
        array['分辨率'] = excel_tables.cell_value(rown,5)

        tables_list.append(array)

    tables_list.pop(0) #删掉第一列的数据

def result_check(result):
    '''
    建议自评和他评的结果：1、去掉空格；2、全部转化为大写；3、如果输入了多个字母则提示报错
    ''' 
    result_str = result.strip().upper()
    if (len(result_str) == 1):
        return result_str
    else:
        showinfo(title='提示', message='结果输入错误，请检查！')
        return 0

def assessed_number(excel_tables):
    '''
    被评价的人数
    '''
    total_ncols = excel_tables.ncols #总共的列
    return (total_ncols - 4)/4

def appraise_number(excel_tables):
    '''
    评价的人数，即有多少人参与了评价
    '''
    total_nrows = excel_tables.nrows #总共的列
    return (total_nrows - 3)

def get_key_quote():
    '''
    获取关键举证的数据
    '''
    excel_file = file_text.get()
    data = xlrd.open_workbook(excel_file)
    sheet_table = data.sheets()[0] #读取excel表中的sheet1
    #import_excel(sheet_table)


def fileopen():
    '''
    打开文件
    '''
    file_text.set('') #清除文件内容
    excel_file = askopenfilename()
    if excel_file:
        file_text.set(excel_file)

if __name__ == "__main__":
    #关键举证输出的文件
    output_file = "关键举证.xls"

    #可视化界面
    frameT = Tk()
    frameT.geometry('500x100+400+200')
    frameT.title('关键举证')
    frame = Frame(frameT)
    frame.pack(padx=10 , pady=10) #设置外边框
    frame1 = Frame(frameT)
    frame1.pack(padx=10 , pady=10) #设置外边框

    file_text = StringVar()

    ent = Entry(frame,width=50,textvariable=file_text).pack(fill=X,side=LEFT) #X方向填充，靠左
    btn = Button(frame,width=20,text='选择文件',font=('宋体',14),command=fileopen).pack(fill=X,padx=10)
    ext = Button(frame1,width=10,text='开始',font=('宋体',14),command=get_key_quote).pack(fill=X,side=LEFT)
    etb = Button(frame1,width=10,text='退出',font=('宋体',14),command=frameT.quit).pack(fill=Y,padx=10)
    frameT.mainloop()
