#coding=utf8
# Create your views here.

__author__ = 'liangnaihua'

from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models.query import QuerySet
from models import BaseInfo, DiskInfo, NetworkInfo, ErrorInfo, CheckError
from forms import SearchMachineForm
from tables import *
from django_tables2 import RequestConfig
import salt.config
import salt.key
import salt.client
from salt import runner
import salt
from assets.models import *
from assets.forms import *


def index(request):
    return render(request,'index.html')

# 获取服务器信息，汇总展示
def names(request):
    page_title='服务器汇总信息'
    machine_list = BaseInfo.objects.all()
    # machine_list = BaseInfo.objects.filter(hostname__contains='is13084905-06')
    return render(request, 'servers/names.html', locals())

# 获取服务器信息，列表展示
def server_list(request):
    page_title='服务器列表'
    if request.method == "GET":
        machine_form = SearchMachineForm(request.GET)
        if machine_form.is_valid():
            form_data       = machine_form.cleaned_data
            hostname        = form_data.get('hostname', '')
            status          = form_data.get('status', '')
            cpu_model       = form_data.get('cpu_model', '')
            num_cpus        = '' if form_data.get('num_cpus',0 ) == None else int(form_data.get('num_cpus',0 ))
            mem_total       = '' if form_data.get('mem_total',0 ) == None else int(form_data.get('mem_total',0 ))
            os              = form_data.get('os', '')
            productname     = form_data.get('productname', '')
            manufacturer    = form_data.get('manufacturer', '')
            ipaddr          = form_data.get('ipaddr', '')

            # 根据相关信息过滤得到QuerySet：machine_list, 由于得到queryset有重复，需要distinct()
            machine_list = BaseInfo.objects.filter(hostname__icontains=hostname,
                                                status__icontains=status,
                                                os__icontains=os,
                                                productname__icontains=productname,
                                                manufacturer__icontains=manufacturer,
                                                interfaces__ipaddr__icontains=ipaddr
                                                ).distinct()

            # 如果mem_total 和 num_cpus 有值，再次进行过滤
            if mem_total:
                machine_list = machine_list.filter(mem_total__range=((mem_total-1)*1024, (mem_total+1)*1024))

            if num_cpus:
                machine_list = machine_list.filter(num_cpus=num_cpus)

            #分页
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
    else:
        machine_form = SearchMachineForm()
        return render(request, 'servers/list.html', locals())

# 服务器详细信息
def server_view(request, hostname):
    page_title='服务器详情'
    # machine_list = BaseInfo.objects.filter(hostname=hostname)
    # machine_instance =  machine_list[0] if machine_list else ''
    machine_instance = BaseInfo.objects.get(hostname=hostname)

    # asset info
    try:
        server_instance = Server.objects.get(hostname=machine_instance.hostname)
    except:
        server_instance = None

    if server_instance:
        device_instance = server_instance.asset
        maninfo_instance = device_instance.maninfo
        device_form = DeviceForm(None, instance = device_instance)
        server_form = ServerForm(None, instance = server_instance)
        maninfo_form = ManInfoForm(None, instance = maninfo_instance)
        for field in device_form.fields.keys():
            device_form.fields[field].widget.attrs['disabled'] = True
        for field in server_form.fields.keys():
            server_form.fields[field].widget.attrs['disabled'] = True
        for field in maninfo_form.fields.keys():
            maninfo_form.fields[field].widget.attrs['disabled'] = True

    return render(request, 'servers/view.html', locals())

# 获取服务器信息，列表展示
def server_errors(request):
    page_title='服务器错误信息'
    errors = ErrorInfo.objects.all()
    return render(request, 'servers/errors.html', locals())

# 获取offline 列表
def salt_status():
    # __opts__ = salt.config.master_config('/etc/salt/master')
    # client = salt.client.LocalClient(__opts__['conf_file'])
    # minions = client.cmd('*', 'test.ping', timeout=__opts__['timeout'])
    # key = salt.key.Key(__opts__)
    # keys = key.list_keys()
    # ret = {}
    # ret['up'] = sorted(minions)
    # ret['down'] = sorted(set(keys['minions']) - set(minions))
    # return ret['down']
    opts = salt.config.master_config('/etc/salt/master')
    runner = salt.runner.RunnerClient(opts)
    ret = runner.cmd('manage.down', [])
    return ret


# 暂时offline服务器
def server_offline(request):
    page_title='离线服务器列表'
    offline_list = salt_status()

    #分页
    count = len(offline_list)
    paginator = Paginator(offline_list ,15)

    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        offline_list = paginator.page(page)
    except :
        offline_list = paginator.page(paginator.num_pages)
    return render(request, 'servers/offline.html', locals())

# offline服务器重启minions信息
def server_checkerror(request):
    page_title='重启Salt minions错误信息'
    error_list = CheckError.objects.all().order_by('time')
    error_table = CheckErrorTable(error_list)
    RequestConfig(request).configure(error_table)
    return render(request,'servers/checkerror.html', locals())

def index(request):
    return render(request, 'index.html', locals())