# encoding: GBK
import datetime
import re
from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT, WD_ROW_HEIGHT_RULE
from docx.shared import Cm, Pt, Inches
import difflib
from docx.shared import Pt
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn
from openpyxl import load_workbook
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT, WD_UNDERLINE
from collections import defaultdict
import os
from djcp.utils import insert_Scheme_confirmation_page
from crm import settings


def add_column_at01(table, new_column_index, column_with):
    """
在指定列插入空白列
    @param table: doc中表格
    @param new_column_index:在第二列加：开始值是0，如果想在第二列插，就写1
    @param column_with:插入行款，Cm(2)
    @return:
    """
    if new_column_index >= len(table.columns):
        return table.add_column(column_with)

    tbl_grid = table._tbl.tblGrid
    grid_col = tbl_grid.add_gridCol()
    grid_col.w = column_with
    tbl_grid.insert(new_column_index, grid_col)
    for tr in table._tbl.tr_lst:
        tc = tr.add_tc()
        tc.width = column_with
        real_tcs = []
        for tc_index, tc_obj in enumerate(tr):
            if tc_obj.__class__.__name__ == "CT_Tc":
                real_tcs.append({
                    "tc": tc_obj,
                    "index": tc_index,
                })
        tr.insert(real_tcs[new_column_index]["index"], tc)
    return table.columns[new_column_index]


def add_column_at(table, new_column_index, column_with):
    """
在指定列插入空白列
    @param table: doc中表格
    @param new_column_index:在第二列加：开始值是0，如果想在第二列插，就写1
    @param column_with:插入行款，Cm(2)
    @return:
    """
    if new_column_index >= len(table.columns):
        return table.add_column(column_with)
    for tr in table._tbl.tr_lst:
        real_tcs = []
        for tc_index, tc_obj in enumerate(tr):
            real_tcs.append({
                "tc": tc_obj,
                "index": tc_index,
            })
        tc = tr.add_tc()
        tc.width = column_with
        tr.insert(new_column_index + 1, tc)
    return table.columns[new_column_index + 1]


def insert_objecte(doc, sheetnum):
    """
插入一列到word中在表头写上"测评对象编号"
    :param doc:
    """
    table = doc.tables[sheetnum]
    # col = table.columns[3]  # 定位列
    # col_cells = table.add_column(Cm(2)).cells  # 在word表格最后一行加入一列
    col_cells = add_column_at01(table, 1, Cm(2)).cells
    cell = col_cells[0]
    cell.text = '测评对象编号'
    p = cell.paragraphs[0]
    p.paragraph_format.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    p.runs[0].bold = True
    p.runs[0].font.size = Pt(10.5)
    # bg = parse_xml(r'<w:shd{nsdecls("w")} w:fill="888888"/>')
    bg = parse_xml(r'<w:shd {} w:fill="{color_value}"/>'.format(nsdecls('w'), color_value='#A6A6A6'))
    cell._tc.get_or_add_tcPr().append(bg)
    return table


def insert_number(doc, C, index_wordlist, excel_list2, index_excellist, cellmax, sheetnum):
    '''插入编号的方法'''
    table = insert_objecte(doc, sheetnum)
    cols = len(table.columns)
    dd = defaultdict(list)
    for k, va in [(v, i) for i, v in enumerate(index_excellist)]:
        dd[k].append(va)
    dd = dict(dd)
    for k, v in dd.items():
        # print('k:{},v:{}'.format(k,v))
        if len(v) == 1:
            run = table.cell(index_wordlist[v[0]], 1).paragraphs[0].add_run(
                'LISS-' + excel_list2[index_excellist[v[0]]] + '-001')
            run.font.name = '华文仿宋'
            run.font.size = Pt(10.5)

        else:
            for index, value in enumerate(v):
                if index < 9:
                    run = table.cell(index_wordlist[value], 1).paragraphs[0].add_run(
                        'LISS-' + excel_list2[index_excellist[value]] + '-00' + str(index + 1))
                    run.font.name = '华文仿宋'
                    run.font.size = Pt(10.5)
                elif index < 99:
                    run = table.cell(index_wordlist[value], 1).paragraphs[0].add_run(
                        'LISS-' + excel_list2[index_excellist[value]] + '-0' + str(index + 1))
                    run.font.name = '华文仿宋'
                    run.font.size = Pt(10.5)
                else:
                    run = table.cell(index_wordlist[value], 1).paragraphs[0].add_run(
                        'LISS-' + excel_list2[index_excellist[value]] + '-' + str(index + 1))
                    run.font.name = '华文仿宋'
                    run.font.size = Pt(10.5)

    for k, v in enumerate(C):
        if k < 9:
            run = table.cell(v, 1).paragraphs[0].add_run('LISS-' + cellmax + '-00' + str(k + 1))
            run.font.name = '华文仿宋'
            run.font.size = Pt(10.5)
        elif k < 99:
            run = table.cell(v, 1).paragraphs[0].add_run('LISS-' + cellmax + '-0' + str(k + 1))
            run.font.name = '华文仿宋'
            run.font.size = Pt(10.5)
        else:
            run = table.cell(v, 1).paragraphs[0].add_run('LISS-' + cellmax + '-' + str(k + 1))
            run.font.name = '华文仿宋'
            run.font.size = Pt(10.5)


def find_sameorDiff_Number(index_list, index_wordlist):
    A = set(index_list).intersection(set(index_wordlist))  # 交集
    B = set(index_list).union(set(index_wordlist))  # 并集
    C = set(index_list).difference(set(index_wordlist))  # 差集，在list1中但不在list2中的元素
    D = set(index_wordlist).difference(set(index_list))  # 差集，在list2中但不在list1中的元素
    # print("交集元素个数:" + str(len(A)))
    # print("并集元素个数:" + str(len(B)))
    # print("在list1中但不在list2中的元素个数:", C)
    # print("在list2中但不在list1中的元素个数:" + str(len(D)))
    C = list(C)
    return A, B, C, D


def mate(excel_list1, word_list2):
    index_wordlist = []
    excelnew_list = []
    index_excellist = []
    index_list = []
    for index, item in enumerate(word_list2):
        index = index + 1
        index_list.append(index)
        for index_excel, j in enumerate(excel_list1):

            seq = difflib.SequenceMatcher(None, item, j)
            ratio = seq.ratio()
            if ratio > 0.2:
                index_wordlist.append(index)
                excelnew_list.append(j)
                index_excellist.append(index_excel)
                # print('excel索引：', index_excel)

    return index_wordlist, excelnew_list, index_excellist, index_list


def read_word(doc, sheetnum):
    """
读取word中的数据
    :param doc:
    :return:word表格第二列的数据
    """
    table = doc.tables[sheetnum]
    rows = len(table.rows)  # 获取最大行数
    word_list2 = []
    for row in range(1, rows):
        col = table.cell(row, 1).text
        word_list2.append(col)
    return word_list2


def read_excel(wb):
    """
读取excel中的数据
    :param wb: excel工作簿
    :return: excel表格第一列的数据列表
    """
    ws = wb.active
    rowmax = ws.max_row
    colmax = ws.max_column
    cellmax = ws.cell(rowmax, colmax).value
    excel_list1 = []
    excel_list2 = []
    for row in range(1, ws.max_row + 1):
        value1 = ws.cell(row, 1).value
        value2 = ws.cell(row, 2).value
        excel_list1.append(value1)
        excel_list2.append(value2)

    return excel_list1, excel_list2, cellmax


def excel_col2data(wb, index_excellist):
    ws = wb.active
    for index_excel in index_excellist:
        print(index_excel)


def management_system():
    """
机房、安全相关人员、安全管理制度等只有一个编号的处理函数
    """
    word_list2 = read_word(doc, sheetnum)
    excel_list1, excel_list2, cellmax = read_excel(wb)
    t = len(word_list2)
    table = insert_objecte(doc, sheetnum)
    cols = len(table.columns)
    for k, v in enumerate(word_list2):
        if k < 9:
            run = table.cell(k + 1, 1).paragraphs[0].add_run('LISS-' + cellmax + '-00' + str(k + 1))
            run.font.name = '华文仿宋'
            run.font.size = Pt(10.5)
        else:
            run = table.cell(k + 1, 1).paragraphs[0].add_run('LISS-' + cellmax + '-0' + str(k + 1))
            run.font.name = '华文仿宋'
            run.font.size = Pt(10.5)


def network_equipment():
    """
网络设备的处理函数，因为在云上的系统无网络设备，所以网络设备这个表格需要单独拉出来。
    """
    word_list2 = read_word(doc, sheetnum)
    if '本报告不涉及' in word_list2:
        table = insert_objecte(doc, sheetnum)
        cols = len(table.columns)
        table.cell(1, 0).merge(table.cell(1, cols - 1))
    elif len(word_list2) == 0:
        table = insert_objecte(doc, sheetnum)
        cols = len(table.columns)
        for i in range(1):  # 模板中已经有一行了，所以总共只需增加len(supplier)行
            table.add_row()
        table.cell(1, 0).merge(table.cell(1, cols - 1))  # 合并单元格
        run = table.cell(1, 0).paragraphs[0].add_run('本系统不涉及')
        run.font.name = '华文仿宋'
        run.font.size = Pt(10.5)
        table.cell(1, 0).paragraphs[0].alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    else:
        start_up()


def insert_row(doc):
    """
在列数只有一列的表格后面插入一列加上“本系统不涉及”居中对齐
    :param doc: 测评方案用户接收
    """
    tbs = doc.tables
    for tb in tbs:
        if len(tb.rows) == 1:
            tb.add_row()
            cols = len(tb.columns)
            tb.cell(1, 0).merge(tb.cell(1, cols - 1))  # 合并单元格
            run = tb.cell(1, 0).paragraphs[0].add_run('本系统不涉及')
            run.font.name = '华文仿宋'
            run.font.size = Pt(10.5)
            tb.cell(1, 0).paragraphs[0].alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
        elif len(tb.rows) == 2 and tb.cell(1, 0).text == '':
            cols = len(tb.columns)
            tb.cell(1, 0).merge(tb.cell(1, cols - 1))  # 合并单元格
            run = tb.cell(1, 0).paragraphs[0].add_run('本系统不涉及')
            run.font.name = '华文仿宋'
            run.font.size = Pt(10.5)
            tb.cell(1, 0).paragraphs[0].alignment = WD_PARAGRAPH_ALIGNMENT.CENTER


def replace_para(doc, old_text, newtext):
    """
“测评中心”替换成“测评机构”
    :param doc: 测评方案用户接收
    :param old_text: 测评中心
    :param newtext: 测评机构
    """
    for p in doc.paragraphs:
        if old_text in p.text:
            inline = p.runs
            for i in inline:

                if old_text in i.text:
                    text = i.text.replace(str(old_text), str(newtext))
                    i.text = text


def start_up():
    word_list2 = read_word(doc, sheetnum)
    excel_list1, excel_list2, cellmax = read_excel(wb)
    index_wordlist, excelnew_list, index_excellist, index_list = mate(excel_list1, word_list2)
    A, B, C, D = find_sameorDiff_Number(index_list, index_wordlist)
    insert_number(doc, C, index_wordlist, excel_list2, index_excellist, cellmax, sheetnum)


def get_parindex(doc):
    """
为了定位“测评方法”的具体位置，找到对应的paragraph.
    :param doc:
    :return:
    """
    paragraphs = list(doc.paragraphs)
    # print(len(paragraphs))
    for i in range(len(paragraphs)):
        paragraph = paragraphs[i]
        if '测评方法' == paragraph.text:
            return i


def getpara_wordcontent(i):
    """
将测评方法内容插入到word中(插入段落)
    """

    paragraphs = list(doc.paragraphs)
    paragraphslist = get_doc01_con()

    for par in doc.paragraphs:
        if '测评方法' == par.text:
            par = paragraphs[i + 1]
            for parh in paragraphslist:
                par.insert_paragraph_before(parh)


def get_doc01_con():
    """
获取doc01（测评方法）文档里面的所有文字数据
    :return:
    """
    paragraphslist = []
    for para in doc01.paragraphs:
        p = para.text
        paragraphslist.append(p)
    return paragraphslist


def getpara_wordcontent02():
    """
将测评依据内容插入到word中(插入段落)
    """

    '''定位内容'''
    restr_start = '等级保护测评工作流程图'
    pos_start = get_position(restr_start)
    # doc.paragraphs[pos_start - 2].clear()  # 删除指定段落

    standard_str_start = doc.paragraphs[pos_start + 1].text  # 测评依据的定位位置
    restr_end = '被测等级保护对象情况'
    pos_end = get_position(restr_end)
    standard_str_end = doc.paragraphs[pos_end].text  # 测评依据的定位位置
    print('开始：{},内容：{}，结束：{},内容：{}'.format(pos_start + 1, standard_str_start, pos_end, standard_str_end))

    '''删除内容'''
    parlist = []  # 删除指定段落
    for i in range(pos_start + 2, pos_end):
        paragraph = doc.paragraphs[i]
        print('需要删除的内容为', paragraph.text)
        parlist.append(paragraph)

    for j in range(len(parlist)):
        delete_paragraph(parlist[j])

    '''插入内容'''
    paragraphslist = []
    for para in standard_doc.paragraphs:
        p = para.text
        paragraphslist.append(p)

    paragraphs = list(doc.paragraphs)

    for parh in paragraphslist:  # 插入内容
        paragraphs[pos_start + 2].insert_paragraph_before(parh)


def delete_paragraph(paragraph):
    '''删除指定段落'''
    p = paragraph._element
    p.getparent().remove(p)
    paragraph._p = paragraph._element = None


def get_standard_con():
    """
获取standard_doc（测评依据）文档里面的所有文字数据
    :return:
    """
    paragraphslist = []
    for para in standard_doc.paragraphs:
        p = para.text
        paragraphslist.append(p)
    return paragraphslist


def get_position(restr):
    '''
    通过字符串进行定位
    @param restr:
    @return:
    '''
    pos = 0
    for i in range(len(doc.paragraphs)):
        matchRet = re.findall(restr, doc.paragraphs[i].text)
        if len(matchRet) > 0:
            pos = i
    return pos


def getday(y=2017, m=8, d=15, n=0):
    '''
    获取指定日期的前几天和后几天日期
    @param y: 年
    @param m: 月
    @param d: 日
    @param n: +5：后5天，-5前5天
    @return:
    '''
    the_date = datetime.datetime(y, m, d)
    result_date = the_date + datetime.timedelta(days=n)
    d = result_date.strftime('%Y-%m-%d')
    return d


def time_content():
    '''
    获得测评方案的时间插入到表内容
    封面和表一内容
    @return:
    '''
    '''定位，找出测评方案所在位置'''
    year_location = '\d{4}[\.\/年-]{,3}'
    month_location = "\d{1,2}[\.\/月-]{,3}"
    day_location = "\d{1,2}[\.\/日-]{,3}"
    casestr = ''
    for i in range(len(doc.paragraphs)):
        mm = re.findall(r"{}年{}月{}日～{}月{}日，方案编制过程。".format(year_location, month_location, day_location, month_location,
                                                           day_location, ), doc.paragraphs[i].text)

        if len(mm) > 0:
            casestr = mm[0]

    case_year = casestr[0:4]  # 拿到测评方案的年
    case_mon = casestr[12:14]  # 拿到测评方案的月和日
    case_day = casestr[15:17]  # 拿到测评方案的日

    '''封面使用'''
    case_time_face = case_year + '年' + case_mon + '月' + case_day + '日' + ' ' * 30  # 给封面用
    print(case_time_face)
    tb = doc.tables[0]
    para = tb.cell(3, 1).paragraphs[0]
    para.text = para.text.replace(para.text, case_time_face)
    para.runs[0].bold = True
    para.runs[0].font.size = Pt(16)
    para.runs[0].underline = WD_UNDERLINE.THICK

    '''表一使用'''
    case_year = int(case_year)
    case_mon = int(case_mon)
    case_day = int(case_day)
    organization_time = getday(case_year, case_mon, case_day, -1)
    auditd_time = getday(case_year, case_mon, case_day, 0)
    doc.tables[1].rows[5].cells[0].tables[0].rows[6].cells[4].text = organization_time  # 编制日期
    doc.tables[1].rows[5].cells[0].tables[0].rows[6].cells[4].paragraphs[0].runs[0].font.size = Pt(10.5)
    doc.tables[1].rows[5].cells[0].tables[0].rows[6].cells[4].paragraphs[
        0].paragraph_format.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER

    doc.tables[1].rows[5].cells[0].tables[0].rows[7].cells[4].text = auditd_time  # 审核日期
    doc.tables[1].rows[5].cells[0].tables[0].rows[7].cells[4].paragraphs[0].runs[0].font.size = Pt(10.5)
    doc.tables[1].rows[5].cells[0].tables[0].rows[7].cells[4].paragraphs[
        0].paragraph_format.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER

    doc.tables[1].rows[5].cells[0].tables[0].rows[8].cells[4].text = auditd_time  # 批准日期
    doc.tables[1].rows[5].cells[0].tables[0].rows[8].cells[4].paragraphs[0].runs[0].font.size = Pt(10.5)
    doc.tables[1].rows[5].cells[0].tables[0].rows[8].cells[4].paragraphs[
        0].paragraph_format.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER


def finalstart_up(paths_case):
    """
最终处理程序
    :param paths_case: 用户传经来的原始的测评方案
    """
    global doc, sheetnum, wb, doc01, table, standard_doc

    paths_excel = settings.ASSET_NUM
    path_word01 = settings.EVA_METHOD  # 测评方法路径
    path_word02 = settings.CASE_SIGN  # 方案签字路径
    standard_path = settings.STANDARD_PATH  # 方案依据路径
    doc01 = Document(path_word01)  # 测评方法的doc
    standard_doc = Document(standard_path)  # 测评依据的doc
    doc_target = Document(path_word02)
    # paragraph_target = doc_target.paragraphs[0]
    table = doc_target.tables[0]
    path = paths_case
    doc = Document(path)
    i = get_parindex(doc)
    getpara_wordcontent(i)  # 将测评方法内容插入到word中(插入段落)
    getpara_wordcontent02()  # 测评过程中主要参考的标准
    for name in os.listdir(paths_excel):
        if name == '01机房.xlsx':
            path_excel = paths_excel + '/' + name
            wb = load_workbook(path_excel)
            sheetnum = 3
            management_system()

        elif name == '02网络设备.xlsx':
            path_excel = paths_excel + '/' + name
            wb = load_workbook(path_excel)
            sheetnum = 4
            network_equipment()
        elif name == '03安全设备.xlsx':
            path_excel = paths_excel + '/' + name
            wb = load_workbook(path_excel)
            sheetnum = 5
            start_up()
        elif name == '04服务器存储设备.xlsx':
            path_excel = paths_excel + '/' + name
            wb = load_workbook(path_excel)
            sheetnum = 6
            start_up()
        elif name == '05终端设备.xlsx':
            path_excel = paths_excel + '/' + name
            wb = load_workbook(path_excel)
            sheetnum = 7
            start_up()
        elif name == '06系统管理软件平台.xlsx':
            path_excel = paths_excel + '/' + name
            wb = load_workbook(path_excel)
            sheetnum = 8
            start_up()
        elif name == '07业务应用软件平台.xlsx':
            path_excel = paths_excel + '/' + name
            wb = load_workbook(path_excel)
            sheetnum = 9
            start_up()
        elif name == '08安全相关人员.xlsx':
            path_excel = paths_excel + '/' + name
            wb = load_workbook(path_excel)
            sheetnum = 11
            management_system()
        elif name == '09安全管理文档.xlsx':
            path_excel = paths_excel + '/' + name
            wb = load_workbook(path_excel)
            sheetnum = 12
            management_system()
    insert_row(doc)
    caselist = {'6.': '6.0', '测评中心': '测评机构', '网络安全等级测评方案': '网络安全等级保护测评方案和计划'}
    for k, v in caselist.items():
        replace_para(doc, k, v)
    # insert_Scheme_confirmation_page.getsheet_wordcontent(doc)
    table01 = doc.tables[0]
    a = table01.cell(1, 1).text
    '''删除指定段落的内容'''
    insert_Scheme_confirmation_page.del_parcontent(doc)  # 其中，2022年07月12日召开了项目启动会议，确定了工作方案及项目人员名单；2022年07月23日召开了项
    '''插入测评方案签字确认页面'''
    insert_Scheme_confirmation_page.insert_table_after_text(doc, table)
    table.cell(0, 1).text = a
    for r, row in enumerate(table.rows):  # 遍历表格的行
        for c, cell in enumerate(row.cells):  # 遍历每一行的列
            cell1 = (r, c)  # 在单元格里写入当前的位置（表格、行、列）
            if cell1 == (0, 1):
                p = cell.paragraphs[0]
                p.runs[0].bold = False
                p.runs[0].font.size = Pt(14)
    try:
        time_content()
    except:
        print('异常')

    temp = path.split('/')
    temp1 = temp[-1]
    temp2 = temp1.split('_')

    output_filename = temp2[0] + '_' + temp2[1] + '_' + temp2[2] + '和计划'
    output_case_path = os.path.join(settings.CASE_OUTPUT_PATH, '{}.docx'.format(output_filename))
    doc.save(output_case_path)
    print('{}.docx处理【完成】'.format(output_filename))
    return output_filename


if __name__ == '__main__':
    path = 'caseUpload/LISS2020DJCP060_历峰集团电商平台_测评方案_20220901134536258（李海燕）.docx'
    path1 = 'caseUpload/LISS2022DJCP031_理财登记过户平台_测评方案_20220830124455139李海燕_rLNiWOK.docx'
    path3 = 'caseUpload/LISS2022DJCP068_杨浦区证证联办场景引导平台_测评方案_20220901134454287（李海燕）.docx'
    path4 = 'caseUpload/LISS2022DJCP060_杨浦区政府网站群_测评方案_20220901134615994（李海燕）.docx'
    paths_case = os.path.join(settings.MEDIA_ROOT, path4)
    paths_case = re.sub('\\\\', '/', paths_case)  # 路径符号转换
    finalstart_up(paths_case)

    # get_case_time(paths_case)
