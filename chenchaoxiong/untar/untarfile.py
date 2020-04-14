#coding=utf-8
import requests
import sys
import tarfile
import os
import shutil
import hashlib

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

def md5_cal(bin_name):
    if os.path.isfile(bin_name):  
        fp=open(bin_name,'rb')  
        contents=fp.read()  
        fp.close()
        bin_name_md5 = hashlib.md5(contents).hexdigest()
        return(bin_name_md5)
    else:  
        print('file not exists')  

def file_name(file_dir):   
    for root, dirs, files in os.walk(file_dir):
        for ele in files: 
            temp_format = os.path.splitext(ele)[1]
            if (temp_format.lstrip(".") == "bin"): 
                return ele
        break

def modify_md5_file(md5_file):
    with open('MSD56_MD5.txt', "r+") as f:
        read_data = f.read()
        f.seek(0)
        f.truncate()   #清空文件
        f.write(md5_file)
        f.close

def make_targz(output_filename, source_dir):
  tar = tarfile.open(output_filename,"w")
  for root,dir,files in os.walk(source_dir):
    for file in files:
      pathfile = os.path.join(root, file)
      tar.add(pathfile,arcname=os.path.join(file))
  tar.close()

original_software = sys.argv[1]
un_tar(original_software)
un_tar_file_dir = original_software + "_files/"
software_xml = original_software+".xml"
have_change_logo=input("if you have use tool to change logo,please input:Y:")
if have_change_logo == "Y":
    new_software_ocs=input("input new ocs:")
    new_software_logo=input("input new logo name:")
    new_software_order_num=input("input new order number:")
    new_software_checksum=input("input new checksum:")
    software_xml_dir = os.getcwd() + "/" + software_xml
    software_xml_copy_dir = os.getcwd()+ "/"+ un_tar_file_dir + software_xml
    os.chdir(original_software + "_files/")
    #print (os.getcwd())
    binfile = file_name(os.getcwd())
    new_software_md5 = md5_cal(binfile)
    md5_file = new_software_md5 + "  " + binfile
    modify_md5_file(md5_file)
    original_software_array = original_software.split("_")
    original_software_len = (len(original_software_array))
    original_software_array[0]=new_software_ocs
    original_software_array[original_software_len-13]=new_software_logo
    original_software_array[original_software_len-12]=new_software_order_num
    original_software_array[original_software_len-3]=original_software_array[original_software_len-3]+ "_" + new_software_checksum
    new_software = "_".join(original_software_array)
    new_software_tar = new_software + ".tar"
    make_targz(new_software_tar,os.getcwd())
    os.chdir("../")
    new_software_xml = new_software + ".xml"
    new_software_xml_copy_dir = os.getcwd()+ "/"+ un_tar_file_dir + new_software_xml
    shutil.copy(software_xml_dir,new_software_xml_copy_dir)
else:
    print("please change the logo first!!")

