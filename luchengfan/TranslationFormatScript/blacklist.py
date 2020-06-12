#!/usr/bin/env python
#-*- coding:utf-8 -*-
#############################
# @author: djming
# @email:dengjinming@cvte.com
#############################

'''
数组中的文件夹下的文件将被过滤
解析xml生成excel时不会解析这些文件夹下的xml
    'values',
'''

BLACK_LIST = [
    'values-1280x720',        
    'values-1920x1080',
    'values-xhdpi',
    'values-xxhdpi',
    'values-xxxhdpi',
    'values-hdpi'
]

