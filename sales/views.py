from django.contrib.auth.decorators import login_required
from django.core.serializers import serialize
from django.db.models import Q
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse

# Create your views here.
from django.views import View
from sales.models import *
from sales.utils import pagination


class ContactView(View):
    '''合同视图'''

    def get(self, request):
        inputcal = request.GET.get('search', '')
        user = request.user
        m = []
        if inputcal == '':
            queryset = CreateContract.objects.filter(user=user).order_by('-pk')
        else:
            queryset = CreateContract.objects.filter(user=user).filter(
                Q(unit_name__icontains=inputcal) | Q(sys_name__icontains=inputcal) | Q(
                    level__icontains=inputcal)).order_by('-pk')
        all_count = queryset.count()
        current_page_num = request.GET.get('page', 1)
        paginationobj = pagination.Pagination(request, queryset, page_size=10)
        page_string = paginationobj.html()
        contractlist = queryset.order_by('-pk')[paginationobj.start:paginationobj.end]

        return render(request, 'sales/contract_list.html', locals())


class LoadAreaView(View):
    '''加载区划信息的函数'''

    def get(self, request):
        # 获取请求参数
        pid = request.GET.get('pid', -1)
        pid = int(pid)

        # 根据父id查询区划信息
        areaList = Area.objects.filter(parentid=pid)

        # 进行序列化
        jareaList = serialize('json', areaList)

        return JsonResponse({'jareaList': jareaList})
