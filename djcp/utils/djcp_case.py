import os
import re

from django.http import StreamingHttpResponse, HttpResponse, JsonResponse
from django.utils.encoding import escape_uri_path
from django.views.decorators.csrf import csrf_exempt

from crm import settings
from djcp.models import Case
from djcp.utils import case
from updateTOC import updatedirdocx


def download_word(file_path, output_filename):
    """
下载word文件
    :param file_path: 文件路径
    :param output_filename: 文件名
    :return:
    """

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
        response['Content-Type'] = 'application/pdf'
        # Content-Disposition就是当用户想把请求所得的内容存为一个文件的时候提供一个默认的文件名
        response['Content-Disposition'] = "attachment; filename*=utf-8''{}.docx".format(
            escape_uri_path(output_filename))  # 文件名可设置为中文
    except:
        return HttpResponse("Sorry but Not Found the File")
    return response


def insert_case(request):
    '''
    插入数据到测评方案输入框中
    :param request:
    :return:
    '''
    res = {}

    case_uid = request.GET.get('case_uid')
    infoobj = Case.objects.filter(case_id=case_uid).values('caseUpload', 'case__customer__unit_name',
                                                           'case__proInfo__sys_name')
    data = list(infoobj)[0]
    res['msg'] = '成功'

    return JsonResponse(data, safe=False)


@csrf_exempt
def create_case(request):
    '''生成方案222222'''
    res = {'code': '200'}
    # 准备写入的路径
    query_dict = {}
    try:
        create_uid_case = request.GET.get('create_uid_case')
        print("create_uid_case", create_uid_case)
        caseUploadobj = Case.objects.filter(case_id=create_uid_case).values('caseUpload')
        temp_case = list(caseUploadobj)[0].get('caseUpload')
        paths_case = os.path.join(settings.MEDIA_ROOT, temp_case)
        paths_case = re.sub('\\\\', '/', paths_case)  # 路径符号转换
        '''生成测评方案、刷新目录并将路径存放在数据库中'''
        output_filename = case.finalstart_up(paths_case=paths_case)  # 生成测评方案的业务处理逻辑
        file_path = os.path.join(settings.CASE_OUTPUT_PATH, '{}.docx'.format(output_filename))
        if file_path:
            jar_path = settings.jar_path
            updatedirdocx.callJar(jarpath=jar_path, jarParams='{} {}'.format(file_path, file_path))  # word文件刷新目录
            caseDown = 'case/{}.docx'.format(output_filename)
            query_dict['caseDown'] = caseDown
            Case.objects.update_or_create(defaults=query_dict, case_id=create_uid_case)  # 插入路径到数据库
            res['msg'] = '测评方案制作完成'
    except:
        res['error'] = '程序遇到错误'

    return JsonResponse(res, safe=False)


def download_case(request):
    '''下载测评方案'''
    downloadcase = request.GET.get('download_case')
    downloadcaseobj = Case.objects.filter(case_id=downloadcase).values('caseDown')
    downloadcaseobj = list(downloadcaseobj)
    file_path = downloadcaseobj[0]['caseDown'].split('/')[1]
    filename = file_path
    file_path = os.path.join(settings.CASE_OUTPUT_PATH, file_path)

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
