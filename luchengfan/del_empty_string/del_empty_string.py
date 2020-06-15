import xml.dom.minidom
import os

def del_empty_string(init_file):
    '''
    删除xml文件中的空元素，例如:
    <string name="COUNTRY_SG_LOCK_INFO_7" />
    " />
    '''
    input_file = open(init_file ,'r' , encoding="utf-8") #要处理的带@string字符的原始文件

    if is_dir:
        del_empty_str_file = 'output_file/' + init_file.split('/strings')[0]
    else:
        del_empty_str_file = 'output_file/'

    if not os.path.isdir(del_empty_str_file):
        os.makedirs(del_empty_str_file)

    output_file = open(del_empty_str_file + '/strings.xml' , 'w' , encoding="utf-8") #生成的中间文件，删除了原始文件中的空元素

    all_strings = input_file.readlines()
    for line in all_strings:
        if (r'" />' not in line):
            output_file.write(line)
    output_file.close()

def get_xml_file(xml_file_path):
    '''
    获取传参路径下的xml文件
    返回当前文件夹及其子目录下所有的xml文件(包括绝对路径)
    '''
    xml_type_list = [".xml"]
    xml_list = []

    for root, dirs, files in os.walk(xml_file_path):
        for file in files:
            for xml_type in xml_type_list:
                if file.endswith(xml_type):
                    filename = root + "/" + file #注意不要改动"/"
                    xml_list.append(filename)
    return xml_list


if __name__ == "__main__":
    init_xml_file = input('请输入处理的文件或文件夹：') 
    is_dir = False

    if os.path.isdir(init_xml_file): #文件夹
        is_dir = True
        xml_file = get_xml_file(init_xml_file)
        if len(xml_file) == 0:
            print ("当前路径下无xml文件")
            exit(0)
        for file_path in xml_file:
            del_empty_string(file_path)
    elif os.path.isfile(init_xml_file): #文件
        if not init_xml_file.endswith(".xml"):
            print ("请输入xml文件")
            exit(0)
        is_dir = False
        del_empty_string(init_xml_file)
    else:
        print ("请检查输入的路径是否存在")
