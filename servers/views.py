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
            status          = form_data.get('status', '')
            cpu_model       = form_data.get('cpu_model', '')
            num_cpus        = '' if form_data.get('num_cpus',0 ) == None else int(form_data.get('num_cpus',0 ))
            mem_total       = '' if form_data.get('mem_total',0 ) == None else int(form_data.get('mem_total',0 ))
            # num_cpus        = form_data.get('num_cpus','' )
            # mem_total       = form_data.get('mem_total','' )
            os              = form_data.get('os', '')
            productname     = form_data.get('productname', '')
            manufacturer    = form_data.get('manufacturer', '')
            ipaddr          = form_data.get('ipaddr', '')

            queryset = BaseInfo.objects.filter(hostname__icontains=hostname,
                                                status__icontains=status,
                                                os__icontains=os,
                                                productname__icontains=productname,
                                                manufacturer__icontains=manufacturer,
                                                interfaces__ipaddr__icontains=ipaddr
                                                ).distinct()

            if mem_total:
                queryset = queryset.filter(mem_total=mem_total)

            if num_cpus:
                queryset = queryset.filter(num_cpus=num_cpus)

            machine_list = get_machine_info(queryset.order_by('hostname'))
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

def server_view(request, hostname):
    page_title='服务器详情'
    tmp = []
    machine_instance = BaseInfo.objects.get(hostname=hostname)
    tmp.append(machine_instance)
    machine_instance = get_machine_info(tmp)
    return render(request, 'servers/view.html', locals())



# def view_servers(request, asset):
#     page_title='服务器详情'
#     servers_instance = Servers.objects.get(asset = asset)
#     form = ServersForm(None, instance = servers_instance)
#     # form.fields['asset'].widget.attrs['readonly'] = True
#     for field in servers_instance._meta.get_all_field_names():
#         if field != 'status':
#             form.fields[field].widget.attrs['readonly'] = True
#         else:
#             form.fields[field].widget.attrs['disabled'] = True
#
#     list_log = ModLog.objects.filter(asset = asset, typename="Servers").order_by('-mtime')
#     t=get_template('assets/view_servers.html')
#     c=RequestContext(request,locals())
#     return HttpResponse(t.render(c))

