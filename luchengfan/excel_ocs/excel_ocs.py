'''
功能描述：随机抽取excel表中的OCS ID
'''

import xlrd
import random
import webbrowser
import os

tables_list = []  #创建一个空列表，存储Excel的数据

#将excel表格内容导入到tables_list列表中
def import_excel(excel_tables):
    '''
    打开excel表格，处理相关的数据
    '''
    for rown in range(excel_tables.nrows):
        array = {'ID':'','客户':'','软件工程师':'','客户确认状态':'','更新时间':'' }

        array['ID'] = str(excel_tables.cell_value(rown,1))[:6] #取前6位去掉生成的.0
        array['客户'] = excel_tables.cell_value(rown,2)
        array['软件工程师'] = excel_tables.cell_value(rown,3)
        array['客户确认状态'] = excel_tables.cell_value(rown,5)
        array['更新时间'] = excel_tables.cell_value(rown,10)
        tables_list.append(array)

    tables_list.pop(0) #删掉第一列的数据

def get_ocsid():
    '''
    在tables_list列表中随机抽取一个ID
    '''
    excel_num = len(tables_list)
    get_id = random.randint(0 , excel_num - 1)
    return get_id

def open_url():
    '''
    通过抽取到的ID打开对应的OCS链接
    '''
    get_id_info = get_ocsid()
    print('抽取到的信息为：' , tables_list[get_id_info])
    get_ocs_id = tables_list[get_id_info]['ID'] #获取具体的OCS ID
    url_link = 'http://ocs.gz.cvte.cn/tv/Tasks/view/range:my/' + get_ocs_id
    webbrowser.open_new_tab(url_link)

if __name__ == '__main__':
    excel_file = '未关闭订单.xlsx'

    if not os.path.isfile(excel_file):
        print('文件不存在！！！')
        exit(0)

    choose_times = 0

    data = xlrd.open_workbook(excel_file)
    sheet_table = data.sheets()[0] #读取excel表中的sheet1
    import_excel(sheet_table)  #将excel表格的内容导入到列表中

    while(choose_times < 3):
        choose_times += 1
        open_url()
