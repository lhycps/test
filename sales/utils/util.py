import re


def datetomonth(data):
    """
    将xxxx-xx-xx格式转化成xxxx年xx月xx日的函数
    :param data: 传入的要转化的日期字符串数据
    """
    date_list = re.split('-', data)
    strdate = ''

    for i, j in enumerate(date_list):
        if i == 0:
            strdate = strdate + j + '年'
        elif i == 1:
            strdate = strdate + j + '月'
        else:
            strdate = strdate + j + '日'
    return strdate


def get_sys_service(proinfo):
    """
    处理系统表里面的sys_service，sys_obj
    :param proinfo:
    :return:
    """
    sys_servicedict = {
        '1': '🗹业务专网      ☐互联网       ☐其它',
        '2': '☐业务专网      🗹互联网       ☐其它',
        '3': '☐业务专网      ☐互联网       🗹其它',
    }

    for i, j in proinfo.items():
        if i == 'sys_service':
            proinfo[i] = sys_servicedict.get(j)

    return proinfo


def num_to_char(num):
    """数字转中文"""
    num = str(num)
    new_str = ""
    num_dict = {"0": u"零", "1": u"一", "2": u"二", "3": u"三", "4": u"四", "5": u"五", "6": u"六", "7": u"七", "8": u"八",
                "9": u"九"}
    listnum = list(num)
    # print(listnum)
    shu = []
    for i in listnum:
        # print(num_dict[i])
        shu.append(num_dict[i])
    new_str = "".join(shu)
    new_str = new_str + '级'
    # print(new_str)
    return new_str
