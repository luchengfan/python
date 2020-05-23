#!/usr/bin/python
# -*- coding: UTF-8 -*-

'''
功能说明：替换xml文件中的@string字符串。例如：
<string name="wifi_security_psk_generic">@string/wifi_security_wpa_wpa2</string>
则wifi_security_psk_generic的翻译同wifi_security_wpa_wpa2的翻译

init_xml_file：带@string字符的原始文件，即翻译中的strings.xml
del_empty_str_file：生成的中间文件，删除了原始文件中的空元素
remove_at_str_file：最终生成的文件
'''

import xml.dom.minidom
import os

del_empty_str_file = 'del_empty_str.xml'
remove_at_str_file = 'result.xml'

def del_empty_string(init_file):
    '''
    删除xml文件中的空元素，例如:
    <string name="empty" translatable="false"></string>
    <item></item>
    '''
    input_file = open(init_file ,'r' , encoding="utf-8") #要处理的带@string字符的原始文件
    output_file = open(del_empty_str_file , 'w' , encoding="utf-8") #生成的中间文件，删除了原始文件中的空元素

    all_strings = input_file.readlines()
    for line in all_strings:
        if ('<item></item>' not in line) and (r'"></string>' not in line):
            output_file.write(line)
    output_file.close()

def get_at_string_content(at_string):
    '''
    获取@string/后面的字符元素，例如：
    <string name="MODULATION_AUTO">@string/auto</string>
    则返回auto
    '''
    temp_string = at_string.split('@string/')[1] #得到：auto</string>
    content = temp_string.split('<')[0] #得到：auto
    return content

def get_string_value(string_content):
    '''
    通过temp_str获取到temp_str对应的翻译，例如temp_str为auto
    <string name="auto">Auto</string>
    则返回Auto
    备注：如果使用firstChild.data则需要删除掉xml中的空元素(即使用del_empty_string生成的文件)，否则会报data有Nonetype的错误
    '''
    dom = xml.dom.minidom.parse(del_empty_str_file) #打开xml文档
    root = dom.documentElement #得到文档元素对象
    strings = root.getElementsByTagName('string')

    for i in range(len(strings)):
        if string_content == strings[i].getAttribute('name'):
            return strings[i].firstChild.data

def replace_at_string():
    '''
    替换xml文件中的@string字符串
    '''
    open_del_empty_file = open(del_empty_str_file ,'r' , encoding="utf-8")
    result_file = open(remove_at_str_file , 'w' , encoding="utf-8")

    contents = open_del_empty_file.readlines()
    for strings in contents:
        if '@string/' in strings:
            str1 = get_at_string_content(strings) #获取@string/后面的字符元素
            str2 = get_string_value(str1) #获取@string/后面字符对应的翻译
            strings = strings.replace('@string/' + str1 , str2)
        result_file.write(strings)
    result_file.close()

if __name__ == "__main__":
    init_xml_file = input('请输入处理的xml文件：') 

    if not os.path.isfile(init_xml_file):
        print('文件不存在！！！')
    else:
        del_empty_string(init_xml_file)
        replace_at_string()
        print(del_empty_str_file , '为删除了原始文件中的空元素生成的文件')
        print('\n处理完成!请查看' , remove_at_str_file)
        print('\n请将{}和{}进行对比验证！'.format(init_xml_file , remove_at_str_file))