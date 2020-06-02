'''
功能描述：随机抽取excel表中的OCS ID
'''

import xlrd
import random
import webbrowser
import os
from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showinfo

def import_excel(excel_tables):
    '''
    打开excel表格，将excel表格内容导入到tables_list列表中
    '''
    for rown in range(excel_tables.nrows):
        array = {'ID':'','客户':'','软件工程师':'','客户确认状态':'','更新时间':'' }

        array['ID'] = str(excel_tables.cell_value(rown,1))[:6] #取前6位,去掉生成的.0
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
    random_number_list = [] #创建一个空列表，存储抽取到的数据
    excel_num = len(tables_list)
    get_id = random.randint(0 , excel_num - 1)

    if (len(random_number_list) != 0):
        while (get_id in random_number_list): #数据重复，重新抽取
            get_id = random.randint(0 , excel_num - 1)

    random_number_list.append(get_id)

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

def fileopen():
    '''
    打开文件
    '''
    v.set('') #清除文件内容
    excel_file = askopenfilename()
    if excel_file:
        v.set(excel_file)

def run():
    '''
    执行随机抽取OCS功能
    '''
    excel_file = v.get()
    choose_times = 0 #记录当前抽取的次数
    choose_total = 3 #设置一共需要抽取的次数

    if not os.path.isfile(excel_file):
        showinfo('提醒' , '文件不存在，请重新选择！')
        return
    else:
        if not (excel_file.endswith('.xlsx') or excel_file.endswith('.xls')):
            showinfo('提醒' , '非excel文件，请重新选择！')
            return

    data = xlrd.open_workbook(excel_file)
    sheet_table = data.sheets()[0] #读取excel表中的sheet1
    import_excel(sheet_table)  #将excel表格的内容导入到列表中

    if len(tables_list) == 0:
        showinfo('提醒' , '表格中没有数据，请重新选择！')
        return
    elif len(tables_list) < choose_total:
        choose_total = len(tables_list)

    while(choose_times < choose_total):
        choose_times += 1
        open_url()

if __name__ == '__main__':
    tables_list = []  #创建一个空列表，存储Excel的数据

    frameT = Tk()
    frameT.geometry('500x100+400+200')
    frameT.title('未关闭订单')
    frame = Frame(frameT)
    frame.pack(padx=10 , pady=10) #设置外边框
    frame1 = Frame(frameT)
    frame1.pack(padx=10 , pady=10) #设置外边框

    v = StringVar()

    ent = Entry(frame,width=50,textvariable=v).pack(fill=X,side=LEFT) #X方向填充，靠左
    btn = Button(frame,width=20,text='选择文件',font=('宋体',14),command=fileopen).pack(fill=X,padx=10)
    ext = Button(frame1,width=10,text='运行',font=('宋体',14),command=run).pack(fill=X,side=LEFT)
    etb = Button(frame1,width=10,text='退出',font=('宋体',14),command=frameT.quit).pack(fill=Y,padx=10)
    frameT.mainloop()
