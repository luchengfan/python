'''
功能描述：随机抽取excel表中的OCS ID
'''

import xlrd
import random
import webbrowser

tables_list = []  #创建一个空列表，存储Excel的数据

#将excel表格内容导入到tables_list列表中
def import_excel(excel_tables):
    for rown in range(excel_tables.nrows):
        array = {'ID':'','customer':'','sw_engineer':'','confirm_status':'','upfate_time':'' }

        array['ID'] = excel_tables.cell_value(rown,1)
        array['customer'] = excel_tables.cell_value(rown,2)
        array['sw_engineer'] = excel_tables.cell_value(rown,3)
        array['confirm_status'] = excel_tables.cell_value(rown,5)
        array['upfate_time'] = excel_tables.cell_value(rown,10)
        tables_list.append(array)

    tables_list.pop(0) #删掉第一列的数据

def get_ocsid():
    excel_num = len(tables_list)
    get_id = random.randint(0 , excel_num - 1)
    return get_id

def open_url():
    get_id_info = get_ocsid()
    get_ocs_id = int(tables_list[get_id_info]['ID'])
    url_link = 'http://ocs.gz.cvte.cn/tv/Tasks/view/range:my/' + str(get_ocs_id)
    webbrowser.open_new_tab(url_link)

if __name__ == '__main__':
    excel_file = '未关闭订单.xlsx'
    data = xlrd.open_workbook(excel_file)
    sheet_table = data.sheets()[0]
    import_excel(sheet_table)  #将excel表格的内容导入到列表中

    open_url()
