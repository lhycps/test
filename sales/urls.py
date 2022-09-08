from django.contrib import admin
from django.urls import path, include, re_path
from sales import views
from .utils import sales_view

urlpatterns = [
    path('contactview/', views.ContactView.as_view(), name='contactview'),  # 合同页面
    path('loadArea/', views.LoadAreaView.as_view(), name='loadArea'),  # 加载区划信息
    path('contract_add/', sales_view.contract_add, name='contract_add'),  # 增加合同
    path('contract_edit/', sales_view.contract_edit, name='contract_edit'),  # 弹出编辑合同
    path('contract_conformedit/', sales_view.contract_conformedit, name='contract_conformedit'),  # 确定编辑合同
    path('contract_conformedel/', sales_view.contract_conformedel, name='contract_conformedel'),  # 确定编辑合同
    path('download/', sales_view.download, name='download'),  # 下载合同
]
