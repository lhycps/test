import re
import os
import zipstream
from django.core.files.base import ContentFile
from django.db.models import Q
from docx.shared import Mm
from docxtpl import DocxTemplate, InlineImage
from cryptography.fernet import Fernet
from crm import settings
from djcp.models import ProInfo, ProDate, Djcp, Customer, CUserInfo, GmanagerInfo, BonusUnit, BonusSystem
from system import models
import base64
import logging
from cryptography.fernet import Fernet
import traceback
from crm import settings
import subprocess
import traceback


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

    shu = []
    for i in listnum:
        shu.append(num_dict[i])
    new_str = "".join(shu)
    new_str = new_str + '级'

    return new_str


def merge_dicts(*dict_args):
    '''定义多个字典合并的函数'''
    result = {}
    for item in dict_args:
        result.update(item)
    return result


def mkdir_cnas(project_name, template_filename):
    '''
    动态生成处理后的CNAS文件夹的名字
    :param project_name: 项目名称：上海吹牛逼有限公司OA系统
    :param template_filenam: 模板文件夹名字：'001项目编号'
    :return:
    '''
    work_path = settings.OUTPUT_CNAS_FILES_PATH + '/CNAS/' + project_name + '_CANS/' + template_filename + '_{}'.format(
        project_name) + '/'
    if not os.path.exists(work_path):
        os.makedirs(work_path)
    return work_path


def clear_date(dow_uid):
    '''传入需要处理的数据的id'''

    proobj = Djcp.objects.filter(id=dow_uid).first()
    customer_id = proobj.customer_id
    cuserinfo_id = proobj.cuserInfo_id
    proinfo_id = proobj.proInfo_id
    prodate_id = proobj.prodate_id
    gmanager_id = proobj.gmanagerInfo_id

    cus = Customer.objects.filter(id=customer_id).values('unit_name', 'company_profile', 'address', 'nature', 'code',
                                                         'department', 'superdepar')
    cuserinfo = CUserInfo.objects.filter(id=cuserinfo_id).values('name', 'email', 'post', 'phone', 'telephone')
    gmanager = GmanagerInfo.objects.filter(id=gmanager_id).values('gmanager', 'gphone', 'gtelephone', 'gpost', 'gemail')
    proinfo = ProInfo.objects.filter(id=proinfo_id).values('proname', 'agentname', 'sys_name', 'level', 'sys_service',
                                                           'sys_obj', 'pro_num', 'Record_num', 'pm', 'supervisor',
                                                           'reporter_pro', 'supervisored', 'desc')
    prodate = ProDate.objects.filter(id=prodate_id).values('apply', 'accept', 'formalization', 'contract', 'secret',
                                                           'authorization', 'task', 'question', 'scheme',
                                                           'schemereview', 'firstmeeting', 'onsiteevalaation', 'record'
                                                           , 'test', 'lasttmeeting', 'reporter_date', 'reporterview',
                                                           'acceptreporter', 'agreen')

    datas = []  # 存放处理后的干净数据的最终生成word文件使用
    remainddate = {}  # 存放剩下14个字段的

    cus = list(cus)
    cuserinfo = list(cuserinfo)
    gmanager = list(gmanager)
    proinfo = list(proinfo)
    prodate = list(prodate)

    cus = cus[0]
    cuserinfo = cuserinfo[0]
    gmanager = gmanager[0]
    proinfo = proinfo[0]
    prodate = prodate[0]

    '''处理项目信息的函数'''
    for i, j in proinfo.items():
        if i == "level":
            eva = ProInfo.objects.filter(id=proinfo_id).first()
            m = eva.get_level_display()
            proinfo[i] = m
            tt = {
                '1': '□ 不确定           🗹确定，安全保护等级是：\n□第一级 A___  S___ 🗹第二级  A_2_ S _2_ □第三级 A__ S __',
                '2': '□ 不确定           🗹确定，安全保护等级是：\n□第一级 A___  S___ 🗹第二级  A_1_ S _2_ □第三级 A__ S __',
                '3': '□ 不确定           🗹确定，安全保护等级是：\n□第一级 A___  S___ 🗹第二级  A_2_ S_1_  □第三级 A__ S __',
                '4': '□ 不确定           🗹确定，安全保护等级是：\n□第一级 A___  S___ □第二级  A__ S __   🗹第三级 A_3_ S _3_',
                '5': '□ 不确定           🗹确定，安全保护等级是：\n□第一级 A___  S___ □第二级  A__ S __   🗹第三级 A_2_ S _3_',
                '6': '□ 不确定           🗹确定，安全保护等级是：\n□第一级 A___  S___ □第二级  A__ S __   🗹第三级 A_3_ S _2_',
            }

            remainddate['formal_level'] = tt.get(j)  # 形式化等级

            hh = {
                "1": '''□第一级 A___  S___          🗹第二级 A_2_ S _2_\n□第三级 A__  S__         □第四级  A__ S __ ''',
                "2": '''□第一级 A___  S___          🗹第二级 A_1_ S _2_\n□第三级 A__  S__         □第四级  A__ S __ ''',
                "3": '''□第一级 A___  S___          🗹第二级 A_2_ S _1_\n□第三级 A__  S__         □第四级  A__ S __ ''',
                "4": '''□第一级 A___  S___          □第二级 A__ S __\n🗹第三级 A_3_  S_3_         □第四级  A__ S __ ''',
                "5": '''□第一级 A___  S___          □第二级 A__ S __\n🗹第三级 A_2_  S_3_         □第四级  A__ S __ ''',
                "6": '''□第一级 A___  S___          □第二级 A__ S __\n🗹第三级 A_3_  S_2_         □第四级  A__ S __ ''',
            }
            remainddate['sspl'] = hh.get(j)  # 系统安全保护等级
            mm = re.findall(r"\d+\.?\d*", m)  # 提取S2A2G2中的数字

            aalist = []
            for i in mm:
                i = int(i)
                i = num_to_char(i)
                aalist.append(i)
            remainddate['slevel'] = aalist[0]  # 业务信息安全保护等级
            remainddate['alevel'] = aalist[1]  # 系统服务安全保护等级
            remainddate['glevel'] = aalist[2]  # 安全保护等级

        if i == "sys_service":  # 系统网络性质
            sys_servicedict = {
                '1': '🗹业务专网      ☐互联网       ☐其它',
                '2': '☐业务专网      🗹互联网       ☐其它',
                '3': '☐业务专网      ☐互联网       🗹其它',
            }

            proinfo[i] = sys_servicedict.get(j)
        if i == "sys_obj":  # 系统服务对象
            sys_objedict = {
                '1': '🗹 单位内部人员  ☐ 社会公众人员 ☐两者均包括  ☐其他',
                '2': '☐ 单位内部人员  🗹 社会公众人员 ☐两者均包括  ☐其他',
                '3': '☐ 单位内部人员  ☐ 社会公众人员 🗹两者均包括  ☐其他',
                '4': '☐ 单位内部人员  ☐ 社会公众人员 ☐两者均包括  🗹 其他',
            }

            proinfo[i] = sys_objedict.get(j)

        if i == 'supervisor':
            supervisor = int(j)
            eva = models.Evaluate.objects.filter(id=supervisor).values()[0]
            j = eva.get('name')
            proinfo[i] = j

        if i == "pm":  # 项目经理
            pm = int(j)
            eva = models.Evaluate.objects.filter(id=pm).values()[0]
            j = eva.get('name')
            evaphone = eva.get('phone')
            remainddate['preparer'] = j  # 1:填表人数据
            remainddate['evaphone'] = evaphone  # 1:填表人电话
            proinfo[i] = j

        if i == "reporter_pro":
            reporter_pro = int(j)

            eva = models.Evaluate.objects.filter(id=reporter_pro).values()[0]
            j = eva.get('name')
            proinfo[i] = j
        if i == "supervisored":
            supervisored = []
            m = re.findall(r"\d+\.?\d*", j)
            for j in m:
                eva = models.Evaluate.objects.filter(id=j).values()[0]
                supervisored.append(eva.get('name'))
            supervisored = str(supervisored)
            supervisored = re.sub("'", '', supervisored)
            supervisored = supervisored.strip('[]')
            supervisored = supervisored.replace(',', '、')
            proinfo[i] = supervisored
        if i == "sys_name":
            remainddate['recordtable'] = j + '备案表'  # 备案表
            remainddate['letable'] = j + '定级报告'  # 定级报告
            remainddate['leaddtable'] = j + '定级备案补充信息表'  # 定级备案补充信息表
    '''处理单位信息的函数'''
    for i, j in cus.items():
        if i == "nature":
            naturedict = {
                '1': '🗹党政机关      ☐国家重要行业、重要领域或重要企事业单位       ☐一般企事业单位       ☐其他类型',
                '2': '☐党政机关      🗹国家重要行业、重要领域或重要企事业单位       ☐一般企事业单位       ☐其他类型',
                '3': '☐党政机关      ☐国家重要行业、重要领域或重要企事业单位       🗹一般企事业单位       ☐其他类型',
                '4': '☐党政机关      ☐国家重要行业、重要领域或重要企事业单位       ☐一般企事业单位       🗹其他类型',
            }
            cus[i] = naturedict.get(j)
    '''处理日期格式的函数'''
    ff = []
    for i, j in prodate.items():
        if i == 'contract':
            contime = datetomonth(j)[:-3]
            ff.append(contime)
        if i == 'question':
            question = datetomonth(j)
            remainddate['questionface'] = question  # 信息调查表封面
        if i == 'test':
            test = datetomonth(j)
            remainddate['testmen'] = test  # 监督人签字时间
        if i == 'agreen':
            agreetime = datetomonth(j)[:-3]
            ff.append(agreetime)
        m = datetomonth(j)
        prodate[i] = m

    remainddate['servereva'] = ff[0] + '-' + ff[1]  # 服务评价表时间
    remainddate['acceptunit'] = '上海交通大学信息安全服务技术研究实验室'  # 接收单位

    '''处理剩余的14个字段的函数'''

    project1 = merge_dicts(cus, cuserinfo, gmanager, proinfo, prodate, remainddate)

    datas.append(project1)
    datas = datas[0]
    return datas, cus, proinfo


# 流方式读取文件
def read_file(file_name, size):
    with open(file_name, mode='rb') as fp:
        while True:
            c = fp.read(size)
            if c:
                yield c
            else:
                break


def download_cnaspic(filename, filepath, datas, template_path, picture_path):
    '''处理信息调查表的函数'''
    template = DocxTemplate(template_path)  # 选定模板---DocxTemplate("my_word_template.docx")
    datas['tpt'] = InlineImage(
        template, picture_path, width=Mm(150)
    )
    context1 = datas  # 需要替换的内容#---{ 'company_name' : "World company" }
    template.render(context1)  # 渲染替换
    file_path = os.path.join(filepath, filename)
    template.save(file_path)  # 保存
    return file_path


def download_cnas(filename, filepath, datas, template_path):
    '''处理cnas的函数'''
    template = DocxTemplate(template_path)  # 选定模板---DocxTemplate("my_word_template.docx")
    context1 = datas  # 需要替换的内容#---{ 'company_name' : "World company" }
    template.render(context1)  # 渲染替换
    file_path = os.path.join(filepath, filename)
    template.save(file_path)  # 保存
    return file_path


class ZipUtilities:
    zip_file = None

    def __init__(self):
        self.zip_file = zipstream.ZipFile(mode='w', compression=zipstream.ZIP_DEFLATED)

    def toZip(self, file, name):
        if os.path.isfile(file):
            self.zip_file.write(file, arcname=os.path.basename(file))
        else:
            self.addFolderToZip(file, name)

    def addFolderToZip(self, folder, name):
        for file in os.listdir(folder):
            full_path = os.path.join(folder, file)
            if os.path.isfile(full_path):
                self.zip_file.write(full_path, arcname=os.path.join(name, os.path.basename(full_path)))
            elif os.path.isdir(full_path):
                self.addFolderToZip(full_path, os.path.join(name, os.path.basename(full_path)))

    def close(self):
        if self.zip_file:
            self.zip_file.close()


def superuser_unit_view(inputcal, pk):
    '''管理员的视图:单位展示'''
    if inputcal == '' and pk == None:
        queryset = Customer.objects.all()
    elif pk:
        queryset = Customer.objects.all().filter(id=pk)
    else:
        queryset = Customer.objects.all().filter(
            Q(unit_name__icontains=inputcal) | Q(desc__icontains=inputcal) | Q(address__icontains=inputcal) | Q(
                nature__icontains=inputcal) | Q(code__icontains=inputcal) | Q(department__icontains=inputcal) | Q(
                superdepar__icontains=inputcal))
    return queryset


def superuser_project_view(inputcal, pagesize):
    '''管理员的视图:项目展示'''

    if inputcal == '' and pagesize == '':
        queryset = Djcp.objects.all().values(
            'customer_id', 'customer__unit_name', 'proInfo_id', 'proInfo__sys_name', 'prodate_id',
            'prodate__contract', 'cuserInfo_id', 'cuserInfo__name', 'gmanagerInfo_id', 'gmanagerInfo__gmanager',
            'info__tpt', 'info__downloadinfo', 'pk')
    else:
        queryset = Djcp.objects.all().filter(
            Q(customer__unit_name__icontains=inputcal) | Q(proInfo__sys_name__icontains=inputcal) | Q(
                cuserInfo__name__icontains=inputcal) | Q(gmanagerInfo__gmanager__icontains=inputcal)).values(
            'customer_id', 'customer__unit_name', 'proInfo_id', 'proInfo__sys_name', 'prodate_id',
            'prodate__contract', 'cuserInfo_id', 'cuserInfo__name', 'gmanagerInfo_id', 'gmanagerInfo__gmanager',
            'info__tpt', 'info__downloadinfo', 'pk')
    return queryset


def superuser_contact_view(inputcal, pk):
    '''管理员的视图:联系人展示'''
    if inputcal == '' and pk == None:
        queryset = CUserInfo.objects.all()
    elif pk:
        queryset = CUserInfo.objects.all().filter(id=pk)

    else:
        queryset = CUserInfo.objects.all().filter(
            Q(name__icontains=inputcal) | Q(email__icontains=inputcal) | Q(post__icontains=inputcal) | Q(
                phone__icontains=inputcal) | Q(telephone__icontains=inputcal) | Q(
                nameinfo__unit_name__icontains=inputcal))
    return queryset


def superuser_gmanager_view(inputcal, pk):
    '''管理员的视图:负责人展示'''
    if inputcal == '' and pk == None:
        queryset = GmanagerInfo.objects.all()
    elif pk:
        queryset = GmanagerInfo.objects.all().filter(id=pk)

    else:
        queryset = GmanagerInfo.objects.all().filter(
            Q(gmanager__icontains=inputcal) | Q(gemail__icontains=inputcal) | Q(gpost__icontains=inputcal) | Q(
                gphone__icontains=inputcal) | Q(gtelephone__icontains=inputcal) | Q(
                gnameinfo__unit_name__icontains=inputcal))
    return queryset


def superuser_date_view(inputcal, pk):
    '''管理员的视图:日期展示'''
    if inputcal == '' and pk == None:
        queryset = ProDate.objects.all()
    elif pk:
        queryset = ProDate.objects.all().filter(id=pk)
    else:
        queryset = ProDate.objects.all().filter(Q(unit__unit_name=inputcal))

    return queryset


def superuser_system_view(inputcal, pk):
    '''管理员的视图:日期展示'''
    if inputcal == '' and pk == None:
        queryset = ProInfo.objects.all()
    elif pk:
        queryset = ProInfo.objects.all().filter(id=pk)

    else:

        queryset = ProInfo.objects.all().filter(
            Q(proname__icontains=inputcal) | Q(agentname__icontains=inputcal) | Q(sys_name__icontains=inputcal) | Q(
                level__icontains=inputcal) | Q(pro_num__icontains=inputcal) | Q(Record_num__icontains=inputcal) | Q(
                pm__icontains=inputcal) | Q(proinfo__unit_name__contains=inputcal))

    return queryset


def dic_slice(_dic, start, end):
    """
    字典的切片
    :param start: 开始切片的key
    :param end: 结束切片的key
    :return: 新的字典
    """
    _dic = _dic
    keys = list(_dic.keys())
    _dic_slice = {}
    for key in keys[keys.index(start): keys.index(end)]:  # 通过index方法，让列表自己找到索引值并返回
        _dic_slice[key] = _dic[key]
    _dic_slice[end] = _dic[end]  # 这里我是想取包括这两个键之间的所有元素，所以将end对应键的值也传入了新字典
    return _dic_slice


def dict_chunk(dicts, size):
    '''
        # 对字典进行分割
    :param dicts: 字典
    :param size: 需要分的组数，2
    :return:
    '''
    new_list = []
    dict_len = len(dicts)
    # 获取分组数
    while_count = dict_len // size + 1 if dict_len % size != 0 else dict_len / size
    split_start = 0
    split_end = size
    while (while_count > 0):
        # 把字典的键放到列表中，然后根据偏移量拆分字典
        new_list.append({k: dicts[k] for k in list(dicts.keys())[split_start:split_end]})
        split_start += size
        split_end += size
        while_count -= 1
    return new_list


def formdata_to_dict(_dict):
    '''
    将bonus=0&bonus_pro=1&unit=上海吹牛逼有限公司格式数据转换成字典格式
    :param _dict:
    :return:
    '''
    m = _dict.replace('=', ':')
    m = m.replace('&', ',')
    m = m.split(',')
    new_dict = {}
    for i in m:
        i = i.split(':')
        new_dict[i[0]] = i[1]
    return new_dict


#
def Autonomous_addition(new_list, dd, user, hh):
    '''用户自己添加系统的函数'''
    bonus = dd['bonus']
    bonus = encrypt(bonus)  # 将奖金进行加密处理
    print('加密处理后的奖金', bonus)

    bonusobj = BonusUnit.objects.create(nature=dd['nature'], unit=dd['unit'], bonus=bonus,
                                        pm=dd['pm'], sale=dd['sale'], remarks=dd['remarks'], user=user)
    if hh:  # 用户传入了合同
        bonusobj.contract_pdf.save(hh.name, ContentFile(hh.read()))

    for index, _dict in enumerate(new_list):
        if index == 0:
            BonusSystem.objects.create(system=_dict['system'], level=_dict['level'],
                                       completion_time=_dict['completion_time'], bonusunit=bonusobj)

        else:
            BonusSystem.objects.create(system=_dict['system{}'.format(index)],
                                       level=_dict['level{}'.format(index)],
                                       completion_time=_dict['completion_time{}'.format(index)],
                                       bonusunit=bonusobj)


def bindProAdd(new_list, dd, user, hh):
    '''通过绑定项目添加的函数'''
    bonus = dd['bonus']
    bonus = encrypt(bonus)  # 将奖金进行加密处理

    bonusobj = BonusUnit.objects.create(nature=dd['nature'], unit=dd['unit'], bonus=bonus,
                                        pm=dd['pm'], sale=dd['sale'], remarks=dd['remarks'], user=user,
                                        bonus_pro_id=dd['bonus_pro'])
    if hh:
        bonusobj.contract_pdf.save(hh.name, ContentFile(hh.read()))
    for index, _dict in enumerate(new_list):
        if index == 0:
            BonusSystem.objects.create(system=_dict['system'], level=_dict['level'],
                                       completion_time=_dict['completion_time'], bonusunit=bonusobj)
        else:
            BonusSystem.objects.create(system=_dict['system{}'.format(index)],
                                       level=_dict['level{}'.format(index)],
                                       completion_time=_dict['completion_time{}'.format(index)], bonusunit=bonusobj)


def Autonomous_updateition(new_list, dd, user, hh, uid):
    '''更新系统信息'''
    bonus = dd['bonus']
    bonus = encrypt(bonus)  # 将奖金进行加密处理
    print('加密处理后的奖金', bonus)
    BonusUnit.objects.filter(id=uid).update(nature=dd['nature'], unit=dd['unit'], bonus=bonus,
                                            pm=dd['pm'], sale=dd['sale'], remarks=dd['remarks'], user=user)
    bonusobj = BonusUnit.objects.filter(id=uid).first()
    if hh:  # 用户传入了合同
        # bonusobj.contract_pdf = avatar
        # # 最后保存一下即可
        # party_pic.save()
        bonusobj.contract_pdf.save(hh.name, ContentFile(hh.read()))
    print("new_list", new_list)
    print("bonusobj", bonusobj)

    for index, _dict in enumerate(new_list):
        if index == 0:
            BonusSystem.objects.create(system=_dict['system'], level=_dict['level'],
                                       completion_time=_dict['completion_time'], bonusunit_id=uid)

        else:
            BonusSystem.objects.create(system=_dict['system{}'.format(index)],
                                       level=_dict['level{}'.format(index)],
                                       completion_time=_dict['completion_time{}'.format(index)],
                                       bonusunit_id=uid)


def encrypt(txt):
    try:
        txt = str(txt)
        cipher_suite = Fernet(settings.ENCRYPT_KEY)
        encrypted_text = cipher_suite.encrypt(txt.encode('ascii'))
        encrypted_text = base64.urlsafe_b64encode(encrypted_text).decode("ascii")
        return encrypted_text
    except Exception as e:
        print(e)
        logging.getLogger("error_logger").error(traceback.format_exc())
    return None


def decrypt(txt):
    try:
        txt = base64.urlsafe_b64decode(txt)
        cipher_suite = Fernet(settings.ENCRYPT_KEY)
        decoded_text = cipher_suite.decrypt(txt).decode("ascii")
        return decoded_text
    except Exception as e:
        print(e)
        logging.getLogger("error_logger").error(traceback.format_exc())
        return None


def callJar(jar_path, jarParams):
    '''

    :param jar_path: ./wordUtils.jar
    :param jarParams: one.docx tow.docx
    :return:
    '''
    try:
        # 构造执行语句
        # jar_path = './wordUtils.jar'
        execute = "java -jar {} {}".format(jar_path, jarParams)
        # print(execute)
        # 执行jar 并返回结果
        output = subprocess.Popen(execute, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        # 获取返回结果
        temp = output.stdout.readlines()
        # 输出返回结果
        print('JAR的执行输出结果：', temp)
        # result = (True, list(map(lambda x: str(x, 'utf-8'), temp)))
        result = (True, '正常执行')
    except  Exception as ex:
        traceback.print_exc()
        print("出现异常来这里")
        result = (False, ex)

    return result  # 可以根据返回结果判断执行是否成功
