#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os

if __name__ == "__main__":
    CheckSum_date = input('请输入日期(例如:20201222_1421)：')
    xml_path = 'output_tcon_xml.xml'

    if os.path.exists(xml_path):
        os.remove(xml_path)

    tcon_xml = open(xml_path , "w" , encoding='utf8')

    tcon_xml.write('<?xml version="1.0" encoding="utf-8"?>' + '\n')
    tcon_xml.write('<Root>' + '\n')
    tcon_xml.write(' '*4 + '<Confirmation>' + '\n')
    tcon_xml.write(' '*8 + '<SW_Items>' + '\n')
    tcon_xml.write(' '*12 + '<Attr Name="SW_CheckSum" Alias="SW_CheckSum" Ids="0" Atoms="' + CheckSum_date + '"/>' + '\n')
    tcon_xml.write(' '*12 + '<Attr Name="SW_DD_PCC" Alias="SW_DD_PCC" Ids="0" Atoms="NONE"/>' + '\n')
    tcon_xml.write(' '*8 + '</SW_Items>' + '\n')
    tcon_xml.write(' '*4 + '</Confirmation>' + '\n')
    tcon_xml.write('</Root>' + '\n')

    print('xml文件已生成，请查看' + xml_path + '文件')
