#!/usr/bin/python
# -*- coding: UTF-8 -*-

'''
此功能为将TCON xml中所需要的的属性有Excel转化为xml
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
        array = {'是否生成xml':'' , '板卡型号':'' , '芯片型号':'' , '配屏':'' , '分辨率':'' , 'PMIC型号':'' , 'GAMMA型号':'' , 'SOC型号':'' , 'FLASH型号':'' , 'FlashSize':'' , '烧录需求':'' , 'CheckSum':'' , '特殊需求':'' , '审核备注':''}

        array['是否生成xml'] = excel_tables.cell_value(rown,0)
        array['板卡型号'] = excel_tables.cell_value(rown,1)
        array['芯片型号'] = excel_tables.cell_value(rown,2)
        array['配屏'] = excel_tables.cell_value(rown,3)
        array['分辨率'] = excel_tables.cell_value(rown,4)
        array['PMIC型号'] = excel_tables.cell_value(rown,5)
        array['GAMMA型号'] = excel_tables.cell_value(rown,6)
        array['SOC型号'] = excel_tables.cell_value(rown,7)
        array['FLASH型号'] = excel_tables.cell_value(rown,8)
        array['FlashSize'] = excel_tables.cell_value(rown,9)
        array['烧录需求'] = excel_tables.cell_value(rown,10)
        array['CheckSum'] = excel_tables.cell_value(rown,11)
        array['特殊需求'] = excel_tables.cell_value(rown,12)
        array['审核备注'] = excel_tables.cell_value(rown,13)
        tables_list.append(array)

    tables_list.pop(0) #删掉第一列的数据

def excel_to_xml(num):
    xml_path = output_folder + '/TCON'
    
    if tables_list[num]['板卡型号'] != '无':
        xml_path += '_' + tables_list[num]['板卡型号']
    if tables_list[num]['芯片型号'] != '无':
        xml_path += '_' + tables_list[num]['芯片型号']
    if tables_list[num]['配屏'] != '无':
        xml_path += '_' + tables_list[num]['配屏']
    if tables_list[num]['PMIC型号'] != '无':
        xml_path += '_' + tables_list[num]['PMIC型号']
    if tables_list[num]['GAMMA型号'] != '无':
        xml_path += '_' + tables_list[num]['GAMMA型号']
    if tables_list[num]['SOC型号'] != '无':
        xml_path += '_' + tables_list[num]['SOC型号']
    
    xml_path += '_' + tables_list[num]['CheckSum'] + '.xml'

    tcon_xml = open(xml_path , "w" , encoding='utf8') # 文件读写方式是追加

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

def run():
    excel_file = file_text.get()
    data = xlrd.open_workbook(excel_file)
    sheet_table = data.sheets()[0] #读取excel表中的sheet1
    import_excel(sheet_table)

    excel_to_xml_num = 0

    if len(tables_list) == 0:
        showinfo(title='提示', message='Excel中无数据，请检查')
    else:
        for i in range(0 , len(tables_list)):
            if tables_list[i]['是否生成xml'] == '是':
                excel_to_xml_num += 1
                excel_to_xml(i)
        
        if (excel_to_xml_num == 0):
            showinfo(title='提示', message='Excel中无需要生成xml的数据，请检查')
        else:
            tip_message = str(excel_to_xml_num) + '条数据已转化，请查看' + output_folder + '文件夹下的xml文件'
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

    dict_Attribute = {'板卡型号':'SW_Chipset' , '芯片型号':'SW_ChipSeries' , '配屏':'SW_Panel' , '分辨率':'SW_PanelResolution' , 'PMIC型号':'SW_PMICType' , 'GAMMA型号':'SW_GAMMAType' , 'SOC型号':'SW_SOCType' , 'FLASH型号':'SW_FlashType' , 'FlashSize':'SW_FlashSize' , '烧录需求':'SW_CvteFactoryKey' , 'CheckSum':'SW_CheckSum' , '特殊需求':'SW_SpecialDemand' , '审核备注':'SW_ReviewRemark'}

    #xml输出的文件夹
    output_folder = "TCON_XML"
    if not os.path.isdir(output_folder):
        os.makedirs(output_folder)

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
