#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os

if __name__ == "__main__":
    SOC_filename = input('请输入日期SOC软件的文件名：')
    if '.bin' in SOC_filename:
        SOC_filename = SOC_filename.rstrip('.bin')

    xml_path = SOC_filename + '.xml'

    checksum_ymd = SOC_filename.split('_')[-2] #年、月、日
    checksum_hm = SOC_filename.split('_')[-1] #时、分
    checksum_date = checksum_ymd + '_' + checksum_hm

    if os.path.exists(xml_path):
        os.remove(xml_path)

    tcon_xml = open(xml_path , "w" , encoding='utf8')

    tcon_xml.write('<?xml version="1.0" encoding="utf-8"?>' + '\n')
    tcon_xml.write('<Root>' + '\n')
    tcon_xml.write(' '*4 + '<Confirmation>' + '\n')
    tcon_xml.write(' '*8 + '<SW_Items>' + '\n')
    tcon_xml.write(' '*12 + '<Attr Name="SW_CheckSum" Alias="SW_CheckSum" Ids="0" Atoms="' + checksum_date + '"/>' + '\n')
    tcon_xml.write(' '*12 + '<Attr Name="SW_DD_PCC" Alias="SW_DD_PCC" Ids="0" Atoms="NONE"/>' + '\n')
    tcon_xml.write(' '*8 + '</SW_Items>' + '\n')
    tcon_xml.write(' '*4 + '</Confirmation>' + '\n')
    tcon_xml.write('</Root>' + '\n')

    print('xml文件已生成，请查看' + xml_path + '文件')
