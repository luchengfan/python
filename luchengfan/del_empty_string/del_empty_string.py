import xml.dom.minidom
import os
import xlrd
import xlwt
from xlutils.copy import copy

def del_xml_empty_string(xml_file):
    '''
    删除xml文件中的空元素，例如:
    <string name="COUNTRY_SG_LOCK_INFO_7" />
    '''
    input_file = open(xml_file ,'r' , encoding="utf-8")

    temp_path = xml_file.split(r'/')[-1] #获取xml的文件名
    folder_path = xml_file.replace(temp_path , '')  #获取xml文件夹路径

    if is_dir:
        del_empty_str_file = 'del_empty_string/xml/' + folder_path
    else:
        del_empty_str_file = 'del_empty_string/xml/'

    if not os.path.isdir(del_empty_str_file):
        os.makedirs(del_empty_str_file)

    output_file = open(del_empty_str_file + temp_path, 'w' , encoding="utf-8")

    all_strings = input_file.readlines()
    for line in all_strings:
        if (r'" />' not in line):
            output_file.write(line)
    output_file.close()

def valid_data(data):
    '''
    判断当前的数据是否有效，当为空时判断为无效数据
    如果是有效数据则返回True，如果是无效数据则返回False
    '''
    if ((data.isspace()) or (len(data) == 0)):
        return False
    else:
        return True

def del_excel_empty_string(excel_file):
    '''
    删除excel文件中的空元素
    '''
    styleBlueBkg = xlwt.easyxf('pattern: pattern solid, fore_colour red;')  # 红色
    input_file = open(excel_file ,'r' , encoding="utf-8")

    temp_path = excel_file.split(r'/')[-1] #获取excel的文件名
    folder_path = excel_file.replace(temp_path , '')  #获取excel文件夹路径

    if is_dir:
        del_empty_str_file = 'del_empty_string/excel/' + folder_path
    else:
        del_empty_str_file = 'del_empty_string/excel/'

    if not os.path.isdir(del_empty_str_file):
        os.makedirs(del_empty_str_file)

    output_file = del_empty_str_file + temp_path 

    data = xlrd.open_workbook(excel_file , formatting_info=True)
    sheet_table = data.sheets()[0] #读取excel表中的sheet1

    old_content = copy(data)
    ws = old_content.get_sheet(0)

    for row in range(sheet_table.nrows): #行
        for col in range(sheet_table.ncols): #列
            if ((row != 0) and (col != 0)):
                if not valid_data(sheet_table.cell(row,col).value):
                    ws.write(row , col , sheet_table.cell(row,1).value , styleBlueBkg)
                    old_content.save(output_file)

def get_file(del_file_path):
    '''
    获取传参路径下的xml/xls/xlsx文件
    返回当前文件夹及其子目录下所有的xml/xls/xlsx文件(包括绝对路径)
    '''
    xml_type_list = [".xml" , ".xls" , ".xlsx"]
    xml_list = []

    for root, dirs, files in os.walk(del_file_path):
        for file in files:
            for xml_type in xml_type_list:
                if file.endswith(xml_type):
                    filename = root + "/" + file #注意不要改动"/"
                    xml_list.append(filename)
    return xml_list

if __name__ == "__main__":
    init_del_file = input('请输入处理的文件或文件夹：') 
    is_dir = False

    if os.path.isdir(init_del_file): #文件夹
        is_dir = True
        get_empty_str_file = get_file(init_del_file)
        if len(get_empty_str_file) == 0:
            print ("当前路径下无xml文件")
            exit(0)
        for file_path in get_empty_str_file:
            if file_path.endswith(".xml"):
                del_xml_empty_string(file_path)
            elif (file_path.endswith(".xls") or file_path.endswith(".xlsx")):
                del_excel_empty_string(file_path)
    elif os.path.isfile(init_del_file): #文件
        if init_del_file.endswith(".xml"):
            is_dir = False
            del_xml_empty_string(init_del_file)
        elif (init_del_file.endswith(".xls") or init_del_file.endswith(".xlsx")):
            is_dir = False
            del_excel_empty_string(init_del_file)
        else:
            print ("请输入xml或者excel文件")
            exit(0)
    else:
        print ("请检查输入的路径是否存在")
