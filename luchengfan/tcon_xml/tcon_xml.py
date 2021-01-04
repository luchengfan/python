#!/usr/bin/python
# -*- coding: UTF-8 -*-

'''
此功能为将TCON xml中所需要的的属性有Excel转化为xml
excel表格第一行的密码为：cvte2020
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
        array['PMIC型号'] = excel_tables.cell_value(rown,6)
        array['GAMMA型号'] = excel_tables.cell_value(rown,7)
        array['SOC型号'] = excel_tables.cell_value(rown,8)
        array['FLASH型号'] = excel_tables.cell_value(rown,9)
        array['FlashSize'] = excel_tables.cell_value(rown,10)
        array['烧录需求'] = excel_tables.cell_value(rown,11)
        array['CheckSum'] = excel_tables.cell_value(rown,12)
        array['特殊需求'] = excel_tables.cell_value(rown,13)
        array['日期'] = excel_tables.cell_value(rown,14)
        array['主芯片SVN'] = excel_tables.cell_value(rown,15)
        array['客制化'] = excel_tables.cell_value(rown,16)
        tables_list.append(array)

    tables_list.pop(0) #删掉第一列的数据

def valid_data(data):
    '''
    判断当前的数据是否有效，当为空或者"无"时判断为无效数据
    如果是有效数据则返回true，如果是无效数据则返回false
    '''
    if ((data.isspace()) or (len(data) == 0) or (data == "无")):
        return 0
    else:
        return 1

def excel_to_xml(num , folder_path):
    '''
    将excel中的内容转化为xml文件输出
    '''

    xml_path = folder_path + output_folder
    if not os.path.isdir(xml_path):
        os.makedirs(xml_path)

    valid_number = valid_data(tables_list[num]['PMIC型号']) + valid_data(tables_list[num]['GAMMA型号']) + valid_data(tables_list[num]['SOC型号'])

    if (valid_number > 1):
        valid_number_tips = 'PMIC型号、GAMMA型号和SOC型号请分开三条数据填写，\n其余两个型号请填"无"'
        showinfo(title='提示', message=valid_number_tips)
        return 0

    xml_path += '/TCON'
    
    #判断位号数据的有效性
    if valid_data(tables_list[num]['位号']):
        xml_path += '_' + tables_list[num]['位号']
    else:
        showinfo(title='提示', message='位号数据不符合要求，请检查')
        return 0

    #判断板卡型号数据的有效性
    if valid_data(tables_list[num]['板卡型号']):
        xml_path += '_' + tables_list[num]['板卡型号']
    else:
        showinfo(title='提示', message='板卡型号数据不符合要求，请检查')
        return 0

    #判断配屏数据的有效性
    if valid_data(tables_list[num]['配屏']):
        xml_path += '_' + tables_list[num]['配屏']
    else:
        showinfo(title='提示', message='配屏数据不符合要求，请检查')
        return 0
 
    #判断输入信号数据的有效性
    if valid_data(tables_list[num]['输入信号']):
        xml_path += '_' + tables_list[num]['输入信号']
    else:
        showinfo(title='提示', message='输入信号数据不符合要求，请检查')
        return 0

    if valid_data(tables_list[num]['PMIC型号']):
        xml_path += '_PMIC_' + tables_list[num]['PMIC型号']
    elif valid_data(tables_list[num]['GAMMA型号']):
        xml_path += '_GAMMA_' + tables_list[num]['GAMMA型号']
    elif valid_data(tables_list[num]['SOC型号']):
        xml_path += '_SOC_' + tables_list[num]['SOC型号']

    #判断输入信号数据的有效性
    if ((not valid_data(tables_list[num]['CheckSum'])) 
         or ('0x' not in tables_list[num]['CheckSum'])):
        showinfo(title='提示', message='CheckSum数据不符合要求(需以0x开头)，请检查')
        return 0
    else:
        xml_path += '_' + tables_list[num]['CheckSum']
    
    #判断日期数据的有效性
    if valid_data(tables_list[num]['日期']):
        xml_path += '_' + tables_list[num]['日期']
    else:
        showinfo(title='提示', message='日期数据不符合要求，请检查')
        return 0

    #判断主芯片SVN数据的有效性
    SVN_number = str(tables_list[num]['主芯片SVN'])
    SVN_number = SVN_number.split('.')[0]
    if (str.isdigit(SVN_number)):
        SVN_number = int(tables_list[num]['主芯片SVN'])
        xml_path += '_svn' + str(SVN_number)
    elif valid_data(SVN_number):
        showinfo(title='提示', message='主芯片SVN数据不符合要求，请检查')
        return 0

    #判断输入信号数据的有效性
    if valid_data(tables_list[num]['客制化']):
        xml_path += '_' + tables_list[num]['客制化']

    xml_path += '.xml'

    tcon_xml = open(xml_path , "w" , encoding='utf8')

    add_xml.append('<?xml version="1.0" encoding="utf-8"?>')
    add_xml.append('<Root>')
    add_xml.append(' '*4 + '<Confirmation>')
    add_xml.append(' '*8 + '<SW_Items>')

    for key,value in dict_Attribute.items():
        add_xml.append(' '*12 + '<Attr Name="' + value + '" Alias="' + value + '" Ids="0" Atoms="' + tables_list[num][key] + '"/>')
    
    add_xml.append(' '*12 + '<Attr Name="SW_DD_PCC" Alias="SW_DD_PCC" Ids="0" Atoms="NONE"/>')
    add_xml.append(' '*8 + '</SW_Items>')
    add_xml.append(' '*4 + '</Confirmation>')
    add_xml.append('</Root>' + '\n')

    for i in add_xml :
        tcon_xml.write(i + '\n')
    
    add_xml.clear()
    return 1
    
def run():
    '''
    执行excel转化为xml的操作
    '''
    tables_list.clear()
    excel_file = file_text.get()
    data = xlrd.open_workbook(excel_file)
    sheet_table = data.sheets()[0] #读取excel表中的sheet1
    import_excel(sheet_table)

    temp_path = excel_file.split(r'/')[-1] #获取excel的文件名
    folder_path = excel_file.replace(temp_path , '')  #获取excel文件夹路径

    excel_to_xml_num = 0

    if len(tables_list) == 0:
        showinfo(title='提示', message='Excel中无数据，请检查')
    else:
        for i in range(0 , len(tables_list)):
            if tables_list[i]['是否生成xml'] != '否':
                excel_to_xml_num += excel_to_xml(i , folder_path)
        
        if (excel_to_xml_num == 0):
            showinfo(title='提示', message='无需要生成xml的数据，请检查数据是否符合需求')
        else:
            tip_message = str(excel_to_xml_num) + '条数据已转化完成。\n请查看' + folder_path + output_folder + '文件夹下的xml文件'
            showinfo(title='提示', message=tip_message)
            frameT.quit()

def fileopen():
    '''
    打开文件
    '''
    file_text.set('') #清除文件内容
    excel_file = askopenfilename()
    if excel_file:
        file_text.set(excel_file)

if __name__ == "__main__":
    tables_list = []  #创建一个空列表，存储Excel的数据
    add_xml = []  #创建一个空列表，用来存储xml中的内容

    dict_Attribute = {'板卡型号':'SW_Chipset' , '配屏':'SW_Panel' , '分辨率':'SW_PanelResolution' , 'PMIC型号':'SW_PMICType' , 'GAMMA型号':'SW_GAMMAType' , 'SOC型号':'SW_SOCType' , 'FLASH型号':'SW_FlashType' , 'FlashSize':'SW_FlashSize' , '烧录需求':'SW_CvteFactoryKey' , 'CheckSum':'SW_CheckSum' , '特殊需求':'SW_SpecialDemand'}

    #xml输出的文件夹
    output_folder = "TCON_XML"

    #可视化界面
    frameT = Tk()
    frameT.geometry('500x100+400+200')
    frameT.title('TCON xml')
    frame = Frame(frameT)
    frame.pack(padx=10 , pady=10) #设置外边框
    frame1 = Frame(frameT)
    frame1.pack(padx=10 , pady=10) #设置外边框

    file_text = StringVar()

    ent = Entry(frame,width=50,textvariable=file_text).pack(fill=X,side=LEFT) #X方向填充，靠左
    btn = Button(frame,width=20,text='选择文件',font=('宋体',14),command=fileopen).pack(fill=X,padx=10)
    ext = Button(frame1,width=10,text='开始',font=('宋体',14),command=run).pack(fill=X,side=LEFT)
    etb = Button(frame1,width=10,text='退出',font=('宋体',14),command=frameT.quit).pack(fill=Y,padx=10)
    frameT.mainloop()
