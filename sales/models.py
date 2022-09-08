from django.db import models


# Create your models here.
class CreateContract(models.Model):
    '''生成合同的数据库'''
    cholevel = (("二级", "二级"), ("三级", "三级"))
    unit_name = models.CharField(max_length=80, verbose_name='单位名称')
    sys_name = models.CharField(max_length=255, verbose_name='系统名称')
    address = models.CharField(max_length=255, verbose_name='单位地址')
    code = models.CharField(max_length=30, verbose_name='邮编')
    name = models.CharField(max_length=30, verbose_name='联系人姓名')
    phone = models.CharField(max_length=30, verbose_name='联系人电话')
    bank = models.CharField(max_length=255, verbose_name='开户行')
    bankcardnum = models.CharField(max_length=255, verbose_name='银行卡号')
    level = models.CharField(max_length=30, verbose_name='系统级别', choices=cholevel)
    money = models.DecimalField(max_digits=8, decimal_places=2, default=0, verbose_name='合同金额')
    province = models.CharField(max_length=255, verbose_name='省')
    city = models.CharField(max_length=255, verbose_name='市')
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    user = models.ForeignKey('system.UserInfo', on_delete=models.CASCADE, verbose_name='人员')


class Area(models.Model):
    '''全国区化表'''
    areaid = models.IntegerField(primary_key=True)
    areaname = models.CharField(max_length=50)
    parentid = models.IntegerField()
    arealevel = models.IntegerField()
    status = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'area'
