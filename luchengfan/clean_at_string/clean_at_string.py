import xml.dom.minidom

xml_file = 'strings.xml'
strings_del_empty = 'strings_del_empty.xml'

def del_empty_string():
    fo = open(strings_del_empty , 'w' , encoding="utf-8")
    fi = open(xml_file,'r', encoding="utf-8")
    content = fi.readlines()
    for line in content:
        line=line.replace('<item></item>','')
        fo.write(line)
    fo.close()


def clean_string():
    #打开xml文档
    dom = xml.dom.minidom.parse(strings_del_empty)
    #得到文档元素对象
    root = dom.documentElement
    strings = root.getElementsByTagName('string')
    items = root.getElementsByTagName('item')

    for i in range(len(strings)):
        print(strings[i].firstChild.data)
        if '@string/' in strings[i].firstChild.data:
            temp_string = strings[i].firstChild.data[8:]
            for j in range(len(strings)):
                if temp_string == strings[j].getAttribute('name'):
                    strings[i].firstChild.data = strings[j].firstChild.data

    for i in range(len(items)):
        if '@string/' in items[i].firstChild.data:
            temp_string = items[i].firstChild.data[8:]
            for j in range(len(strings)):
                if temp_string == strings[j].getAttribute('name'):
                    items[i].firstChild.data = strings[j].firstChild.data

    #修改并保存文件
    xml_specific = 'result.xml'
    with open(xml_specific , 'w' , encoding="utf-8") as f:
        dom.writexml(f)

if __name__ == "__main__":
    del_empty_string()
    clean_string()