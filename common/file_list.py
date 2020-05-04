'''
功能描述：获取当前文件夹下所有文件名
'''
import os

def file_name(file_path):
    file_display = open(show_file, "wt", encoding="utf-8")
    file_hide = open(hide_fle, "wt", encoding="utf-8")

    file_display.write(file_path + "及其子目录下显示的文件:\n\n")
    file_hide.write(file_path + "及其子目录下隐藏的文件:\n\n")

    for root, dirs, files in os.walk(file_path):
        if "\." not in root: #隐藏的文件
            for name in files:
                file_display.write(os.path.join(root , name) + "\n")
            file_display.write("\n")
        else:
            for name in files:
                file_hide.write(os.path.join(root , name) + "\n")
            file_hide.write("\n")

    file_display.close()
    file_hide.close()

if __name__ == "__main__":
    show_file = "显示的文件列表.txt"
    hide_fle = "隐藏的文件列表.txt"

    path = input("请输入要查询的文件路径(默认为当前路径,直接回车则使用默认路径)：")
    if (not path.isspace()) and (len(path) != 0):
        file_name(path)
    else:
        file_name(os.getcwd())
    print("查询完成，请查看当前路径下的{}和{}文件".format(show_file , hide_fle))