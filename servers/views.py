#coding=utf8
# Create your views here.

__author__ = 'liangnaihua'

from models import *
from django.shortcuts import render
from django.core.paginator import Paginator

def index(request):
    return render(request,'index.html')


# 获取服务器信息
# tmp是存储服务器信息的字典，并将当前值加入到info列表
def getmachineinfo():
    info = []
    # machineSet = BaseInfo.objects.all()
    # for machine in BaseInfo.objects.all().order_by('hostname'):
    for machine in BaseInfo.objects.filter(hostname__contains='is13084905-06'):
        tmp                        = {}
        tmp['hostname']            = machine.hostname
        tmp['status']              = machine.status
        tmp['cpu_model']           = machine.cpu_model
        tmp['num_cpus']            = machine.num_cpus
        tmp['mem_total']           = machine.mem_total
        tmp['os']                  = machine.os
        tmp['productname']         = machine.productname
        tmp['manufacturer']        = machine.manufacturer
        tmp['disks']               = machine.disks.all().order_by('mount')
        tmp['interfaces']          = machine.interfaces.all().order_by('interface')
        info.append(tmp)

    return info

# 获取服务器信息，并汇总展示
def names(request):
    page_title='服务器汇总信息'
    info = getmachineinfo()
    return render(request, 'servers/names.html', locals())

# 获取服务器信息，列表展示
def serverlist(request):
    page_title='服务器列表'
    info = getmachineinfo()
    count = len(info)
    paginator = Paginator(info ,15)

    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        list_items = paginator.page(page)
    except :
        list_items = paginator.page(paginator.num_pages)

    return render(request, 'servers/list.html', locals())

