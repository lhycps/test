from django.contrib import admin
from django.urls import path, include, re_path
from djcp import views
from .utils import function, djcp_view, bouns_view, djcp_info, djcp_case

urlpatterns = [
    path('unitinfo/', views.unitinfo, name='unitinfo'),  # 添加单位列表
    path('sysinfo/', views.sysinfo, name='sysinfo'),  # 添加系统列表
    path('contact/', views.contact, name='contact'),  # 添加联系人列表
    path('gmanagerInfo/', views.gmanagerInfo, name='gmanagerInfo'),  # 添加负责人列表
    path('prodate/', views.prodate, name='prodate'),  # 添加日期列表

    # 需要登录但是不需要校验权限的url

    path('get_unitinfo/', function.get_unit, name='get_unitinfo'),  # 获得单位信息
    path('get_evroleinfo/', function.get_evrole, name='get_evrole'),  # 获得角色信息

    path('get_unit_id/', function.get_unit_id, name='get_unit_id'),  # 获得单位id
    path('get_contact_id/', function.get_contact_id, name='get_contact_id'),  # 获得联系人id
    path('get_gmanage_id/', function.get_gmanage_id, name='get_gmanage_id'),  # 获得负责人id
    path('get_date_id/', function.get_date_id, name='get_date_id'),  # 获得时间id

    # 查看联系人信息
    re_path(r'shcontact/$', views.shcontact, name='shcontact'),  # 联系人列表
    re_path(r'shcontact/(?P<pk>\d+)/$', views.shcontact),
    path('selectcontact/', function.selectcontact, name='selectcontact'),  # 选择联系人
    path('editcontact/', function.editcontact, name='editcontact'),  # 编辑联系人
    path('conformeditcontact/', function.conformeditcontact),  # 确认编辑联系人
    path('conformdelcontact/', function.conformdelcontact, name='delcontact'),  # 确认删除联系人

    # 查看负责人信息
    re_path(r'shgmanager/$', views.shgmanager, name='shgmanager'),
    re_path(r'shgmanager/(?P<pk>\d+)/$', views.shgmanager),  # 查看联系人正则
    path('editgmanager/', function.editgmanager, name='editgmanager'),  # 编辑负责人
    path('conformeditgmanager/', function.conformeditgmanager, name='conformeditgmanager'),  # 确认编辑负责人
    path('conformdelgmanager/', function.conformdelgmanager, name='conformdelgmanager'),  # 确认删除负责人

    # 查看被测单位信息
    re_path(r'shunit/$', views.shunit, name='shunit'),  # 被测单位列表
    re_path(r'shunit/(?P<pk>\d+)/$', views.shunit),
    path('editunit/', function.editunit),  # 编辑单位
    path('conformeditunit/', function.conformeditunit),  # 确认编辑单位
    path('conformdelunit/', function.conformdelunit),  # 确认删除单位

    # 查看被测单位时间信息
    re_path(r'shdate/$', views.shdate, name='shdate'),  # 时间列表
    re_path(r'shdate/(?P<pk>\d+)/$', views.shdate),
    path('editdate/', function.editdate),  # 编辑时间
    path('conformeditdate/', function.conformeditdate),  # 确认编辑时间
    path('conformdeldate/', function.conformdeldate),  # 确认删除时间

    # 查看被测系统信息
    re_path(r'shsystem/$', views.shsystem, name='shsystem'),  # 系统列表
    re_path(r'shsystem/(?P<pk>\d+)/$', views.shsystem),
    path('editsystem/', function.editsystem, name='editsystem'),  # 编辑系统
    path('conformeditsystem/', function.conformeditsystem, name='conformeditsystem'),  # 确认编辑系统
    path('conformdelsystem/', function.conformdelsystem, name='conformdelsystem'),  # 确认删除系统

    # 查看被测项目信息
    path('project/', views.project, name='project'),  # 项目列表
    path('addproject/', function.addproject, name='addproject'),  # 增加项目
    path('download1/', function.download1),  # 下载到excel
    path('apply_pronum/', djcp_view.apply_pronum),  # 申请项目编号
    path('signature_and_seal/', djcp_view.signature_and_seal),  # 签字盖章
    path('end_document/', djcp_view.end_document),  # 收尾文件
    path('Download_assistant/', function.Download_assistant, name='Download_assistant'),  # 下载测评小助手
    path('conformdelproject/', function.conformdelproject, name='conformdelproject'),  # 确认删除项目

    # 奖金管理
    path('bonus/', views.bonus, name='bonus'),  # 项目列表
    path('insertVal/', bouns_view.insertVal, name='insertVal'),  # 插入输入框值
    path('bonus_add/', bouns_view.bonus_add, name='bonus_add'),  # 添加奖金
    path('bonus_edit/', bouns_view.bonus_edit, name='bonus_edit'),  # 编辑奖金
    path('bonus_conformedit/', bouns_view.bonus_conformedit, name='bonus_conformedit'),  # 确认编辑奖金
    path('bonus_conformdel/', bouns_view.bonus_conformdel, name='bonus_conformdel'),  # 确认删除联系人
    path('download_pdf/', bouns_view.download_pdf, name='download_pdf'),  # 下载合同源文件
    path('output_excel/', bouns_view.output_excel, name='output_excel'),  # 下载excel

    # 信息调查表
    path('Information_download/', views.Information_download, name='Information_download'),  # 生成信息调查表
    path('Information_edit/', djcp_info.Information_edit, name='Information_edit'),  # 弹出信息调查表模态框并将信息填充到信息调查表中
    path('Information_add/', djcp_info.Information_add, name='Information_add'),  # 添加信调表并将内容存放到数据库中
    path('downloadinfo/', djcp_info.downloadinfo, name='downloadinfo'),  # 下载信息调查表
    # 测评方案
    path('upload_case/', views.upload_case, name='upload_case'),  # 上传测评方案
    path('insert_case/', djcp_case.insert_case, name='insert_case'),  # 插入信息到测评方案中
    path('create_case/', djcp_case.create_case, name='create_case'),  # 生成测评方案
    path('download_case/', djcp_case.download_case, name='download_case'),  # 下载测评方案

]
