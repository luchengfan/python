#!/usr/bin/env python
#-*- coding:utf-8 -*-
#############################
# @author: djming
# @email:dengjinming@cvte.com
#############################

import translate 
import os, sys
import json 
from srclist import SRC_LIST as srclist

#设置编码
reload(sys)
sys.setdefaultencoding("utf-8")

def file_is_exists(filename):
    return os.path.exists(filename)

# 遍历srclist中的目录寻找string文件
def get_files_list_with_list() :
    allstrfiles = set()
    for path in srclist :
        strfilepaths = translate.get_files_list(path)
        for strfilepath in strfilepaths:
            allstrfiles.add(strfilepath)
    return allstrfiles

def write_dict_to_file(data, filepath) :
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def parse_file_to_dict(filepath) :
    data = {}
    with open(filepath, 'r') as f:
        data = json.load(f, encoding='utf-8')

    return data 

if __name__ == '__main__' :
    allfiles = get_files_list_with_list()

    for fn in allfiles:
        print("\r\nparsing " + fn + "...")
        output = './translations/' + fn.split('/')[-2] + '.json'
        result = {}
        if file_is_exists(output):
            result = parse_file_to_dict(output)
        newdata = translate.parse_xml(fn)
        result = dict(newdata.items() + result.items())
        write_dict_to_file(result, output)
        print("successed")



