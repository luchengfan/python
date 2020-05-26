# -*- coding: utf-8 -*-
"""
功能描述：将pdf文件转化为excel文件
请确保你在运行这个代码的时候，已经安装了pdfplumber库
如果没有安装，请在[附件-命令提示符]下输入：pip install pdfplumber
"""

import pdfplumber
import xlwt
import os

def is_empty(str):
    '''
    字符串是否为None或者为空
    '''
    if (str is None) or (str == ''):
        return True
    else:
        return False

def pdf_to_excel():
    # 定义保存Excel的位置
    workbook = xlwt.Workbook()  #定义workbook
    sheet = workbook.add_sheet('彩迅需求表')  #添加sheet
    # Excel起始位置
    i = 0

    pdf = pdfplumber.open(pdf_file)
    print('\n开始读取数据\n')

    for page in pdf.pages:
        for table in page.extract_tables():
            for row in table:
                for j in range(len(row)):
                    sheet.write(i, j, row[j])
                i += 1
    pdf.close()

    # 保存Excel表
    workbook.save('PDFresult.xls')
    print('\n写入excel成功')

if __name__ == '__main__':
    pdf_file = 'TK2005-105.pdf' #input("请输入需要转化的PDF文件：")

    if not os.path.isfile(pdf_file):
        print('文件不存在！！！')
    else:
        pdf_to_excel()