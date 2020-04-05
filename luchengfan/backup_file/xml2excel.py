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
    sPath = sPath + "   " + AddCountryName(sPath)
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

def AddCountryName(filename_strings):
    dict_Country={'am':'Armenian' , 'ar':'Arabic' , 'az':'Azerbaijani' , 'bg':'Bulgarian' , 'cs':'Czech',
                  'de':'German' , 'el':'Greek' , 'es':'Spaish' , 'fa':'Farsi' , 'fr':'French', 'hr':'Croatian',
                  'hu':'Hungarian' , 'in':'India' , 'it':'Italian' , 'iw':'Hebrew' , 'lt':'Lithuanian',
                  'lv':'Latvian' , 'mk':'Macedonian' , 'ms':'Montserrat' , 'nl':'Dutch' , 'pl':'Polish',
                  'pt':'Portuguese' , 'ro':'Romanian' , 'ru':'Russian' , 'sk':'Slovak' , 'sl':'Slovenian',
                  'sq':'Albanian' , 'sr':'Serbian' , 'th':'Thai' , 'tk':'Turkmen' , 'tr':'Turkish' , 'uk':'Ukrainian',
                  'ur':'Urdu' , 'uz':'Uzbekistan' , 'vi':'Vietnamese' , 'zh':'Chinese'}

    filename_strings.strip()
    countrylist = filename_strings.split(r'/')
    country_str = countrylist[1]
    if (country_str.find('-') >= 0):
        country_temp = country_str.split(r'-')
        countryshort = country_temp[1]
    else: #./values/strings.xml
        return "English"

    countryshort.lower()
    if (countryshort not in dict_Country.keys()):
        return ""
    else:
        for key,value in dict_Country.items():
            key.lower()
            if countryshort == key:
                return value

if ( __name__ == "__main__"):
    nColumn = 2
    parseXmlFirst('values/strings.xml','language.xls')
    for filename in iterfindfiles(r".", "strings.xml"):
        parseXmlOthers(filename,'language.xls',nColumn)
        nColumn = nColumn+1
        print 'tansform to excel:  ',filename


