#coding=utf8
__author__ = 'liangnaihua'

from django import forms
#from models import *

class SearchMachineForm(forms.Form):
    hostname    = forms.CharField(label='主机名', max_length=60, required=False)
    # status      = forms.CharField(label='状态', max_length=20, required=False)
    status      = forms.ChoiceField(label='状态', choices=[('True','True'),('False','False')],required=False)
    cpu_model   = forms.CharField(label='CPU 型号', max_length=100, required=False)
    num_cpus    = forms.IntegerField(label='CPU 数量', required=False)
    mem_total   = forms.IntegerField(label='内存', required=False)
    os          = forms.CharField(label='操作系统', max_length=150, required=False)
    productname = forms.CharField(label='服务器型号', max_length=100, required=False)
    manufacturer= forms.CharField(label='品牌', max_length=100, required=False)
    ipaddr      = forms.CharField(label='IP地址', max_length=100, required=False)
