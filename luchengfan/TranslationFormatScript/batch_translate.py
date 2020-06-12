#!/usr/bin/python
#-*- coding:utf-8 -*-

import xlrd,xlwt
from optparse import OptionParser
import os,sys
import traceback

CONFIG = 'config.txt'
DEFAULT_SHEET_NAME = ('translate', 'untranslate', 'willtranslate')
DOWNLOADER = os.path.join(sys.path[0], 'translate.py')

def set_opt():
    parser = OptionParser()
    parser.add_option('-m', '--mode', help='set translate mode ,default is 1 for read config.txt and output excels, 2 for read excel and output xmls', dest='mode', action='store', type='int', default=1)
    parser.add_option('-c', '--config', help="set config path, default is './config.txt'",dest='config_path', action='store', type='str', default=CONFIG)
    parser.add_option('-i', '--input', help="set excel path, defalut is translate.xls",dest='input', action='store', type='str', default='translate.xls')
    parser.add_option('-o','--output',help="set output dir path, default is ./output/",dest='output', action='store', type='str', default='output')
    return parser.parse_args()

def parse_config(config):
    with open(config, 'r') as f:
        projs = [val.replace(' ','').strip() for val in f.readlines() if not val.replace(' ','').startswith('#') and not val.strip()=='']
        f.close()
    return projs

def init_new_excel():
    workbook = xlwt.Workbook(encoding='utf-8')
    workbook.add_sheet(DEFAULT_SHEET_NAME[0])
    workbook.add_sheet(DEFAULT_SHEET_NAME[1])
    workbook.add_sheet(DEFAULT_SHEET_NAME[2])
    return workbook

'''
将多个excel文档拼接成一个文件，每个文件的条目之间由文件名分割
方便将多个项目的需要翻译的语言一起导出交给翻译公司
'''
def splice_excels(excels, new_excel,sheet_name):
    """
        Args:
            excels:字典，结构为{表格名：表格}
            new_excel:workbook，用于保存所有内容的excel
            sheet_name：指定合并哪一个表，目前有DEFAULT_SHEET_NAME中的三种
    """
    current_row = 0 # 当前行
    row_length = 0
    for excel_name,excel in excels.items():
        new_excel.get_sheet(sheet_name).write(current_row,0, excel_name)
        if current_row == 0:    #第一行写入语言索引
            sheet = excel.sheet_by_index(0)
            lans = sheet.row_values(0)[0:]
            row_length = len(lans)
            for i in range(1,row_length):
                new_excel.get_sheet(sheet_name).write(current_row, i, lans[i])

        current_row = current_row + 1
        new_sheet = new_excel.get_sheet(sheet_name)
        sheet = excel.sheet_by_name(sheet_name)
        col_length = len(sheet.col_values(0)[0:])
        for i in range(1, col_length):
            for j in range(0, row_length):
                new_sheet.write(current_row, j, sheet.cell_value(i,j))
            current_row = current_row + 1
    new_excel.save(output+'.xls')

"""
根据总表的格式解析出其中每个项目的条目所在行
"""
def get_split_index(excel):
    """
    Args:
        excel: String, 总表的名称
    Returns:
        index:字典，格式为:
                            {
                                sheet_name:String:{项目名称:String:[内容开始行:Int， 内容结束行:Int]}
                            }
    """
    workbook = xlrd.open_workbook(excel)
    index = {}
    last_sheet_name = ''
    for sheet_name in workbook.sheet_names():
        sheet  = workbook.sheet_by_name(sheet_name)
        col_values = sheet.col_values(1)
        sheet_index = {}
        sheet_index[sheet.cell_value(0,0)] = [0,0]
        # 第一个项目总是从第一排开始
        last_sheet_name = sheet.cell_value(0,0)
        for i in range(0, len(col_values)):
            if col_values[i] == '': # 若第二列内容为空则表示这一行是项目分割行
                sheet_index[last_sheet_name][1] = i #记录上一个项目的开始行
                sheet_index[sheet.cell_value(i,0)] = [0,0]
                sheet_index[sheet.cell_value(i,0)][0]=i #记录新项目的结束行
                last_sheet_name = sheet.cell_value(i,0) #记录新项目的名称

        sheet_index[last_sheet_name][1] = len(col_values)   #最后一个项目在最后一行结束 无法通过循环判断
        index[sheet_name] = sheet_index
    return index


"""
根据项目分割excel总表为不同的表，方便调用脚本处理
"""
def split_excel(excel,output_dir):
    if not os.path.exists(output_dir):os.mkdir(output_dir)
    excels = []
    index = get_split_index(excel)
    from_workbook = xlrd.open_workbook(excel)
    excel_names = index[DEFAULT_SHEET_NAME[0]].keys()
    for excel_name in excel_names:
        workbook = xlwt.Workbook(encoding='utf-8')
        for k,v in index.items():
            from_sheet = from_workbook.sheet_by_name(k)
            sheet = workbook.add_sheet(k)
            copy_row(from_sheet, sheet, 0, 0)
            start_row = v[excel_name][0]+1
            end_row = v[excel_name][1]
            current_row = 1
            for i in range(start_row, end_row):
                copy_row(from_sheet, sheet, i, current_row)
                current_row = current_row + 1
        excel = os.path.join(output_dir, excel_name+'.xls')
        excels.append(excel)
        workbook.save(excel)
    return excels


def copy_row(from_sheet, to_sheet, from_row, to_row):
    values = from_sheet.row_values(from_row)
    for i in range(0,len(values)):
        to_sheet.write(to_row, i, values[i])
    

if __name__ == "__main__":
    try:
        (parser, Args) = set_opt()
        if parser.mode == 1:    #xml转excel
            config_path = parser.config_path
            output = parser.output
            #if not os.path.exists(output): os.mkdir(output)
            projs = parse_config(config_path)
            for proj in projs:
                proj = proj.split(":")
                if len(proj) == 1:proj.append("app")
                os.system('python '+DOWNLOADER+' -i '+proj[0] + ' -a ' + proj[1])
            projs = [val.split('/')[-1] for val in projs]
            excels = {}
            for proj in projs:
                excels[proj] = xlrd.open_workbook(proj+'.xls')
            workbook = init_new_excel()
            splice_excels(excels,workbook,DEFAULT_SHEET_NAME[0])
            splice_excels(excels,workbook,DEFAULT_SHEET_NAME[1])
            splice_excels(excels,workbook,DEFAULT_SHEET_NAME[2])
        elif parser.mode == 2:  #excel转xml
            excel = parser.input
            output_dir = parser.output
            excels = split_excel(excel,output_dir)
            for excel in excels:
                os.system('python '+DOWNLOADER+' -m 2 -i '+excel)

        sys.exit(0)
    except Exception, e:
        sys.exit(1)
