import os
import time

from django.utils.http import urlquote
from django.core.serializers import serialize
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, FileResponse, StreamingHttpResponse
from crm import settings
# Create your views here.
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from docx import Document

from sales.models import *

from sales.utils.money import cncurrency
from docxtpl import DocxTemplate, InlineImage
from docx.shared import Mm


@csrf_exempt
def contract_add(request):
    '''新增合同的函数'''
    res = {'code': '200'}
    unit_name = request.POST.get('unit_name')
    sys_name = request.POST.get('sys_name')
    code = request.POST.get('code')
    money = request.POST.get('money')
    level = request.POST.get('level')
    name = request.POST.get('name')
    phone = request.POST.get('phone')
    bank = request.POST.get('bank')

    bankcardnum = request.POST.get('bankcardnum')
    province = request.POST.get('province1')
    city = request.POST.get('city1')
    address = request.POST.get('addr')

    user = request.user
    contractdict = {"unit_name": unit_name, "sys_name": sys_name, "address": address, "code": code, 'name': name,
                    'phone': phone, "bank": bank, "bankcardnum": bankcardnum, "province": province, "city": city
        ,
                    "level": level, "money": money, "user": user,
                    }
    print(contractdict)
    try:
        CreateContract.objects.create(**contractdict)
        res['msg'] = '合同添加成功'
    except:
        res['error'] = '合同添加失败'

    return JsonResponse(res)


def contract_edit(request):
    '''弹出编辑合同界面将信息写入到编辑合同界面中'''
    res = {'code': '200'}
    contract_editid = request.GET.get('contract_editid')
    contract = CreateContract.objects.filter(id=contract_editid).values().all()

    if contract:
        contract = list(contract)
        return JsonResponse(contract, safe=False)
    else:
        res['error'] = '程序异常'
        return JsonResponse(contract, safe=False)


@csrf_exempt
def contract_conformedit(request):
    '''对合同信息的确认编辑视图'''
    res = {'code': '200'}
    unit_name = request.POST.get('unit_name')
    sys_name = request.POST.get('sys_name')
    code = request.POST.get('code')
    money = request.POST.get('money')
    level = request.POST.get('level')
    name = request.POST.get('name')
    phone = request.POST.get('phone')
    bank = request.POST.get('bank')
    bankcardnum = request.POST.get('bankcardnum')
    province = request.POST.get('province1')
    city = request.POST.get('city1')
    address = request.POST.get('addr')
    uuid = request.POST.get('uuid')

    user = request.user
    contractdict = {"unit_name": unit_name, "sys_name": sys_name, "address": address, "code": code, 'name': name,
                    'phone': phone, "bank": bank, "bankcardnum": bankcardnum, "province": province, "city": city,
                    "level": level, "money": money, "user": user}
    print(contractdict)
    try:
        CreateContract.objects.filter(id=uuid).update(**contractdict)
        res['msg'] = '成功'
    except:
        res['error'] = '不知道的错误'

    return JsonResponse(res, safe=False)


def contract_conformedel(request):
    '''处理确认删除的函数'''
    res = {'code': '200'}
    delete_uid = request.GET.get('delete_uid')
    try:
        CreateContract.objects.filter(id=delete_uid).delete()
        res['msg'] = '成功'
    except:
        res['error'] = '失败'

    return JsonResponse(res, safe=False)


# 流方式读取文件
def read_file(file_name, size):
    with open(file_name, mode='rb') as fp:
        while True:
            c = fp.read(size)
            if c:
                yield c
            else:
                break


def download(request):
    '''下载合同'''
    dow_uid = request.GET.get('dow_uid')
    context1 = CreateContract.objects.filter(id=dow_uid).values('unit_name', 'sys_name', 'address', 'code', 'level',
                                                                'bankcardnum', 'bank', 'bankcardnum',
                                                                'phone', 'province', 'city', 'name', 'money')

    context1 = list(context1)

    context1 = context1[0]
    for k, v in context1.items():
        if k == 'money':
            v = cncurrency(v)
            context1['money'] = v

    filename = context1['unit_name'] + context1['sys_name'] + str(time.time()) + '.docx'

    # filename = 'testhaiyan.docx'  # 所生成的word文档需要以.docx结尾，文档格式需要
    filepath = settings.OUTPUT_FILES_PATH
    template_path = settings.WORD_TEMPLATES_PATH
    template = DocxTemplate(template_path)

    template.render(context1)
    template.save(os.path.join(filepath, filename))
    response = StreamingHttpResponse(read_file(os.path.join(filepath, filename), 512))
    response['Content-Type'] = 'application/msword'
    file_name_chinese = filename
    response['Content-Disposition'] = 'attachment;filename="%s"' % (urlquote(file_name_chinese))
    return response
