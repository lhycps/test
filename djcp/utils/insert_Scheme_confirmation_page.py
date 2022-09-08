# encoding: GBK
import re

from docx import Document
from docx.shared import Inches
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.shared import Pt
from copy import deepcopy
from docx.oxml.xmlchemy import OxmlElement
from docx.oxml.ns import qn


def copy_table_after(table, paragraph):
    tbl, p = table._tbl, paragraph._p
    new_tbl = deepcopy(tbl)
    p.addnext(new_tbl)
    return tbl, p


def move_table_after(table, paragraph):
    tbl, p = table._tbl, paragraph._p
    p.addnext(tbl)


# 设置表格的边框
def set_cell_border(cell, **kwargs):
    """
    Set cell`s border
    Usage:
    set_cell_border(
        cell,
        top={"sz": 12, "val": "single", "color": "#FF0000", "space": "0"},
        bottom={"sz": 12, "color": "#00FF00", "val": "single"},
        left={"sz": 24, "val": "dashed", "shadow": "true"},
        right={"sz": 12, "val": "dashed"},
    )
    """
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()

    # check for tag existnace, if none found, then create one
    tcBorders = tcPr.first_child_found_in("w:tcBorders")
    if tcBorders is None:
        tcBorders = OxmlElement('w:tcBorders')
        tcPr.append(tcBorders)

    # list over all available tags
    for edge in ('left', 'top', 'right', 'bottom', 'insideH', 'insideV'):
        edge_data = kwargs.get(edge)
        if edge_data:
            tag = 'w:{}'.format(edge)
            # check for tag existnace, if none found, then create one
            element = tcBorders.find(qn(tag))
            if element is None:
                element = OxmlElement(tag)
                tcBorders.append(element)

            # looks like order of attributes is important
            for key in ["sz", "val", "color", "space", "shadow"]:
                if key in edge_data:
                    element.set(qn('w:{}'.format(key)), str(edge_data[key]))


def inser_page(doc):
    paragraphs = list(doc.paragraphs)
    for i in range(len(paragraphs)):
        if i == 15:
            par1 = doc.paragraphs[i].insert_paragraph_before('被测单位方案确认签字页\n')
            par1.style = doc.styles['Title']


def insert_table_after_text(document, table):
    '''
    插入测评方案签字内容
    @param document:
    @param table:
    @return:
    '''
    inser_page(document)
    # tbl, p = copy_table_after(table=table, paragraph=paragraph_target)
    for paragraph in document.paragraphs:
        paragraph_text = paragraph.text
        if paragraph_text == '被测单位方案确认签字页\n':
            move_table_after(table, paragraph)
            # 给表格增加边框
            for r, row in enumerate(table.rows):  # 遍历表格的行
                for c, cell in enumerate(row.cells):  # 遍历每一行的列
                    cell1 = (r, c)  # 在单元格里写入当前的位置（表格、行、列）
                    set_cell_border(
                        table.cell(r, c),
                        top={"sz": 1, "val": "single", "color": "#000000", "space": "0"},
                        bottom={"sz": 1, "val": "single", "color": "#000000", "space": "0"},
                        left={"sz": 1, "val": "single", "color": "#000000", "space": "0"},
                        right={"sz": 1, "val": "single", "color": "#000000", "space": "0"},
                    )


def del_parcontent(doc):
    """
删除指定段落内容
    :param doc:
    """


    restr_start = '等级保护测评工作流程图'
    pos = 0
    for i in range(len(doc.paragraphs)):
        matchRet = re.findall(restr_start, doc.paragraphs[i].text)
        if len(matchRet) > 0:
            pos = i
    runspaelen = len(doc.paragraphs[pos - 2].runs)
    delstartpos = 0
    for i in range(runspaelen - 1):
        if doc.paragraphs[pos - 2].runs[i].text == '其中，':
            delstartpos = i
    for j in range(delstartpos, runspaelen - 1):
        doc.paragraphs[pos - 2].runs[j].clear()

    # doc.paragraphs[pos - 2].clear()  # 删除指定段落


# if __name__ == '__main__':
#     path_word = '../01动态文件_需要输入/测评方案用户接收/LISS2021DJCP081_qqqq案_20210629150407544（李海燕）.docx'
#     path_word01 = '../02静态文件_CNAS/测评方法+测评依据/方案签字页.docx'
#     doc = Document(path_word)
#     doc_target = Document(path_word01)
#     paragraph_target = doc_target.paragraphs[0]
#     table = doc_target.tables[0]
#     insert_table_after_text(doc)
#     doc.save('./5555.docx')
