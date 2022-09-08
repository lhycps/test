import re

from django import forms
from django.core.exceptions import ValidationError
from django.forms import widgets


class UserInfoForm(forms.Form):
    '''客户方联系人信息表'''
    name = forms.CharField(max_length=32, label='联系人名字：',
                           widget=widgets.TextInput(attrs={'class': 'input-style-1'}))
    email = forms.EmailField(max_length=32, label='联系人邮箱：', widget=widgets.EmailInput(attrs={'class': 'input-style-1'}))
    post = forms.CharField(max_length=32, label='联系人岗位：',
                           widget=widgets.TextInput(attrs={'class': 'input-style-1 '}))
    phone = forms.CharField(max_length=32, label='联系人手机号：',
                            widget=widgets.NumberInput(attrs={'class': 'input-style-1'}))
    telephone = forms.CharField(max_length=32, label='联系人电话：',
                                widget=widgets.NumberInput(attrs={'class': 'input-style-1'}))

    def clean_phone(self):  # 函数必须以clean_开头
        """
        通过正则表达式验证手机号码是否合法
        """
        phone = self.cleaned_data['phone']
        phone_regex = r'^1[34578]\d{9}$'
        p = re.compile(phone_regex)
        if p.match(phone):
            return phone
        else:
            raise forms.ValidationError('手机号码非法', code='invalid mobile')


class GmanagerInfoForm(forms.Form):
    '''客户方负责人信息表'''
    gname = forms.CharField(max_length=32, label='负责人名字：',
                            widget=widgets.TextInput(attrs={'class': 'input-style-1'}))
    gemail = forms.CharField(max_length=32, label='负责人邮箱：',
                             widget=widgets.TextInput(attrs={'class': 'input-style-1'}))
    gpost = forms.CharField(max_length=32, label='负责人岗位：',
                            widget=widgets.TextInput(attrs={'class': 'input-style-1'}))
    gphone = forms.CharField(max_length=32, label='负责人手机号：',
                             widget=widgets.TextInput(attrs={'class': 'input-style-1'}))
    gtelephone = forms.CharField(max_length=32, label='负责人电话：',
                                 widget=widgets.TextInput(attrs={'class': 'input-style-1'}))

    # def clean_gphone(self):  # 函数必须以clean_开头
    #     """
    #     通过正则表达式验证手机号码是否合法
    #     """
    #     gphone = self.cleaned_data['gphone']
    #     phone_regex = r'^1[34578]\d{9}$'
    #     p = re.compile(phone_regex)
    #     if p.match(gphone):
    #         return gphone
    #     else:
    #         raise forms.ValidationError('手机号码非法', code='invalid mobile')


class UnitInfo(forms.Form):
    '''客户方单位信息表'''
    unit_name = forms.CharField(max_length=32, label='单位名称：',
                                widget=widgets.TextInput(attrs={'class': 'input-style-1'}))
    address = forms.EmailField(max_length=132, label='单位地址：',
                               widget=widgets.EmailInput(attrs={'class': 'input-style-1'}))
    nature = forms.CharField(max_length=32, label='单位性质：',
                             widget=widgets.TextInput(attrs={'class': 'input-style-1'}))
    department = forms.CharField(max_length=32, label='部门：',
                                 widget=widgets.TextInput(attrs={'class': 'input-style-1'}))
    code = forms.CharField(max_length=32, label='邮编：',
                           widget=widgets.NumberInput(attrs={'class': 'input-style-1'}))
    desc = forms.CharField(max_length=32, label='单位简介：',
                           widget=widgets.Textarea(attrs={'class': 'input-style-1'}))
