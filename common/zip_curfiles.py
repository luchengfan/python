'''
压缩当前路径下的文件
'''

import os
import zipfile

def zip_files(target_path, zip_path):
    '''
    target_path：目标文件夹路径
    zip_path：压缩后的文件夹路径
    '''
    file_list = []
    zip = zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED)

    if os.path.isfile(target_path):
        file_list.append(target_path)
    else:
        for root, dirs, files in os.walk(target_path):
            file_path = root.replace(target_path, '')#不使用replace会从根目录开始复制
            file_path = file_path and file_path + os.sep or ''  # 实现当前文件夹以及包含的所有文件的压缩
            # 循环出一个个文件名
            for file in files:
                if file != zip_filename + ".zip":
                    zip.write(os.path.join(root, file), os.path.join(file_path, file))
        zip.close()
        print("压缩完成...")

if __name__ == "__main__":
    cur_path = os.getcwd()
    zip_filename = "zip_curpath_file"
    zipfilename_tmp = input("请输入压缩后的文件名(默认为：zip_curpath_file,直接回车则使用默认名)：")
    if (not zipfilename_tmp.isspace()) and (len(zipfilename_tmp) != 0):
        zip_filename = zipfilename_tmp

    zip_filepath = cur_path + "/" + zip_filename + ".zip"
    if os.path.exists(zip_filepath):
        print("文件已存在，请先删除原文件再执行压缩操作")
    else:
        zip_files(cur_path, zip_filepath)

