# Generated by Django 2.1.5 on 2022-08-23 08:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Area',
            fields=[
                ('areaid', models.IntegerField(primary_key=True, serialize=False)),
                ('areaname', models.CharField(max_length=50)),
                ('parentid', models.IntegerField()),
                ('arealevel', models.IntegerField()),
                ('status', models.IntegerField()),
            ],
            options={
                'db_table': 'area',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='CreateContract',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unit_name', models.CharField(max_length=80, verbose_name='单位名称')),
                ('sys_name', models.CharField(max_length=255, verbose_name='系统名称')),
                ('address', models.CharField(max_length=255, verbose_name='单位地址')),
                ('code', models.CharField(max_length=30, verbose_name='邮编')),
                ('name', models.CharField(max_length=30, verbose_name='联系人姓名')),
                ('phone', models.CharField(max_length=30, verbose_name='联系人电话')),
                ('bank', models.CharField(max_length=255, verbose_name='开户行')),
                ('bankcardnum', models.CharField(max_length=255, verbose_name='银行卡号')),
                ('level', models.CharField(choices=[('二级', '二级'), ('三级', '三级')], max_length=30, verbose_name='系统级别')),
                ('money', models.DecimalField(decimal_places=2, default=0, max_digits=8, verbose_name='合同金额')),
                ('province', models.CharField(max_length=255, verbose_name='省')),
                ('city', models.CharField(max_length=255, verbose_name='市')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='人员')),
            ],
        ),
    ]