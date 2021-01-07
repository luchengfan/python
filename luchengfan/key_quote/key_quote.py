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

def get_assessed_name(excel_tables):
    '''
    被评价的姓名，并返回列表
    '''
    assessed_name_list = []
    total_people = get_assessed_number(excel_tables)

    for num in range(total_people):
        assessed_name_list.append(excel_tables.cell_value(2 , num*4))

    return assessed_name_list

def dict_self_assessment(excel_tables):
    '''
    获取自评的结果并按照各个维度写入字典中
    '''
    #清空字典中的值
    dict_self_requirement.clear()
    dict_self_satisfaction.clear()
    dict_self_assist.clear()
    dict_self_improve.clear()

    num = 0
    self_assessment_list = []
    total_people = get_assessed_number(excel_tables)
    dic_answerer_rown = get_answerer_rown(excel_tables)
    answerer_name = get_answerer_name(excel_tables)

    for num in range(total_people):
        assessment_name = excel_tables.cell_value(2 , num*4)
        if assessment_name in answerer_name:
            answerer_rown_num = int(dict_to_str(dic_answerer_rown[assessment_name]))

            dict_self_requirement[assessment_name] = result_check(excel_tables.cell_value(answerer_rown_num , num*4))
            dict_self_satisfaction[assessment_name] = result_check(excel_tables.cell_value(answerer_rown_num , num*4 + 1))
            dict_self_assist[assessment_name] = result_check(excel_tables.cell_value(answerer_rown_num , num*4 + 2))
            dict_self_improve[assessment_name] = result_check(excel_tables.cell_value(answerer_rown_num , num*4 + 3))

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
        return dict_to_str(dict_self_requirement[name])
    elif key_dime == '满意度':
        return dict_to_str(dict_self_satisfaction[name])
    elif key_dime == '协作与及时性':
        return dict_to_str(dict_self_assist[name])
    elif key_dime == '问题改善与推动':
        return dict_to_str(dict_self_improve[name])
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
    result_level = ''

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
    
    if str_A_num != 0:
        result_level += str(str_A_num) + 'A  '
    if str_B_num != 0:
        result_level += str(str_B_num) + 'B  '
    if str_C_num != 0:
        result_level += str(str_C_num) + 'C  '
    if str_D_num != 0:
        result_level += str(str_D_num) + 'D  '

    return result_level

def others_evaluation(excel_tables):
    '''
    获取他评的结果，并写入各个字典中
    excel_tables：数据来源的表格
    '''
    dict_others_requirement.clear()
    dict_others_satisfaction.clear()
    dict_others_assist.clear()
    dict_others_improve.clear()

    total_people = get_assessed_number(excel_tables) #被评价的人数

    dic_answerer_rown = get_answerer_rown(excel_tables)
    answerer_name = get_answerer_name(excel_tables)

    for num in range(total_people):
        others_name = excel_tables.cell_value(2 , num*4)
        dict_others_requirement[others_name] = result_statistics(excel_tables , others_name , num*4 , '需求确认')
        dict_others_satisfaction[others_name] = result_statistics(excel_tables , others_name , num*4 + 1 , '满意度')
        dict_others_assist[others_name] = result_statistics(excel_tables , others_name , num*4 + 2 , '协作与及时性')
        dict_others_improve[others_name] = result_statistics(excel_tables , others_name , num*4 + 3 , '问题改善与推动')

def save_to_excel(excel_tables):
    #关键举证输出的文件
    output_file = "关键举证.xls"

    styleRedBkg = xlwt.easyxf('pattern: pattern solid, fore_colour red;')  # 红色

    others_evaluation(excel_tables) #他评
    assessed_name = get_assessed_name(excel_tables)
    answerer_department = get_answerer(excel_tables)

    if os.path.exists(output_file):
        os.remove(output_file)

    style =  xlwt.XFStyle()   #赋值style为XFStyle()，初始化样式    

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
    
    for j in range(len(assessed_name)):
        name = assessed_name[j]
        if name in answerer_department.keys():
            sheet_key_quote.write(j+2 , 0 , dict_to_str(answerer_department[name]).strip("'"))

        sheet_key_quote.write(j+2 , 1 , assessed_name[j])

        #自评
        if name in dict_self_requirement.keys():
            sheet_key_quote.write(j+2 , 2 , dict_self_requirement[name])
        else:
            sheet_key_quote.write(j+2 , 2 , '未自评' , styleRedBkg)

        if name in dict_self_satisfaction.keys():
            sheet_key_quote.write(j+2 , 5 , dict_self_satisfaction[name])
        else:
            sheet_key_quote.write(j+2 , 5 , '未自评' , styleRedBkg)

        if name in dict_self_assist.keys():
            sheet_key_quote.write(j+2 , 8 , dict_self_assist[name])
        else:
            sheet_key_quote.write(j+2 , 8 , '未自评' , styleRedBkg)

        if name in dict_self_improve.keys():
            sheet_key_quote.write(j+2 , 11 , dict_self_improve[name])
        else:
            sheet_key_quote.write(j+2 , 11 , '未自评' , styleRedBkg)

        #他评
        if name in dict_others_requirement.keys():
            sheet_key_quote.write(j+2 , 3 , dict_others_requirement[name])
        if name in dict_others_satisfaction.keys():
            sheet_key_quote.write(j+2 , 6 , dict_others_satisfaction[name])
        if name in dict_others_assist.keys():
            sheet_key_quote.write(j+2 , 9 , dict_others_assist[name])
        if name in dict_others_improve.keys():
            sheet_key_quote.write(j+2 , 12 , dict_others_improve[name])

    wb.save(output_file)
    tip_message = '关键举证数据已生成，请查看' + output_file + '文件'
    showinfo(title='提示', message=tip_message)
    frameT.quit()

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
    #创建自评各个维度的字典
    dict_self_requirement = {} #自评需求确认
    dict_self_satisfaction = {} #自评满意度
    dict_self_assist = {} #自评协作与及时性
    dict_self_improve = {} #自评问题改善与推动

    #创建他评各个维度的字典
    dict_others_requirement = {} #他评需求确认
    dict_others_satisfaction = {} #他评满意度
    dict_others_assist = {} #他评协作与及时性
    dict_others_improve = {} #他评问题改善与推动

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
