#!/usr/bin/python
# -*- coding: UTF-8 -*-

import xml.etree.ElementTree as ET
import xlrd
import sys
import os



def parseExcel(sPath):
	stringSheet = xlrd.open_workbook(sPath)
	table = stringSheet.sheet_by_name(u'languageTable')
	num_rows = table.nrows
	num_cols = table.ncols
	for coln in range(1,num_cols):
		stringDir = table.cell_value(0,coln)
		print 'insert to xml:  ',stringDir
		tree = ET.parse(stringDir)
		root = tree.getroot()
		for rown in range(1,num_rows):
			cell = table.cell_value(rown,coln)
			stringname = table.cell_value(rown,0)
	        for stringNode in root.findall('string'):
				name = stringNode.get('name')
				print('name = ' , name)
				if name == stringname:
					print('run to here')
					stringNode.text = cell
					tree.write(stringDir, encoding="utf-8",xml_declaration=True)
					
if ( __name__ == "__main__"):
    if len(sys.argv) < 2:
	print "Parameters error:python excel2xml.py input_excelfile"
	exit(1)
		
    excelfile = os.path.abspath(sys.argv[1])

    if ( not os.path.isfile(excelfile) ):
        print "excel file not exist ",excelfile
        exit(1)
    parseExcel(excelfile)

