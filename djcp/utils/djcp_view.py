import os
import re
import time

from django.utils.encoding import escape_uri_path
from django.utils.http import urlquote
from django.http import JsonResponse, HttpResponse, FileResponse, StreamingHttpResponse
from crm import settings
from djcp.models import *
from djcp.utils import util
from djcp.utils.util import ZipUtilities, mkdir_cnas
from sales.utils.money import cncurrency
from docxtpl import DocxTemplate
from system import models


def apply_pronum(request):
    '''下载编号申请文件'''
    res = {'code': '200'}
    # 准备写入的路径
    dow_uid = request.GET.get('pronum_uid')
    dow_uid = int(dow_uid)
    datas, cus, proinfo = util.clear_date(dow_uid)  # 数据清洗和处理

    project_name = cus.get('unit_name') + proinfo.get('sys_name')
    path01 = settings.CNAS_FILES_PATH_PRONUM
    list_dir = []
    filepath = mkdir_cnas(project_name, '001编号申请')

    for list in os.listdir(path01):
        if list.endswith('.docx'):
            list_dir.append(list)
    for name in list_dir:
        path = path01 + os.sep + name
        util.download_cnas(filename=name, filepath=filepath, datas=datas, template_path=path)

    utilities = ZipUtilities()
    filename = '001编号申请_' + project_name
    utilities.toZip(filepath, filename)
    response = StreamingHttpResponse(utilities.zip_file, content_type='application/zip')
    response['Content-Disposition'] = "attachment; filename*=utf-8''{}.zip".format(escape_uri_path(filename))
    return response


def signature_and_seal(request):
    '''下载签字盖章'''
    res = {'code': '200'}
    # 准备写入的路径
    dow_uid = request.GET.get('seal_uid')
    dow_uid = int(dow_uid)
    datas, cus, proinfo = util.clear_date(dow_uid)  # 数据清洗和处理
    project_name = cus.get('unit_name') + proinfo.get('sys_name')
    path01 = settings.CNAS_FILES_PATH_SIGNATURE
    list_dir = []
    filepath = mkdir_cnas(project_name, '002签字盖章')
    for list in os.listdir(path01):
        if list.endswith('.docx'):
            list_dir.append(list)

    for name in list_dir:
        path = path01 + os.sep + name
        util.download_cnas(filename=name, filepath=filepath, datas=datas, template_path=path)

    utilities = ZipUtilities()
    filename = '002签字盖章_' + project_name
    utilities.toZip(filepath, filename)
    response = StreamingHttpResponse(utilities.zip_file, content_type='application/zip')
    response['Content-Disposition'] = "attachment; filename*=utf-8''{}.zip".format(escape_uri_path(filename))
    return response


def end_document(request):
    '''下载签字盖章'''
    res = {'code': '200'}
    # 准备写入的路径
    dow_uid = request.GET.get('end_uid')
    dow_uid = int(dow_uid)
    datas, cus, proinfo = util.clear_date(dow_uid)  # 数据清洗和处理

    project_name = cus.get('unit_name') + proinfo.get('sys_name')
    path01 = settings.CNAS_FILES_END
    list_dir = []
    filepath = mkdir_cnas(project_name, '003收尾文件')
    for list in os.listdir(path01):
        if list.endswith('.docx'):
            list_dir.append(list)

    for name in list_dir:
        path = path01 + os.sep + name
        util.download_cnas(filename=name, filepath=filepath, datas=datas, template_path=path)

    utilities = ZipUtilities()
    filename = '003收尾文件_' + project_name
    utilities.toZip(filepath, filename)
    response = StreamingHttpResponse(utilities.zip_file, content_type='application/zip')
    response['Content-Disposition'] = "attachment; filename*=utf-8''{}.zip".format(escape_uri_path(filename))
    return response
