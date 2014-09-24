#coding=utf8
# Create your views here.

__author__ = 'liangnaihua'

from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models.query import QuerySet
from models import BaseInfo, DiskInfo, NetworkInfo, ErrorInfo
from forms import SearchMachineForm


def index(request):
    return render(request,'index.html')


# 获取服务器信息
# tmp是存储服务器信息的字典，并将当前值加入到info列表
def get_machine_info(queryset):
    machine_list = []
    # for machine in BaseInfo.objects.all().order_by('hostname'):
    # for machine in BaseInfo.objects.filter(hostname__contains='is13084905-06'):
    for machine in queryset:
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
        machine_list.append(tmp)

    return machine_list

# 获取服务器信息，并汇总展示
def names(request):
    # for machine in BaseInfo.objects.all().order_by('hostname'):
    # for machine in BaseInfo.objects.filter(hostname__contains='is13084905-06'):
    page_title='服务器汇总信息'
    machine_list = get_machine_info(BaseInfo.objects.filter(hostname__contains='is13084905-06'))
    return render(request, 'servers/names.html', locals())

# 获取服务器信息，列表展示
def server_list(request):
    page_title='服务器列表'
    if request.method == "GET":
        machine_form = SearchMachineForm(request.GET)
        if machine_form.is_valid():
            form_data       = machine_form.cleaned_data
            hostname        = form_data.get('hostname', '')
            status          = form_data.get('hostname', '')
            cpu_model       = form_data.get('hostname', '')
            num_cpus        = form_data.get('hostname', '')
            mem_total       = form_data.get('mem_total', '')
            os              = form_data.get('os', '')
            productname     = form_data.get('productname', '')
            manufacturer    = form_data.get('manufacturer', '')
            ipaddr          = form_data.get('ipaddr', '')

            if len(ipaddr) == 0:
                queryset = BaseInfo.objects.filter(hostname__icontains=hostname,
                                                     status__icontains=status,
                                                     cpu_model__icontains=cpu_model,
                                                     num_cpus__icontains=num_cpus,
                                                     mem_total__icontains=mem_total,
                                                     os__icontains=os,
                                                     productname__icontains=productname,
                                                     manufacturer__icontains=manufacturer)
            else:
                hostname_list = []
                for item in NetworkInfo.objects.filter(ipaddr__icontains=ipaddr).order_by("hostname_id"):
                    hostname_list.append(item.hostname)
                hostname_set = list(set(hostname_list))





    machine_list = get_machine_info()
    count = len(machine_list)
    paginator = Paginator(machine_list ,15)

    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        machine_list = paginator.page(page)
    except :
        machine_list = paginator.page(paginator.num_pages)

    return render(request, 'servers/list.html', locals())

