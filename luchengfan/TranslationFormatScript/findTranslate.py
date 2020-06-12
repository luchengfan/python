#!/usr/bin/env python
#-*- coding:utf-8 -*-
#############################
# @author: djming
# @email:dengjinming@cvte.com
#############################


import os, sys
import re
from libs.prettytable import PrettyTable
from lans_dict import LANS_DICT as lans
from generate_dict import parse_file_to_dict
from optparse import OptionParser 

reload(sys)
sys.setdefaultencoding("utf-8")

def set_opt():
    parser = OptionParser()
    parser.add_option('-l', '--libdir', help='翻译库的文件夹路径，默认为当前文件夹下的translations中', action='store', type='string', default=os.path.join(os.getcwd(), 'translations'))
    parser.add_option('-s', '--slice', help='设置每一行显示的翻译语言种类，默认每行显示4种翻译,可在进入程序后通过输入set slice 设置,-1为单行显示', action='store', type='int', default=4)
    parser.add_option('-f', '--fuzzy', help='设置是否启用模糊查询，默认启用，可在进入程序后通过set fuzzy 进行更改', action='store', type='string', default='true')
    return parser.parse_args()

def getfiles(path):
    files = set()
    for fn in os.listdir(path):
        if fn.startswith('values') and fn.endswith('json'):
            files.add(os.path.join(path, fn))

    return files

def fuzzyfinder(user_input, collection):
    suggestions = []
    pattern = '.*?'.join(user_input.lower())    
    regex = re.compile(pattern)         
    for item in collection:
        match = regex.search(item.lower())      
        if match:
            suggestions.append((len(match.group()), match.start(), item))
    return [x for _, _, x in sorted(suggestions)]

def find_data(k):
    values = dctns.values()
    result = []
    for v in values:
        value = v.get(k)
        if not value : value = ""
        result.append(value)

    return [k] + result

def printTableSplice(header, table, num=-1):
    nums = len(header) - 1  # 总长度，不计算key位
    if num == -1 : num = nums

    for start in range(1, nums, num):
        h = [headers[0]] + headers[start:start+num]
        pt = PrettyTable(h)
        for data in table:
            pt.add_row([data[0]] + data[start:start+num])

        print(pt)


    print('\r\n\r\n\r\n\r\n Query finished')


if __name__ == '__main__':
    parser, Args = set_opt()
    libdir = parser.libdir 
    splice = parser.slice
    fuzzy = parser.fuzzy
    if Args:
        name = Args[0]
    print("loading dictionaries...")
    global dctns
    dctns = {}
    index = []
    for fn in getfiles(libdir) :
        dctn = parse_file_to_dict(fn)
        lan = fn.split('/')[-1].replace('.json','')
        lan = lans.get(lan, lan)
        if lan == "英语":
            index = dctn
        dctns[lan] = dctn
        print("load " + lan + " success")

    print("start success: slice : " + str(splice) + " fuzzy query : " + fuzzy)

    print('''
            set slice ${slice}
                        设置每一行显示的翻译语言种类，默认每
                        行显示4种翻译

            set fuzzy ${ture/false}
                        设置是否启用模糊查询，默认启用
            ''')

    global headers
    headers = ["keyword"] + dctns.keys()
    while True:
        keyword = raw_input("input keyword(ctrl+c for quit):")

        if keyword.startswith('set slice'):
            splice = int(keyword.split(' ')[-1])
            continue

        if keyword.startswith('set fuzzy'):
            fuzzy = str(keyword.split(' ')[-1])
            continue

        if not keyword : continue

        if fuzzy == 'true':
            keys = fuzzyfinder(keyword, index)
        else:
            keys = [keyword]

        results = []
        for k in keys:
            results.append(find_data(k))

        printTableSplice(headers, results, splice)
