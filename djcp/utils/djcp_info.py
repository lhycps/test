import os
import re
import lxml.etree
from django.http import JsonResponse, StreamingHttpResponse, HttpResponse
from django.utils.encoding import escape_uri_path
from django.views.decorators.csrf import csrf_exempt
from docx import Document
from crm import settings
from djcp.models import Info, Djcp, Customer, CUserInfo, ProInfo, GmanagerInfo, ProDate
from djcp.utils.function import merge_dicts
from djcp.utils.util import num_to_char, datetomonth
from system import models
from docx.oxml.ns import qn
from docx.oxml import OxmlElement


def Information_edit(request):
    # 点击编辑按钮弹出编辑模态对话框并将数据插入到对应的模态对话框中
    res = {'code': "200"}
    info_uid = request.GET.get('info_uid')
    infoobj = Info.objects.filter(djcp=info_uid).values('zc_excel', 'tpt', 'tpt_desc', 'djcp__customer__unit_name',
                                                        'djcp__proInfo__sys_name')

    data = list(infoobj)[0]

    return JsonResponse(data, safe=False)


@csrf_exempt
def Information_add(request):
    '''存放到数据库中'''
    res = {'user': None, 'msg': None}
    info_uid = request.POST.get('info_uid')
    zichan = request.FILES.get('zichan', '')
    tpt = request.FILES.get('tpt', '')
    tpt_desc = request.POST.get('tpt_desc')
    query_dict = {}
    if zichan:
        query_dict['zc_excel'] = zichan
    if tpt:
        query_dict['tpt'] = tpt
    if tpt_desc:
        query_dict['tpt_desc'] = tpt_desc

    try:
        '''将数据插入到数据库中'''
        Info.objects.update_or_create(defaults=query_dict,
                                      djcp_id=info_uid)

        res['msg'] = '新建成功'
    except:
        res['error'] = '错误，可能数据库中已存在该数据或者您提交的数据类型为空'
    return JsonResponse(res, safe=False)


def cleardata_info(dow_uid):
    '''
    信息调查表所需数据清洗和处理
    :return:
    :dow_uid:需要处理的项目信息id
    '''
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
    proinfo = ProInfo.objects.filter(id=proinfo_id).values('sys_name', 'level', 'sys_service',
                                                           'sys_obj', 'pro_num', 'Record_num', 'pm',
                                                           'desc')
    prodate = ProDate.objects.filter(id=prodate_id).values('question')
    tptdesc = Info.objects.filter(djcp_id=dow_uid).values('tpt', 'tpt_desc')
    datas = []  # 存放处理后的干净数据的最终生成word文件使用
    remainddate = {}  # 存放个别特殊字段

    cus = list(cus)
    cuserinfo = list(cuserinfo)
    gmanager = list(gmanager)
    proinfo = list(proinfo)
    prodate = list(prodate)
    tptdesc = list(tptdesc)

    cus = cus[0]
    cuserinfo = cuserinfo[0]
    gmanager = gmanager[0]
    proinfo = proinfo[0]
    prodate = prodate[0]
    tptdesc = tptdesc[0]

    '''处理项目信息的函数'''
    for i, j in proinfo.items():
        if i == "level":
            eva = ProInfo.objects.filter(id=proinfo_id).first()
            m = eva.get_level_display()
            proinfo[i] = m
            mm = re.findall(r"\d+\.?\d*", m)  # 提取S2A2G2中的数字
            aalist = []
            for i in mm:
                i = int(i)
                i = num_to_char(i)
                aalist.append(i)
            remainddate['slevel'] = aalist[0]  # 业务信息安全保护等级
            remainddate['alevel'] = aalist[1]  # 系统服务安全保护等级
            remainddate['glevel'] = aalist[2]  # 安全保护等级

        if i == "pm":  # 项目经理
            pm = int(j)
            eva = models.Evaluate.objects.filter(id=pm).values()[0]
            j = eva.get('name')
            proinfo[i] = j

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
    for i, j in prodate.items():
        if i == 'question':
            question = datetomonth(j)
            remainddate['questionface'] = question  # 信息调查表封面

    project1 = merge_dicts(cus, cuserinfo, gmanager, proinfo, prodate, remainddate, tptdesc)
    datas.append(project1)
    datas = datas[0]
    print("datas", datas)
    return datas


# word目录刷新
'''
def update_toc(docx_file):
    pythoncom.CoInitialize()  # 加上的
    word = win32com.client.DispatchEx("Word.Application")
    pythoncom.CoInitialize()  # 加上的
    doc = word.Documents.Open(docx_file)
    doc.TablesOfContents(1).Update()
    doc.Close(SaveChanges=True)
    word.Quit()
'''


def set_updatefields_true(docx_path):
    namespace = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
    doc = Document(docx_path)
    update_name_space = "%supdateFields" % namespace
    val_name_space = "%sval" % namespace
    # add child to doc.settings element
    # 自动更新目录
    try:
        element_update_field_obj = lxml.etree.SubElement(doc.settings.element, update_name_space)
        element_update_field_obj.set(val_name_space, "true")
    except Exception as e:
        del e
    doc.save(docx_path)


def downloadinfo(request):
    downloadinfo = request.GET.get('downloadinfo')
    downloadinfo = Info.objects.filter(djcp_id=downloadinfo).values('downloadinfo')
    downloadinfo = list(downloadinfo)
    file_path = downloadinfo[0]['downloadinfo'].split('/')[1]
    filename = file_path
    file_path = os.path.join(settings.INFO_OUTPUT_PATH, file_path)
    file_path = re.sub('\\\\', '/', file_path)  # 路径符号转换

    def file_iterator(file_path, chunk_size=512):
        """
        文件生成器,防止文件过大，导致内存溢出
        :param file_path: 文件绝对路径
        :param chunk_size: 块大小
        :return: 生成器
        """
        with open(file_path, mode='rb') as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break

    try:
        response = StreamingHttpResponse(file_iterator(file_path))
        # 以流的形式下载文件,这样可以实现任意格式的文件下载
        response['Content-Type'] = 'application/pdf'
        # Content-Disposition就是当用户想把请求所得的内容存为一个文件的时候提供一个默认的文件名
        response['Content-Disposition'] = "attachment; filename*=utf-8''{}".format(
            escape_uri_path(filename))  # 文件名可设置为中文
    except:
        return HttpResponse("Sorry but Not Found the File")

    return response
    # return HttpResponse('ok')
