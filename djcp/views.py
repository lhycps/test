import datetime
import os
import re
from django.db.models import Q
from django.shortcuts import render
from django.utils import timezone
from django.http import JsonResponse, StreamingHttpResponse, response, HttpResponse
from django.utils.encoding import escape_uri_path
from django.views.decorators.csrf import csrf_exempt
from crm import settings
from crm.settings import INFO_OUTPUT_PATH
from .models import *
from system import models
from .utils import function, pagination, formdata, info, case, djcp_case
from djcp.utils import bouns_view
from djcp.utils import util
from .utils.djcp_info import cleardata_info

from updateTOC import updatedirdocx


def project(request):
    cuslist = function.get_unitinfo(request)
    pagesize = request.GET.get('pagesize', 10)
    pagesize = int(pagesize)
    user = request.user
    inputcal = request.GET.get('search', '')
    if user.is_superuser:
        queryset = util.superuser_project_view(inputcal, pagesize)
    else:
        if inputcal == '' and pagesize == '':
            queryset = Djcp.objects.filter(gmanagerInfo__gnameinfo__user=user).values(
                'customer_id', 'customer__unit_name', 'proInfo_id', 'proInfo__sys_name', 'prodate_id',
                'prodate__contract', 'cuserInfo_id', 'cuserInfo__name', 'gmanagerInfo_id', 'gmanagerInfo__gmanager',
                'info__tpt', 'info__downloadinfo', 'case__caseUpload', 'case__caseDown', 'pk')
        else:
            queryset = Djcp.objects.filter(gmanagerInfo__gnameinfo__user=user).filter(
                Q(customer__unit_name__icontains=inputcal) | Q(proInfo__sys_name__icontains=inputcal) | Q(
                    cuserInfo__name__icontains=inputcal) | Q(gmanagerInfo__gmanager__icontains=inputcal)).values(
                'customer_id', 'customer__unit_name', 'proInfo_id', 'proInfo__sys_name', 'prodate_id',
                'prodate__contract', 'cuserInfo_id', 'cuserInfo__name', 'gmanagerInfo_id', 'gmanagerInfo__gmanager',
                'info__tpt', 'info__downloadinfo', 'case__caseUpload', 'case__caseDown', 'pk')

    all_count = queryset.count()
    current_page_num = request.GET.get('page', 1)
    paginationobj = pagination.Pagination(request, queryset, page_size=pagesize)
    page_string = paginationobj.html()
    projectlist = queryset.order_by('-pk')[paginationobj.start:paginationobj.end]
    return render(request, 'djcp/project.html', locals())


def unitinfo(request):
    '''添加单位信息'''
    if request.is_ajax():
        res = {'user': None, 'msg': None}
        unit_name = request.POST.get('unit_name', '')
        address = request.POST.get('address', '')
        nature = request.POST.get('nature', '')
        code = request.POST.get('code', '')
        department = request.POST.get('department', '')
        superdepartment = request.POST.get('superdepartment', '')
        desc = request.POST.get('desc', '')
        user = request.user

        Customer.objects.create(unit_name=unit_name, address=address, nature=nature, code=code,
                                department=department, superdepar=superdepartment,
                                company_profile=desc, user=user)
        res['msg'] = '添加成功'
        return JsonResponse(res, safe=False)
    else:
        cuslist = function.get_unitinfo(request)

        get_evrolelist = function.get_evrole()

        return render(request, 'djcp/unitinfo.html', locals())


def contact(request):
    '''添加客户方联系人信息'''
    if request.is_ajax():
        res = {'user': None, 'msg': None}
        userobj = formdata.UserInfoForm(request.POST)
        if userobj.is_valid():
            name = userobj.cleaned_data.get('name')
            email = userobj.cleaned_data.get('email')
            post = userobj.cleaned_data.get('post')
            phone = userobj.cleaned_data.get('phone')
            telephone = userobj.cleaned_data.get('telephone')
            nameinfo_id = request.POST.get('bind_unitcontact')

            user = CUserInfo.objects.create(name=name, email=email, post=post, phone=phone, telephone=telephone,
                                            nameinfo_id=nameinfo_id)
            user.save()
            res['msg'] = '联系人添加成功'
        else:
            res['error'] = userobj.errors

        return JsonResponse(res, safe=False)
    userobj = formdata.UserInfoForm()
    gmanager = formdata.GmanagerInfoForm()
    cuslist = function.get_unitinfo(request)

    return render(request, 'djcp/contact.html', locals())


def gmanagerInfo(request):
    '''添加客户方负责人信息'''
    if request.is_ajax():
        res = {'user': None, 'msg': None}
        userobj = formdata.GmanagerInfoForm(request.POST)
        if userobj.is_valid():
            gname = userobj.cleaned_data.get('gname')
            gemail = userobj.cleaned_data.get('gemail')
            gpost = userobj.cleaned_data.get('gpost')
            gphone = userobj.cleaned_data.get('gphone')
            gtelephone = userobj.cleaned_data.get('gtelephone')
            gnameinfo_id = request.POST.get('bind_gunitcontact')

            user = GmanagerInfo.objects.create(gmanager=gname, gemail=gemail, gpost=gpost, gphone=gphone,
                                               gtelephone=gtelephone,
                                               gnameinfo_id=gnameinfo_id)
            user.save()
            res['msg'] = '添加成功'
        else:
            res['error'] = userobj.errors

        return JsonResponse(res, safe=False)
    userobj = formdata.UserInfoForm()
    gmanager = formdata.GmanagerInfoForm()
    cuslist = function.get_unitinfo(request)

    return render(request, 'djcp/contact.html', locals())


@csrf_exempt
def sysinfo(request):
    '''添加系统描述的信息'''

    if request.is_ajax():
        res = {'user': None}
        proname = request.POST.get("proname")
        agentname = request.POST.get("agentname", '')
        sys_name = request.POST.get("sys_name")
        level = request.POST.get("level", '')
        sys_service = request.POST.get("sys_service", '')
        sys_obj = request.POST.get("sys_obj", '')
        pro_num = request.POST.get("pro_num", '')
        Record_num = request.POST.get("Record_num", '')
        pm = request.POST.get("pm", '')
        supervisor = request.POST.get("supervisor", '')
        reporter = request.POST.get("reporter", '')
        supervisored = request.POST.getlist("supervisored")
        desc = request.POST.get("desc", '')
        proinfo_id = request.POST.get('bind_unitinfo_name')

        pro_dict = {"proname": proname, "sys_obj": sys_obj, "agentname": agentname, "sys_name": sys_name,
                    "level": level, "sys_service": sys_service,
                    "pro_num": pro_num, "Record_num": Record_num, "pm": pm,
                    "supervisor": supervisor, "reporter_pro": reporter, "supervisored": supervisored, "desc": desc,
                    "proinfo_id": proinfo_id}

        if proname == '':
            res['error'] = '项目名称不能为空'
        elif sys_name == '':
            res['error'] = '系统名称不能为空'
        elif desc == '':
            res['error'] = '描述不能为空'
        elif level == '0':
            res['error'] = '未选择系统级别'
        elif sys_service == '0':
            res['error'] = '未选择系统服务性质'
        elif sys_obj == '0':
            res['error'] = '未选择系统服务对象'
        elif pm == '0':
            res['error'] = '未选择项目经理'
        elif supervisor == '0':
            res['error'] = '未选择监督人'
        elif reporter == '0':
            res['error'] = '未选择汇报人'
        elif proinfo_id == '0':
            res['error'] = '未绑定单位信息'
        elif supervisored == []:
            res['error'] = '未选择被监督人'
        else:
            try:
                ProInfo.objects.create(**pro_dict)
                res['msg'] = '添加成功'
            except:
                res['error'] = '不知道的错误'
        return JsonResponse(res, safe=False)


def prodate(request):
    res = {'user': None}
    user = request.user

    order_id = timezone.localtime().strftime('%Y%m%d%H%M%S%f') + ('%09d' % user.id)

    if request.is_ajax():

        unit_id = request.POST.get('bind_unitcontact')
        if unit_id == '0':
            res['error'] = '未绑定单位名称'
            return JsonResponse(res)

        apply = request.POST.get('apply')
        accept = request.POST.get('accept')
        formalization = request.POST.get('formalization')
        contract = request.POST.get('contract')
        secret = request.POST.get('secret')
        authorization = request.POST.get('authorization')

        task = request.POST.get('task')
        question = request.POST.get('question')
        scheme = request.POST.get('scheme')
        schemereview = request.POST.get('schemereview')

        firstmeeting = request.POST.get('firstmeeting')
        onsiteevalaation = request.POST.get('onsiteevalaation')
        record = request.POST.get('record')
        test = request.POST.get('test')
        lasttmeeting = request.POST.get('lasttmeeting')

        reporter = request.POST.get('reporter')
        reporterview = request.POST.get('reporterview')
        acceptreporter = request.POST.get('acceptreporter')
        agreen = request.POST.get('agreen')

        prodate = {"apply": apply, "accept": accept, "formalization": formalization, "contract": contract,
                   "secret": secret, "authorization": authorization,
                   "task": task, "question": question, "scheme": scheme,
                   "schemereview": schemereview, "firstmeeting": firstmeeting, "onsiteevalaation": onsiteevalaation,
                   "record": record,
                   "test": test,
                   "lasttmeeting": lasttmeeting, "reporter_date": reporter, "reporterview": reporterview,
                   "acceptreporter": acceptreporter, "agreen": agreen,
                   "unit_id": unit_id,
                   }
        for k, v in prodate.items():
            if v == '':
                res['error'] = '{}时间未选择'.format(k)
                return JsonResponse(res)

        ProDate.objects.create(**prodate)

        return JsonResponse({'code': '200'})
    cuslist = function.get_unitinfo(request)
    return render(request, 'djcp/prodate.html', locals())


def shcontact(request, pk=None):
    '''
    展示单位联系人的信息
    :param request:
    :param pk: pk值的作用是为了用户通过‘添加项目‘点击按钮能够找到对应的完整数据，pk值不能删除’
    :return:
    '''
    # for i in range(30):
    #     CUserInfo.objects.create(name='李海燕', email='22288@qq.com', post='主管', phone='13878786678',
    #                              telephone='2342218888', nameinfo_id=3)

    inputcal = request.GET.get('search', '')
    user = request.user
    if user.is_superuser:
        queryset = util.superuser_contact_view(inputcal, pk)
    else:
        if inputcal == '' and pk == None:
            queryset = CUserInfo.objects.filter(nameinfo__user=user)
        elif pk:
            queryset = CUserInfo.objects.filter(nameinfo__user=user).filter(id=pk)
        else:
            queryset = CUserInfo.objects.filter(nameinfo__user=user).filter(
                Q(name__icontains=inputcal) | Q(email__icontains=inputcal) | Q(post__icontains=inputcal) | Q(
                    phone__icontains=inputcal) | Q(telephone__icontains=inputcal) | Q(
                    nameinfo__unit_name__icontains=inputcal))

    all_count = queryset.count()
    current_page_num = request.GET.get('page', 1)
    paginationobj = pagination.Pagination(request, queryset, page_size=10)
    page_string = paginationobj.html()

    cuslist = queryset.order_by('-pk')[paginationobj.start:paginationobj.end]

    userobj = formdata.UserInfoForm()
    unitlist = function.get_unitinfo(request)

    return render(request, 'djcp/shcontact.html', locals())


def shgmanager(request, pk=None):
    inputcal = request.GET.get('search', '')
    user = request.user
    if user.is_superuser:
        queryset = util.superuser_gmanager_view(inputcal, pk)
    else:
        if inputcal == '' and pk == None:
            queryset = GmanagerInfo.objects.filter(gnameinfo__user=user)
        elif pk:
            queryset = GmanagerInfo.objects.filter(gnameinfo__user=user).filter(id=pk)

        else:
            queryset = GmanagerInfo.objects.filter(gnameinfo__user=user).filter(
                Q(gmanager__icontains=inputcal) | Q(gemail__icontains=inputcal) | Q(gpost__icontains=inputcal) | Q(
                    gphone__icontains=inputcal) | Q(gtelephone__icontains=inputcal) | Q(
                    gnameinfo__unit_name__icontains=inputcal))

    all_count = queryset.count()
    current_page_num = request.GET.get('page', 1)
    paginationobj = pagination.Pagination(request, queryset, page_size=10)
    page_string = paginationobj.html()

    cuslist = queryset.order_by('-pk')[paginationobj.start:paginationobj.end]

    userobj = formdata.GmanagerInfoForm()
    unitlist = Customer.objects.all()
    return render(request, 'djcp/shgmanager.html', locals())


def shunit(request, pk=None):
    '''查询被测单位信息'''
    # for i in range(10):
    #     Customer.objects.create(unit_name='安徽国康网络安全测评有限公司', desc='一家非常牛逼的公司', address='安徽松江区', nature='私企',
    #                             code='20000', department='技术部', superdepar='信息中心')

    inputcal = request.GET.get('search', '')
    user = request.user
    if user.is_superuser:
        queryset = util.superuser_unit_view(inputcal, pk)
    else:
        if inputcal == '' and pk == None:
            queryset = Customer.objects.filter(user=user)
        elif pk:
            queryset = Customer.objects.filter(user=user).filter(id=pk)
        else:
            queryset = Customer.objects.filter(user=user).filter(
                Q(unit_name__icontains=inputcal) | Q(desc__icontains=inputcal) | Q(address__icontains=inputcal) | Q(
                    nature__icontains=inputcal) | Q(code__icontains=inputcal) | Q(department__icontains=inputcal) | Q(
                    superdepar__icontains=inputcal))

    all_count = queryset.count()
    current_page_num = request.GET.get('page', 1)
    paginationobj = pagination.Pagination(request, queryset, page_size=10)
    page_string = paginationobj.html()
    unitlist = queryset.order_by('-pk')[paginationobj.start:paginationobj.end]
    unitobj = formdata.UnitInfo()
    return render(request, 'djcp/shunit.html', locals())


def shdate(request, pk=None):
    '''查询被测单位时间的视图函数'''
    inputcal = request.GET.get('search', '')
    user = request.user
    if user.is_superuser:
        queryset = util.superuser_date_view(inputcal, pk)
    else:
        if inputcal == '' and pk == None:
            queryset = ProDate.objects.filter(unit__user=user)
        elif pk:
            queryset = ProDate.objects.filter(unit__user=user).filter(id=pk)
        else:
            queryset = ProDate.objects.filter(unit__user=user).filter(Q(unit__unit_name=inputcal))

    all_count = queryset.count()
    current_page_num = request.GET.get('page', 1)
    paginationobj = pagination.Pagination(request, queryset, page_size=10)
    page_string = paginationobj.html()
    datelist = queryset.order_by('-pk')[paginationobj.start:paginationobj.end]
    cuslist = function.get_unitinfo(request)

    return render(request, 'djcp/shdate.html', locals())


def shsystem(request, pk=None):
    inputcal = request.GET.get('search', '')
    user = request.user
    m = []
    if user.is_superuser:
        queryset = util.superuser_system_view(inputcal, pk)
    else:
        if inputcal == '' and pk == None:
            queryset = ProInfo.objects.filter(proinfo__user=user)
        elif pk:
            queryset = ProInfo.objects.filter(proinfo__user=user).filter(id=pk)

        else:

            queryset = ProInfo.objects.filter(proinfo__user=user).filter(
                Q(proname__icontains=inputcal) | Q(agentname__icontains=inputcal) | Q(sys_name__icontains=inputcal) | Q(
                    level__icontains=inputcal) | Q(pro_num__icontains=inputcal) | Q(Record_num__icontains=inputcal) | Q(
                    pm__icontains=inputcal) | Q(proinfo__unit_name__contains=inputcal))

    all_count = queryset.count()
    current_page_num = request.GET.get('page', 1)
    paginationobj = pagination.Pagination(request, queryset, page_size=10)
    page_string = paginationobj.html()
    systemlist = queryset.order_by('-pk')[paginationobj.start:paginationobj.end]

    for i in systemlist:
        if i.supervisor:
            eva = models.Evaluate.objects.filter(id=i.supervisor).values()[0]
            i.supervisor = eva.get('name')
        if i.pm:
            eva = models.Evaluate.objects.filter(id=i.pm).values()[0]
            i.pm = eva.get('name')
        if i.reporter_pro:
            eva = models.Evaluate.objects.filter(id=i.reporter_pro).values()[0]
            i.reporter_pro = eva.get('name')
        if i.supervisored:
            supervisored = []
            m = re.findall(r"\d+\.?\d*", i.supervisored)
            for j in m:
                eva = models.Evaluate.objects.filter(id=j).values()[0]
                supervisored.append(eva.get('name'))
            supervisored = str(supervisored)
            supervisored = re.sub("'", '', supervisored)
            supervisored = supervisored.strip('[]')
            i.supervisored = supervisored

    cuslist = function.get_unitinfo(request)
    get_evrolelist = function.get_evrole()

    for i in get_evrolelist:
        print(i)
    return render(request, 'djcp/shsystem.html', locals())


def bonus(request):
    '''
    奖金记录表
    :param request:
    :return:
    '''
    user = request.user
    renyuanobj = models.Evaluate.objects.all().values('id', 'name')
    for i in renyuanobj:
        request.session[i.get('id')] = i.get('name')
    evalist = models.Evaluate.objects.filter(role__in='3')  # 拿到测评师列表
    salelist = models.Evaluate.objects.filter(role__in='7')  # 拿到商务经理列表
    bonusobj1 = BonusUnit.objects.filter(user=user, bonus_pro_id__isnull=False).values_list('bonus_pro',
                                                                                            flat=True).distinct()  # 拿到奖金单位表中bonus_pro_id的所有值
    bonusobj1 = list(bonusobj1)  # 转成列表，目的是提交给单位表做筛选条件
    djcp1 = Djcp.objects.filter(customer__user=user).values_list('customer', flat=True).distinct()
    temp0 = list(set(list(djcp1)).difference(set(list(bonusobj1))))


    cuslist = Customer.objects.filter(pk__in=temp0)  # 排除已经添加过信息的单位对象。

    bonuslist, query_dict, datefilter = bouns_view.query_date(request)
    if query_dict.get('pm'):
        renyuan_pm = request.session.get(query_dict['pm'])
    if query_dict.get('sale'):
        renyuan_sale = request.session.get(query_dict['sale'])
    if query_dict.get('bonussystem__level__in'):
        if query_dict['bonussystem__level__in'] == [1, 2, 3]:
            query_level = '二级'
        if query_dict['bonussystem__level__in'] == [4, 5, 6]:
            query_level = '三级'
    all_count = bonuslist.count()
    current_page_num = request.GET.get('page', )
    paginationobj = pagination.Pagination(request, bonuslist, page_size=10)
    page_string = paginationobj.html()
    datelist = bonuslist.order_by('-pk')[paginationobj.start:paginationobj.end]
    for i in datelist:
        if i.bonus:
            bonus_dict = BonusUnit.objects.filter(id=i.id).values('bonus')[0]
            i.bonus = util.decrypt(bonus_dict["bonus"])

    return render(request, 'djcp/bonus_list.html', locals())


def Information_download(request):
    '''生成信息调查表'''
    res = {}
    try:
        dow_uid_info = request.GET.get('dow_uid_info')
        path_doc = settings.INFO_FILES_PATH  # 信息调查表模板文件位置
        path_doc = re.sub('\\\\', '/', path_doc)  # 路径符号转换
        infoobj = Info.objects.filter(djcp_id=dow_uid_info).values('zc_excel', 'tpt', 'tpt_desc')
        infolist = list(infoobj)
        path_docx = os.path.join(settings.MEDIA_ROOT, infolist[0]['zc_excel'])  # 用户上传的资产表excel路径
        path_docx = re.sub('\\\\', '/', path_docx)  # 路径符号转换
        datas = cleardata_info(dow_uid=dow_uid_info)  # 信息调查表的数据清理函数
        bumen = datas['department']  # 部门名字
        t = datetime.datetime.now().strftime('%Y-%m-%d')
        filename = datas['unit_name'] + datas['sys_name'] + str(t) + '.docx'
        filename = '信息调查表__' + filename
        outputpath = os.path.join(INFO_OUTPUT_PATH, filename)
        outputpath = re.sub('\\\\', '/', outputpath)  # 路径符号转换
        sys_name = datas['sys_name']
        picture_path = os.path.join(settings.MEDIA_ROOT, datas['tpt'])  # 用户上传的图片地址
        picture_path = re.sub('\\\\', '/', picture_path)  # 路径符号转换
        outputpath = info.start_up(path_docx, path_doc, bumen, sys_name, outputpath)  # 将资产信息填充到信息调查表中
        file_path = util.download_cnaspic(filename=filename, filepath=INFO_OUTPUT_PATH, datas=datas,
                                          template_path=outputpath,
                                          picture_path=picture_path)

        file_path = re.sub('\\\\', '/', file_path)  # 路径符号转换
        if file_path:
            jar_path = settings.jar_path
            updatedirdocx.callJar(jarpath=jar_path, jarParams='{} {}'.format(file_path, file_path))
            Info.objects.filter(djcp_id=dow_uid_info).update(downloadinfo='info/{}'.format(filename))
            res['msg'] = '信息调查表制作完成'
        else:
            res['error'] = '没有找到相关路径'
    except:
        res['error'] = '程序遇到错误'

    return JsonResponse(res, safe=False)


@csrf_exempt
def upload_case(request):
    '''
上传测评方案
'''
    res = {}
    query_dict = {}
    try:
        case_uid = request.POST.get('case_uid')
        caseUploadspan = request.FILES.get('caseUploadspan', '')
        if caseUploadspan:
            query_dict['caseUpload'] = caseUploadspan
            Case.objects.update_or_create(defaults=query_dict, case_id=case_uid)
            res['msg'] = '测评方案添加成功'
    except:
        res['error'] = '程序遇到错误'

    return JsonResponse(res, safe=False)
'''
frhgft6743tg763g67fg7y7
'''