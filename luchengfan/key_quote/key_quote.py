#!/usr/bin/python
# -*- coding: UTF-8 -*-

'''
此功能是将问卷中的关键举证按照整合分为自评和他评并按照特定的格式输出到新的excel中，方便评估确定
'''
import xlrd
import xlwt
import os
from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showinfo

def result_check(result):
    '''
    建议自评和他评的结果：1、去掉空格；2、全部转化为大写；3、如果输入了多个字母则提示报错
    ''' 
    result_str = result.strip().upper()
    result_range = ['A' , 'B' , 'C' , 'D']

    if (len(result_str) == 1):
        if result_str in result_range:
            return result_str
        else:
            showinfo(title='提示', message='填写的值不在范围内，请检查！')
            return 0
    else:
        showinfo(title='提示', message='结果输入错误，请检查！')
        return 0

def get_answerer_name(excel_tables):
    '''
    获取答题人的姓名，即Excel中的'答题人'
    '''
    answerer_list = []

    for rown in range(4 , excel_tables.nrows):
        answerer = excel_tables.cell_value(rown,excel_tables.ncols - 4)
        answerer_list.append(answerer)
    
    return answerer_list

def get_answerer(excel_tables):
    '''
    获取答题人信息，包括'答题人'以及'答卷者部门'
    '''
    dict_answerer = {}

    for rown in range(4 , excel_tables.nrows):
        answerer = excel_tables.cell_value(rown,excel_tables.ncols - 4)
        answerer_department = excel_tables.cell_value(rown,excel_tables.ncols - 2).split('-')[-1]
        dict_answerer[answerer] = {answerer_department}
    
    return dict_answerer

def get_answerer_rown(excel_tables):
    '''
    获取答题人在Excel所在的行
    '''
    dict_answerer_rown = {}

    for rown in range(4 , excel_tables.nrows):
        answerer = excel_tables.cell_value(rown,excel_tables.ncols - 4)
        dict_answerer_rown[answerer] = {rown}
    
    return dict_answerer_rown

def get_assessed_number(excel_tables):
    '''
    被评价的人数
    '''
    total_ncols = excel_tables.ncols #总共的列
    return int((total_ncols - 5)/4)

def get_appraise_number(excel_tables):
    '''
    评价的人数，即有多少人参与了评价
    '''
    total_nrows = excel_tables.nrows #总共的行
    return (total_nrows - 4)

def dict_to_str(dict_str):
    return str(dict_str).strip('{').strip('}')

def dict_self_assessment(excel_tables):
    '''
    获取自评的结果并按照各个维度写入字典中
    '''
    #清空字典中的值
    dict_requirement.clear()
    dict_satisfaction.clear()
    dict_assist.clear()
    dict_improve.clear()

    num = 0
    self_assessment_list = []
    total_people = get_assessed_number(excel_tables)
    dic_answerer_rown = get_answerer_rown(excel_tables)
    answerer_name = get_answerer_name(excel_tables)

    for num in range(total_people):
        assessment_name = excel_tables.cell_value(2 , num*4)
        if assessment_name in answerer_name:
            answerer_rown_num = int(dict_to_str(dic_answerer_rown[assessment_name]))

            dict_requirement[assessment_name] = result_check(excel_tables.cell_value(answerer_rown_num , num*4))
            dict_satisfaction[assessment_name] = result_check(excel_tables.cell_value(answerer_rown_num , num*4 + 1))
            dict_assist[assessment_name] = result_check(excel_tables.cell_value(answerer_rown_num , num*4 + 2))
            dict_improve[assessment_name] = result_check(excel_tables.cell_value(answerer_rown_num , num*4 + 3))

def self_assessment(excel_tables , name , key_dime):
    '''
    获取自评的结果
    excel_tables：数据来源的表格
    name:需要获取自评的人员
    key_dime：获取自评的维度，包括'需求确认','满意度','协作与及时性','问题改善与推动'
    '''
    answerer_name = get_answerer_name(excel_tables)

    if name not in answerer_name:
        return 0

    if key_dime == '需求确认':
        return dict_to_str(dict_requirement[name])
    elif key_dime == '满意度':
        return dict_to_str(dict_satisfaction[name])
    elif key_dime == '协作与及时性':
        return dict_to_str(dict_assist[name])
    elif key_dime == '问题改善与推动':
        return dict_to_str(dict_improve[name])
    else:
        return 0

def result_statistics(excel_tables , name , result_num , key_dime):
    '''
    获取他评的等级的结果
    excel_tables：数据来源的表格
    result_num：当前查询结果的人员
    key_dime：获取自评的维度，包括'需求确认','满意度','协作与及时性','问题改善与推动'
    '''
    appraise_num = get_appraise_number(excel_tables) #评价的人数
    self_assessment_level = self_assessment(excel_tables , name , key_dime)

    str_A_num = 0
    str_B_num = 0
    str_C_num = 0
    str_D_num = 0

    for i in range(appraise_num):
        get_result_level = result_check(excel_tables.cell_value(i + 4 , result_num))
        if get_result_level == 'A':
            str_A_num += 1
        elif get_result_level == 'B':
            str_B_num += 1
        elif get_result_level == 'C':
            str_C_num += 1
        elif get_result_level == 'D':
            str_D_num += 1

    if self_assessment_level == 'A':
        str_A_num -= 1
    elif self_assessment_level == 'B':
        str_B_num -= 1
    elif self_assessment_level == 'C':
        str_C_num -= 1
    elif self_assessment_level == 'D':
        str_D_num -= 1
    
    result_level = str(str_A_num) + 'A, ' + str(str_B_num) + 'B, ' + str(str_C_num) + 'C, ' + str(str_D_num) + 'D'
    return result_level

def others_evaluation(excel_tables):
    '''
    获取他评的结果
    excel_tables：数据来源的表格
    '''
    #get_result_num = 0
    others_evaluation_list = []
    total_people = get_assessed_number(excel_tables) #被评价的人数

    dic_answerer_rown = get_answerer_rown(excel_tables)
    answerer_name = get_answerer_name(excel_tables)

    for num in range(total_people):
        array = {'被评价者':'','需求确认':'','满意度':'','协作与及时性':'','问题改善与推动':'' }
        array['被评价者'] = excel_tables.cell_value(2 , num*4)
        array['需求确认'] = result_statistics(excel_tables , array['被评价者'] , num*4 , '需求确认')
        array['满意度'] = result_statistics(excel_tables , array['被评价者'] , num*4 + 1 , '满意度')
        array['协作与及时性'] = result_statistics(excel_tables , array['被评价者'] , num*4 + 2 , '协作与及时性')
        array['问题改善与推动'] = result_statistics(excel_tables , array['被评价者'] , num*4 + 3 , '问题改善与推动')
        others_evaluation_list.append(array)
    
    return others_evaluation_list

def save_to_excel(excel_tables):
    #关键举证输出的文件
    output_file = "关键举证.xls"

    if os.path.exists(output_file):
        os.remove(output_file)

    style =  xlwt.XFStyle()   #赋值style为XFStyle()，初始化样式    

    others_evaluation_result_list = others_evaluation(excel_tables)

    #设置居中
    al = xlwt.Alignment()
    al.horz = 0x02      # 设置水平居中
    al.vert = 0x01      # 设置垂直居中
    style.alignment = al

    pattern =xlwt.Pattern()   # 创建一个模式
    pattern.pattern =  xlwt.Pattern.SOLID_PATTERN # 设置其模式为实型
    pattern.pattern_fore_colour = 0x33
    style.pattern = pattern  # 将赋值好的模式参数导入Style

    wb = xlwt.Workbook() #创建工作簿
    sheet_key_quote = wb.add_sheet(u'关键举证') #创建sheet
    sheet_key_quote.write_merge(0,1,0,0,'战队',style) #将第0行到第1行和第0列到第0列合并
    sheet_key_quote.write_merge(0,1,1,1,'姓名',style) #将第0行到第1行和第1列到第1列合并
    sheet_key_quote.write_merge(0,0,2,4,'需求确认',style)
    sheet_key_quote.write_merge(0,0,5,7,'满意度',style)
    sheet_key_quote.write_merge(0,0,8,10,'协作&及时性',style)
    sheet_key_quote.write_merge(0,0,11,13,'问题改善与推动',style)
    for i in range(4):
        sheet_key_quote.write_merge(1,1,i*3 + 2,i*3 + 2,'自评',style)
        sheet_key_quote.write_merge(1,1,i*3 + 3,i*3 + 3,'他评',style)
        sheet_key_quote.write_merge(1,1,i*3 + 4,i*3 + 4,'最终评级',style)
    
    wb.save(output_file)

def get_key_quote():
    '''
    获取关键举证的数据
    '''
    excel_file = file_text.get()
    data = xlrd.open_workbook(excel_file)
    sheet_table = data.sheets()[0] #读取excel表中的sheet1

    dict_self_assessment(sheet_table)
    save_to_excel(sheet_table)


def fileopen():
    '''
    打开文件
    '''
    file_text.set('') #清除文件内容
    excel_file = askopenfilename()
    if excel_file:
        file_text.set(excel_file)

if __name__ == "__main__":
    #创建各个维度的字典
    dict_requirement = {} #需求确认
    dict_satisfaction = {} #满意度
    dict_assist = {} #协作与及时性
    dict_improve = {} #问题改善与推动

    #可视化界面
    frameT = Tk()
    frameT.geometry('500x100+400+200')
    frameT.title('关键举证')
    frame = Frame(frameT)
    frame.pack(padx=10 , pady=10) #设置外边框
    frame1 = Frame(frameT)
    frame1.pack(padx=10 , pady=10) #设置外边框

    file_text = StringVar()

    ent = Entry(frame,width=50,textvariable=file_text).pack(fill=X,side=LEFT) #X方向填充，靠左
    btn = Button(frame,width=20,text='选择文件',font=('宋体',14),command=fileopen).pack(fill=X,padx=10)
    ext = Button(frame1,width=10,text='开始',font=('宋体',14),command=get_key_quote).pack(fill=X,side=LEFT)
    etb = Button(frame1,width=10,text='退出',font=('宋体',14),command=frameT.quit).pack(fill=Y,padx=10)
    frameT.mainloop()
