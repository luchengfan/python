#!/usr/bin/python
#-*- coding:utf-8 -*-

import xlwt, xlrd
import json
from optparse import OptionParser
import os
import xml.etree.ElementTree as ET
import lans_dict
import blacklist
import collections

TRANSLATE_PATH = 'src/main/res'
# module名称，一般默认为app，某些项目包含不同的module也需要翻译，可以通过设定单独指定
APP_NAME = 'app'
STRING_FILE_NAME = 'values/strings.xml'
UNTRANSLATE_FILE_NAME = 'values/strings_untranslate.xml'
WILL_TRANSLATE_FILE_NAME = 'values/strings_will_translate.xml'
EXCEL_FILE_NAME = 'translate.xls'
SHEET_NAMES = ['translate', 'untranslate', 'willtranslate']

def createDir(path) :
    if not os.path.exists(path): os.makedirs(path)
    return path

#   目前要求若目录存在则直接覆盖,不再生成额外的文件夹
#    else:
#        path = path+'_1'
#        return createDir(path)

# 设置脚本接收参数，由于xlwt只支持较低版本的excel，因此创建的文件类型应该对应.xls而非.xlsx
def set_opt() :
    parser = OptionParser()
    parser.add_option('-m', '--mode', help='set translate mode. default is 1 for read xml and ouput excel, 2 for read excel and output xml', dest='mode', action='store', type='int', default='1')
    parser.add_option('-i','--input', help="set app's dir path in mode1, set excel name in mode2", dest='input_path', action='store', type='string')
    parser.add_option('-o','--ouput', help="set output file name in mode1, default is translate.xls/strings.xml. set output_dirs in mode2, default is projects' name", dest='output', action='store', type='string', default=EXCEL_FILE_NAME)
    parser.add_option('-a','--app',help="set app dirs name, default is app, only useful in mode1",dest='app_dir',action='store',type='string',default=APP_NAME)
    return parser.parse_args()

# path：app的根目录 将遍历res文件夹寻找所有翻译后的strings.xml文件，但是过滤掉/values目录以及黑名单中的文件
def get_files_list(path) :
    string_files = []
    will_translate_files = []
    for (root, dirs, files) in os.walk(path) :
        for f in files:
            # 过滤掉values文件夹下的strings.xml以及可能存在的untranslate、will translate文件单独处理
            if root.split('/')[-1] in blacklist.BLACK_LIST:
                continue
            if f.endswith("strings.xml") : 
                string_files.append(os.path.join(root,f))
            elif f.endswith("strings_will_translate.xml"):
                will_translate_files.append(os.path.join(root,f))
    return string_files,will_translate_files

# 解析strings.xml key为name属性，value为节点的值
def parse_xml(xml_path) :
    results = collections.OrderedDict()
    tree = ET.parse(xml_path)
    root = tree.getroot()
    for child in root :
        if not child.text:
            child.text = ''
        results[child.attrib['name']] = child.text.replace("\\'","'").replace('\\"', '"')
    return results

# 创建row索引，用于记录excel表格中每一列对应的语言种类
def create_row_index(string_file_names) :
    row_index = {}

    row_index['name'] = 0
    row_index['values'] = 1
    ns = []  
    for name in sorted(string_file_names, key=str.lower) :
        #由于传入是完整的strings.xml路径，这里以文件夹作为列名如：values-ar/strings.xml 列名为ar
        #name = name.split('/')[-2][7:] 
        name = name.split('/')[-2]
        ns.append(name)
    for i in range(0, len(ns)) :
        row_index[ns[i]] = i + 1

    return row_index 

# 创建col索引，记录每一行的name
def create_col_index(app_path, app_dir, string_file_names):
    col_index = {}
    results = parse_xml(os.path.join(app_path, app_dir, TRANSLATE_PATH, string_file_names))
    num = 0
    for k,v in results.items():
        col_index[k] = num + 1
        num = num + 1
    return col_index 

def read_row_index(excel_path):
    workbook  = xlrd.open_workbook(excel_path)
    row_values = workbook.sheet_by_name(SHEET_NAMES[0]).row_values(0)
    row_values = [val.split(':')[-1] for val in row_values]
    row_index = {}
    for i in range(0, len(row_values)):
        row_index[row_values[i]] = i
    return row_index

def read_col_index(excel_path, sheet_name):
    sheet = xlrd.open_workbook(excel_path).sheet_by_name(sheet_name)
    col_values = sheet.col_values(0)
    col_index = collections.OrderedDict()
    for i in range(0, len(col_values)):
        col_index[col_values[i]] = i
    return col_index

# 初始化excel，创建3个表格分别对应三种情况
def init_excel(row_index) :
    workbook = xlwt.Workbook(encoding='utf-8')
    excels = SHEET_NAMES
    sheets = []
    for excel in excels:
        excel = workbook.add_sheet(excel)
        for k,v in row_index.items():
            if lans_dict.LANS_DICT.get(k) == None :
                print(k + " not exsits in lans_dict.py")
                excel.write(0, v, " :"+k)
            else :
                excel.write(0, v, lans_dict.LANS_DICT.get(k)+":"+k)
        sheets.append(excel)
    sheets.append(workbook)
    return sheets

# 由于每个表格包含的内容不同，抽离出来单独处理
def write_col_to_sheet(col_index, sheet):
    for k,v in col_index.items():
        sheet.write(v,0,k)

def prettyXml(element, indent='    ', newline='\n', level = 0): 
    if len(element):    
        if element.text == None or element.text.isspace():   
            element.text = newline + indent * (level + 1)      
        else:    
            element.text = newline + indent * (level + 1) + element.text.strip() + newline + indent * (level + 1)    
    temp = list(element) # 将elemnt转成list    
    for subelement in temp:    
        if temp.index(subelement) < (len(temp) - 1): # 如果不是list的最后一个元素，说明下一个行是同级别元素的起始，缩进应一致    
            subelement.tail = newline + indent * (level + 1)    
        else:  
            subelement.tail = newline + indent * level    
        prettyXml(subelement, indent, newline, level = level + 1) # 对子元素进行递归操作    


# data类型为字典，k为文件名，v为name与翻译对应的dict
def write_to_xml(data, output, xml_name="strings.xml"):
    output = createDir(output)
    for k,v in data.items():
        k = os.path.join(output, k)
        dir_path = createDir(k)
        if xml_name == 'strings.xml':
            xml = parse_dict_to_xmlstr(v)
        else:
            xml = parse_dict_to_xmlstr(v, {'translatable':'false'})
        if not xml == '':
            with open(os.path.join(dir_path, xml_name), 'wb') as f:
                f.write(b"<?xml version='1.0' encoding='utf-8'?>\n")
                f.write(xml)
                f.close()

# 将name与text的键值对转换为strings.xml的文本
def parse_dict_to_xmlstr(dict_data, attrib = {}):
    root = ET.Element('resources')
    for k,v in dict_data.items():
        attrib['name'] = k
        element = ET.SubElement(root,'string', attrib=attrib)
        element.text = v.replace("'","\\'")
    prettyXml(root, '    ','\n')
    if len(root.getchildren()) == 0:
        return ''
    return ET.tostring(root, encoding='utf-8', method='xml')
        

# 解析values对应的excel sheet
def parse_translate_values(row_index, col_index, excel_path):
    values_data = collections.OrderedDict()
    sheet = xlrd.open_workbook(excel_path).sheet_by_name(SHEET_NAMES[0])
    for rk,rv in row_index.items():
        # 跳过第一列
        if rv == 0:
            continue
        data = collections.OrderedDict()
        for ck,cv in col_index.items():
            # 跳过第一行
            if cv == 0:
                continue 
            data[ck] = sheet.cell_value(cv,rv)
        values_data[rk] = data
    return values_data

# 解析untranslate与will_translate对应的excel sheet
def parse_untranslate_values(col_index, excel_path, sheet_name):
    values_data = collections.OrderedDict()
    sheet = xlrd.open_workbook(excel_path).sheet_by_name(sheet_name)
    data = collections.OrderedDict()
    for k,v in col_index.items():
        if v == 0:
            continue
        data[k] = sheet.cell_value(v,1) 
    values_data['values'] = data
    return values_data

# 根据索引解析strings.xml文档，将翻译的内容写入对应的cell中
def write_to_excel(row_index, col_index, xml_file, sheet):
    data = parse_xml(xml_file)
    row_name = xml_file.split('/')[-2]
    row = row_index[row_name]
    for k,v in data.items():
        if k in col_index:
            sheet.write(col_index[k], row, v)
        else:
            print("""\"%s\" not translate completely""" % (k))

def mode_1(parser):
    '''
    将strings.xml转为excel
    '''
    app_path = parser.input_path
    app_dir = parser.app_dir
    output = parser.output
    
    if output == EXCEL_FILE_NAME:
        output = app_path.split('/')[-1]+":"+app_dir+".xls"

    path = os.path.join(app_path, app_dir, TRANSLATE_PATH)
    files_path,will_path = get_files_list(path)

    row_index = create_row_index(files_path)
    with open('dicts.py', 'wb') as f:
        jsonStr = json.dumps(row_index)
        f.write(jsonStr)
        f.close
    col_index = create_col_index(app_path, app_dir, STRING_FILE_NAME)

    translated_sheet,untranslated_sheet,willtranslate_sheet,workbook = init_excel(row_index)

    #开始处理translate sheet
#    en_file_path = os.path.join(app_path, app_dir, TRANSLATE_PATH, STRING_FILE_NAME) 
#    files_path.append(en_file_path)
    write_col_to_sheet(col_index, translated_sheet)
    for f in files_path:
        write_to_excel(row_index, col_index, f, translated_sheet)

    untranslated_path = os.path.join(app_path, app_dir, TRANSLATE_PATH, UNTRANSLATE_FILE_NAME) 
    if os.path.exists(untranslated_path):
        col_index = create_col_index(app_path, app_dir, UNTRANSLATE_FILE_NAME)
        write_col_to_sheet(col_index, untranslated_sheet)
        write_to_excel(row_index, col_index, untranslated_path, untranslated_sheet)

    '''
    willtranslate_path = os.path.join(app_path, app_dir, TRANSLATE_PATH, WILL_TRANSLATE_FILE_NAME) 
    if os.path.exists(willtranslate_path):
        col_index = create_col_index(app_path, app_dir, WILL_TRANSLATE_FILE_NAME)
        write_col_to_sheet(col_index, willtranslate_sheet)
        write_to_excel(row_index, col_index, willtranslate_path, willtranslate_sheet)
    '''
    willtranslate_path = os.path.join(app_path, app_dir, TRANSLATE_PATH, WILL_TRANSLATE_FILE_NAME) 
    if os.path.exists(willtranslate_path):
        col_index = create_col_index(app_path, app_dir, WILL_TRANSLATE_FILE_NAME)
        write_col_to_sheet(col_index, willtranslate_sheet)
        for f in will_path:
            write_to_excel(row_index, col_index, f, willtranslate_sheet)
    workbook.save(output)

def mode_2(parser):
    '''
    将excel解析为众多strings.xml
    '''
    excel_path = parser.input_path 
    output_dir = parser.output
    if output_dir == EXCEL_FILE_NAME:
        output_dir = excel_path.split('/')[-1].replace('.xls','')
    workbook = xlrd.open_workbook(excel_path)
    row_index = read_row_index(excel_path)
    sheet_name = workbook._sheet_names

    # 处理translate sheet的内容
    if SHEET_NAMES[0] in sheet_name:
        col_index = read_col_index(excel_path, SHEET_NAMES[0])
        data = parse_translate_values(row_index, col_index, excel_path) 
        write_to_xml(data, output_dir)
    else:
        print(SHEET_NAMES[0] , '不在excel中')
    
    # 处理untranslate的内容
    if SHEET_NAMES[1] in sheet_name:
        col_index = read_col_index(excel_path, SHEET_NAMES[1])
        data = parse_untranslate_values(col_index, excel_path, SHEET_NAMES[1] )
        write_to_xml(data, output_dir, xml_name='strings_untranslate.xml')
    else:
        print(SHEET_NAMES[1] , '不在excel中')
    
    # 处理will translate的内容
    if SHEET_NAMES[2] in sheet_name:
        col_index = read_col_index(excel_path, SHEET_NAMES[2])
        data = parse_untranslate_values(col_index, excel_path, SHEET_NAMES[2] )
        write_to_xml(data, output_dir, xml_name='strings_will_translate.xml')
    else:
        print(SHEET_NAMES[2] , '不在excel中')

def get_excel_file(excel_file_path):
    '''
    获取传参路径下的excel文件
    返回当前文件夹及其子目录下所有的excel文件(包括绝对路径)
    '''
    excel_type_list = [".xls", ".xlsx"]
    excel_list = []

    for root, dirs, files in os.walk(excel_file_path):
        for file in files:
            for excel_type in excel_type_list:
                if file.endswith(excel_type):
                    filename = root + "/" + file #注意不要改动"/"
                    excel_list.append(filename)
    return excel_list

if __name__ == '__main__':
    (parser,Args) = set_opt()

    if parser.mode == 1:
        mode_1(parser)
    else:
        if os.path.isdir(parser.input_path): #文件夹
            excel_file = get_excel_file(parser.input_path)
            for file_path in excel_file:
                print('file_path = ' , file_path)
                parser.input_path = file_path
                mode_2(parser)
        elif os.path.isfile(parser.input_path): #文件
            mode_2(parser)
        else:
            print ("请检查输入的路径是否存在")
