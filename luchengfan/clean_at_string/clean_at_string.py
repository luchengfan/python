#!/usr/bin/python
# -*- coding: UTF-8 -*-

'''
功能说明：替换xml文件中的@string字符串。例如：
<string name="wifi_security_psk_generic">@string/wifi_security_wpa_wpa2</string>
则wifi_security_psk_generic的翻译同wifi_security_wpa_wpa2的翻译

xml_file：原始文件，即翻译中的strings.xml
strings_del_empty：生成的中间文件没删除了空元素
xml_remove_at_string：最终生成的文件
'''

import xml.dom.minidom

xml_file = 'strings.xml'
strings_del_empty = 'strings_del_empty.xml'
xml_remove_at_string = 'result.xml'

def del_empty_string():
    '''
    删除xml文件中的空元素，例如:
    <string name="empty" translatable="false"></string>
    <item></item>
    '''
    input_file = open(xml_file ,'r' , encoding="utf-8")
    del_empty_string_file = open(strings_del_empty , 'w' , encoding="utf-8")

    strings = input_file.readlines()
    for line in strings:
        if ('<item></item>' not in line) and (r'"></string>' not in line):
            del_empty_string_file.write(line)
    del_empty_string_file.close()

def get_at_string_value(temp_string):
    '''
    获取@string/后面的字符元素，例如：
    <string name="MODULATION_AUTO">@string/auto</string>
    则返回auto
    '''
    string1 = temp_string.split('@string/')[1]
    string2 = string1.split('<')[0]
    return string2

def get_string_value(temp_str):
    '''
    通过temp_str获取到temp_str对应的翻译，例如temp_str为auto
    <string name="auto">Auto</string>
    则返回Auto
    备注：如果使用firstChild.data则需要删除掉xml中的空元素(即使用del_empty_string生成的文件)，否则会报data有Nonetype的错误
    '''
    #打开xml文档
    dom = xml.dom.minidom.parse(strings_del_empty)
    #得到文档元素对象
    root = dom.documentElement
    strings = root.getElementsByTagName('string')

    for i in range(len(strings)):
        if temp_str == strings[i].getAttribute('name'):
            return strings[i].firstChild.data

def del_at_string():
    '''
    替换xml文件中的@string字符串
    '''
    open_del_empty_file = open(strings_del_empty ,'r' , encoding="utf-8")
    result_file = open(xml_remove_at_string , 'w' , encoding="utf-8")

    content = open_del_empty_file.readlines()
    for strings in content:
        if '@string/' in strings:
            str1 = get_at_string_value(strings)
            str2 = get_string_value(str1)
            strings = strings.replace('@string/' + str1 , str2)
        result_file.write(strings)
    result_file.close()

if __name__ == "__main__":
    del_at_string()