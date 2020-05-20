import xml.dom.minidom

def clean_string():
    xml_file = 'temp_strings.xml'

    #打开xml文档
    dom = xml.dom.minidom.parse(xml_file)
    #得到文档元素对象
    root = dom.documentElement
    strings = root.getElementsByTagName('string')

    for i in range(len(strings)):
        #xml_string[strings[i].getAttribute('name')] = strings[i].firstChild.data
        if '@string/' in strings[i].firstChild.data:
            temp_string = strings[i].firstChild.data[8:]
            for j in range(len(strings)):
                if temp_string == strings[j].getAttribute('name'):
                    strings[i].firstChild.data = strings[j].firstChild.data

    #修改并保存文件
    xml_specific = 'result.xml'
    with open(xml_specific , 'w' , encoding="utf-8") as f:
        dom.writexml(f)

if __name__ == "__main__":
    clean_string()