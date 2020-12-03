import xml.dom.minidom
import os
import xlrd
import xlwt
from xlutils.copy import copy
from openpyxl import *

def get_language_type(excel_file):
    input_in_title = []
    input_not_in_title = []
    table_list = []
    lang_type_num = []

    excel_filename = excel_file.split(r'/')[-1] #获取excel的文件名
    excel_folder_path = excel_file.replace(excel_filename , '')  #获取excel文件夹路径

    if is_dir:
        get_language_type_file = 'get_language_type/' + excel_folder_path
    else:
        get_language_type_file = 'get_language_type/'

    if not os.path.isdir(get_language_type_file):
        os.makedirs(get_language_type_file)

    output_file = get_language_type_file + excel_filename

    data = xlrd.open_workbook(excel_file , formatting_info=True)
    sheet_table = data.sheets()[0] #读取excel表中的sheet1

    old_content = copy(data)
    ws = old_content.get_sheet(0)

    for col in range(sheet_table.ncols): #列
        excel_title.append(sheet_table.cell(0,col).value)

    for lang_type in get_lang_type_list:
        for excel_title_content in excel_title:
            if lang_type in excel_title_content:
                input_in_title.append(lang_type)

    input_not_in_title = [item for item in get_lang_type_list if item not in input_in_title]

    if len(input_not_in_title) != 0:
        print(input_not_in_title , "不在语言列表中，请确认是否输入错误")
        exit(0)

    lang_type_num.append(0)
    for input_type in input_in_title:
        for i in range(0 , len(excel_title)):
            if input_type in excel_title[i]:
                lang_type_num.append(i)

    for row in range(sheet_table.nrows): #行
        for col in range(sheet_table.ncols): #列
            ws.write(row , col , "")

    for row in range(sheet_table.nrows): #行
        col_num = 0
        for col in range(sheet_table.ncols): #列
            if col in lang_type_num:
                ws.write(row , col_num , sheet_table.cell(row,col).value)
                col_num += 1
            old_content.save(output_file)

def get_file(excel_file_path):
    '''
    获取传参路径下的xls/xlsx文件
    返回当前文件夹及其子目录下所有的xls/xlsx文件(包括绝对路径)
    '''
    xml_type_list = [".xls" , ".xlsx"]
    xml_list = []

    for root, dirs, files in os.walk(excel_file_path):
        for file in files:
            for xml_type in xml_type_list:
                if file.endswith(xml_type):
                    filename = root + "/" + file #注意不要改动"/"
                    xml_list.append(filename)
    return xml_list

if __name__ == "__main__":
    get_excel_file = input("请输入处理的文件或文件夹：")
    get_lang_type = input("请输入要保留的语言，以'_'区分，例如：English_Thai_Russian：")
    get_lang_type_list = get_lang_type.split("_")
    
    excel_title = []
    is_dir = False

    if os.path.isdir(get_excel_file): #文件夹
        is_dir = True
        get_language_type_file = get_file(get_excel_file)
        if len(get_language_type_file) == 0:
            print ("当前路径下无xml文件")
            exit(0)
        else:
            for file_path in get_language_type_file:
                get_language_type(file_path)
    elif os.path.isfile(get_excel_file): #文件
        if (get_excel_file.endswith(".xls") or get_excel_file.endswith(".xlsx")):
            is_dir = False
            get_language_type(get_excel_file)
        else:
            print ("请输入xml或者excel文件")
            exit(0)
    else:
        print ("请检查输入的路径是否存在")
