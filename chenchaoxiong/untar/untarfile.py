#coding=utf-8
import requests
import sys
import tarfile
import os

def un_tar(file_name):
    """解压tar"""
    #print(file_name)
    file_name_tar = file_name + ".tar"
    tar = tarfile.open(file_name_tar)
    names = tar.getnames()
    temp_file_path = ''
    if os.path.isdir(file_name + "_files"):
        #print('file exists')
        temp_file_path = os.path.isdir(file_name + "_files")
    else:
        temp_file_path = os.mkdir(file_name + "_files")
        #print('creat a new file dir')
    #因为解压后是很多文件，预先建立同名目录
    for name in names:
        tar.extract(name, file_name + "_files/")
    tar.close()
    return temp_file_path

def file_name(file_dir):   
    for root, dirs, files in os.walk(file_dir):
        for ele in files: 
            temp_format = os.path.splitext(ele)[1]
            if (temp_format.lstrip(".") == "bin"): 
                return ele
        break
original_software = sys.argv[1]
un_tar(original_software)

have_change_logo=input("if you have use tool to change logo,please input:Y:")
if have_change_logo == "Y":
new_software_ocs=input("input new ocs:")
new_software_logo=input("input new logo name:")
new_software_checksum=input("input new checksum:")

    os.chdir(original_software + "_files/")
    #print (os.getcwd())
    binfile = file_name(os.getcwd())
else:
    print("please change the logo first!!")

