#!/usr/bin/python
# -*- coding: UTF-8 -*-

import xml.etree.ElementTree as ET
import xlrd
import xlwt

import os
import fnmatch

def parseXmlFirst(sPath,dPath):
    tree = ET.parse(sPath)
    root = tree.getroot()
    excel = xlwt.Workbook()
    sheet = excel.add_sheet('languageTable',cell_overwrite_ok=True)
    row = 0;
    column = 0
	#Write country name 
    sheet.write(row,column+1,sPath)
    row = row+1
	
    for stringName in root.findall('string'):
        name = stringName.get('name')
        text = stringName.text
        sheet.write(row,column,name)
        sheet.write(row,column+1,text)
        row = row+1
    excel.save(dPath)

def parseXmlOthers(sPath,dPath,nColumn):
    excel = xlwt.Workbook()
    sheet = excel.add_sheet('languageTable',cell_overwrite_ok=True)
    workbook = xlrd.open_workbook(dPath)
    table = workbook.sheet_by_name(u'languageTable')
    nrows = table.nrows
    tree = ET.parse(sPath)
    root = tree.getroot()
    #Copy all excel data
    num_rows = table.nrows
    num_cols = table.ncols
    for rown in range(num_rows):
        for coln in range(num_cols):
            cell = table.cell_value(rown,coln)
            sheet.write(rown,coln,cell)
    #Write country name
    sheet.write(0,nColumn,sPath)

    for stringName in root.findall('string'):
        name = stringName.get('name')
        text = stringName.text
        for rownum in range(nrows):
            xlsName =  table.cell_value(rownum,0)
            if (name == xlsName):
                sheet.write(rownum,nColumn,text)
    excel.save(dPath)
 
def iterfindfiles(path, fnexp):
    for root, dirs, files in os.walk(path):
        for filename in fnmatch.filter(files, fnexp):
            yield os.path.join(root, filename)

if ( __name__ == "__main__"):
    nColumn = 2
    parseXmlFirst('values/strings.xml','language.xls')
    for filename in iterfindfiles(r".", "strings.xml"):
        parseXmlOthers(filename,'language.xls',nColumn)
        nColumn = nColumn+1
        print 'tansform to excel:  ',filename


