#coding=utf-8
import requests
import sys
import tarfile
import os

def un_tar(file_name):
    """解压tar"""
    print(file_name)
    file_name_tar = file_name + ".tar"
    tar = tarfile.open(file_name_tar)
    names = tar.getnames()
    temp_file_path = ''
    if os.path.isdir(file_name + "_files"):
        print('文件已存在')
        temp_file_path = os.path.isdir(file_name + "_files")
    else:
        temp_file_path = os.mkdir(file_name + "_files")
        print('创建一个新的文件名')
    #因为解压后是很多文件，预先建立同名目录
    for name in names:
        tar.extract(name, file_name + "_files/")
    tar.close()
    return temp_file_path

original_software = sys.argv[1]
un_tar(original_software)
os.chdir(original_software + "_files/" )
#print (os.getcwd())
new_software_ocs=input("input new ocs:")
new_software_logo=input("input new logo name:")
new_software_checksum=input("input new checksum:")


