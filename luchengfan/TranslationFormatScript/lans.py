#!/usr/bin/python
#-*- coding:utf-8 -*-

'''
根据键值对的文件生成一个数组数据结构
或者将一个数组写为键值对行使的文件

最早使用与根据网上的文件名与语言对应的信息生成目前的dicts.py 
但目前在项目中没有使用到
'''
import sys
import dict

PATH = '/Users/leviming/Develop/scripts/lans.txt'

def get_dict():
    lans_dict = {}
    with open(PATH) as f:
        for line in f.readlines() :
            line = line.replace(' ','')
            line = line.strip(' \n')
            lan = line.split(":")
            lans_dict[lan[1]] = lan[0]
    return lans_dict

def write_dict(dict) :
    with open('dict.py', 'w') as f:
        for k,v in dict.items():
            f.write("'" + k + "':'"+v+"',\n")
        f.close()

#write_dict(get_dict())
print(dict.LANS_DICT['values-th-rTH'])
