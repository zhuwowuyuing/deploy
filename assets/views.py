#coding=utf8
import copy
import datetime
from django.shortcuts import render
from django.core.paginator import Paginator
from models import Devices, Server, Status, ManInfo
from forms import *
from django.http import HttpResponse, HttpResponseRedirect
# from forms import AssetSearch, AssetForm
# Create your views here.

# 新建状态记录
def status_create(request):
    page_title='添加使用状态'
    form = StatusForm(request.POST or None)
    if form.is_valid():
        form.save()
        form = StatusForm()

    return render(request, 'assets/status_create.html', locals())

# 状态列表
def status_list(request):
    page_title='使用状态列表'
    list_items = Status.objects.all()
    paginator = Paginator(list_items ,15)


    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        list_items = paginator.page(page)
    except :
        list_items = paginator.page(paginator.num_pages)

    return render(request, 'assets/status_list.html', locals())

# 编辑使用状态
def status_edit(request, status):
    page_title='编辑使用状态'
    status_instance = Status.objects.get(status = status)

    form = StatusForm(request.POST or None, instance = status_instance)

    if form.is_valid():
        form.save()
    return render(request, 'assets/status_edit.html', locals())

def server_list(request):
    page_title='资产信息列表'
    list_items = Devices.objects.all()
    count = list_items.count()
    paginator = Paginator(list_items ,15)

    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        list_items = paginator.page(page)
    except :
        list_items = paginator.page(paginator.num_pages)

    return render(request, 'assets/server_list.html', locals())

def server_create(request):
    page_title='新增资产记录'
    prefix_device   = 'device_form'
    prefix_server   = 'server_form'
    prefix_maninfo  = 'maninfo_form'

    if request.method == "POST":
        device_form     = DeviceForm(request.POST)
        server_form     = ServerForm(request.POST)
        maninfo_form    = ManInfoForm(request.POST)

        if device_form.is_valid() and server_form.is_valid() and maninfo_form.is_valid():
            device = device_form.save()
            server = server_form.save(commit=False)
            maninfo = maninfo_form.save(commit=False)
            server.asset = device
            server.save()
            maninfo.asset = device
            maninfo.save()
    else:
        device_form     = DeviceForm(prefix=prefix_device)
        server_form     = ServerForm(prefix=prefix_server)
        maninfo_form    = ManInfoForm(prefix=prefix_maninfo)

    return render(request, 'assets/server_create.html', locals())
#
# def server_create(request):
#     page_title='新增资产记录'
#     if request.method == "POST":
#         asset_form = AssetForm(request.POST)
#         if asset_form.is_valid():
#             data = asset_form.cleaned_data
#             asset = data.get('asset','')
#             asset_old = data.get('asset_old','')
#             district = data.get('district','')
#             company = data.get('company','')
#             type = data.get('type','')
#             subtype = data.get('subtype','')
#             status = '' if data.get('status','') == None else data.get('status')
#             manufacturer = data.get('manufacturer','')
#             model = data.get('model','')
#             serialno = data.get('serialno','')
#             size = data.get('size', '')
#             cpu = data.get('cpu', '')
#             harddisk = data.get('harddisk','')
#             ram = data.get('ram','')
#             os = data.get('os','')
#             building = data.get('building','')
#             location = data.get('location','')
#             consignee = data.get('consignee','')
#             hostname = data.get('hostname','')
#             dept = data.get('dept','')
#             business = data.get('business','')
#             ownername = data.get('ownername','')
#             administrator = data.get('administrator','')
#             warehousedate = data.get('warehousedate','')
#             receivedate = data.get('receivedate','')
#             warrantyexpirationdate = data.get('warrantyexpirationdate','')
#             scrapDate = data.get('scrapDate','')
#             purchase_date = data.get('purchase_date','')
#             purchase_cost = 0 if not  data.get('purchase_cost','')  else float(data.get('purchase_cost'))
#             accounting_date = data.get('accounting_date','')
#             account_cost = 0 if not data.get('account_cost','')  else float(data.get('account_cost'))
#             vendor = data.get('vendor','')
#             vendor_contacts = data.get('vendor_contacts','')
#             accounting_info = data.get('accounting_info','')
#             order_list = data.get('order_list','')
#             changeInfo = data.get('changeInfo','')
#             comment = data.get('comment','')
#
#             if not changeInfo:
#                 changeInfo = "%s 新增资产信息"%(datetime.date.today()).strftime('%Y-%m-%d')
#
#             new_device = Devices(asset=asset, asset_old=asset_old, district=district, company=company,status=status, \
#                                  type=type, subtype=subtype, manufacturer=manufacturer, model=model, serialno=serialno, \
#                                  changeInfo=changeInfo, comment=comment)
#             new_device.save()
#
#             new_server = Server(asset=new_device, size=size, cpu=cpu, harddisk=harddisk, ram=ram, os=os, building=building, \
#                                 location=location, consignee=consignee, hostname=hostname, dept=dept, business=business, \
#                                 ownername=ownername)
#             new_server.save()
#
#             new_maninfo = ManInfo(asset=new_device, administrator=administrator, warehousedate=warehousedate, receivedate=receivedate, \
#                                   warrantyexpirationdate=warrantyexpirationdate, scrapDate=scrapDate, purchase_date=purchase_date, \
#                                   purchase_cost=purchase_cost, accounting_date=accounting_date, account_cost=account_cost, \
#                                   vendor=vendor, vendor_contacts=vendor_contacts, accounting_info=accounting_info, \
#                                   order_list=order_list)
#             new_maninfo.save()
#     else:
#         asset_form = AssetForm()
#     return render(request, 'assets/server_create.html', locals())


# 编辑 assets
def server_edit(request, asset):
    page_title='编辑服务器信息'
    device_instance     = Devices.objects.get(asset =asset)
    server_instance     = Server.objects.get(asset = asset)
    maninfo_instance    = ManInfo.objects.get(asset = asset)

    old_device_instance = copy.deepcopy(device_instance)
    old_server_instance = copy.deepcopy(server_instance)
    old_maninfo_instance = copy.deepcopy(maninfo_instance)
    list_log = ModLog.objects.filter(asset = asset, typename="服务器").order_by('-mtime')
    prefix_device   = "device_form"
    prefix_server   = "server_form"
    prefix_maninfo   = "maninfo_form"

    device_form     = DeviceForm(request.POST or None, instance = device_instance)
    server_form     = ServerForm(request.POST or None, instance = server_instance)
    maninfo_form    = ManInfoForm(request.POST or None, instance = maninfo_instance)

    # device_form     = DeviceForm(request.POST or None, instance = device_instance, prefix=prefix_device)
    # server_form     = ServerForm(request.POST or None, instance = server_instance, prefix=prefix_server)
    # maninfo_form    = ManInfoForm(request.POST or None, instance = maninfo_instance, prefix=prefix_maninfo)

    if device_form.is_valid() and server_form.is_valid() and maninfo_form.is_valid():
        if device_form.has_changed():
            for filed in device_form.changed_data:
                log = ModLog(typename="服务器",asset=device_instance.asset, mtime= datetime.datetime.now(),\
                             field=device_instance._meta.get_field(filed).verbose_name,\
                             oldvalue=old_device_instance.__dict__[filed], newvalue=device_form.data.get('%s-%s'%(prefix_device, filed),''), \
                             moduser=request.user)
                log.save()

        if server_form.has_changed():
            for filed in server_form.changed_data:
                log = ModLog(typename="服务器",asset=server_instance.asset, mtime= datetime.datetime.now(),\
                             field=server_instance._meta.get_field(filed).verbose_name,\
                             oldvalue=old_server_instance.__dict__[filed], newvalue=server_form.data.get('%s-%s'%(prefix_server, filed),''), \
                             moduser=request.user)
                log.save()

        if maninfo_form.has_changed():
            for filed in maninfo_form.changed_data:
                log = ModLog(typename="服务器",asset=maninfo_instance.asset, mtime= datetime.datetime.now(),
                             field=maninfo_instance._meta.get_field(filed).verbose_name,
                             oldvalue=old_maninfo_instance.__dict__[filed], newvalue=maninfo_form.data.get('%s-%s'%(prefix_maninfo, filed),''), \
                             moduser=request.user)
                log.save()

        device = device_form.save()
        server = server_form.save(commit=False)
        maninfo = maninfo_form.save(commit=False)
        server.asset = device
        server.save()
        maninfo.asset = device
        maninfo.save()

    return render(request, 'assets/server_edit.html', locals())

#
def server_view(request, asset):
    page_title='服务器详情'
    typename = '服务器'
    device_instance = Devices.objects.get(asset = asset)
    server_instance = device_instance.server
    maninfo_instance = device_instance.maninfo
    device_form = DeviceForm(None, instance = device_instance)
    server_form = ServerForm(None, instance = server_instance)
    maninfo_form = ManInfoForm(None, instance = maninfo_instance)

    list_log = ModLog.objects.filter(asset = asset, typename=typename).order_by('-mtime')
    return render(request, 'assets/server_view.html', locals())

#
def server_delete(request, asset):
    typename="服务器"
    Devices.objects.get(asset = asset).delete()
    log = ModLog(typename=typename, asset=asset, mtime= datetime.datetime.now(), \
                              moduser=request.user, comment="删除服务器")
    log.save()
    searchform = AssetSearch()
    return HttpResponseRedirect("/assets/server/search/",locals())


def server_search(request):
    page_title='搜索服务器'
    if request.method == "GET":
        searchform = AssetSearch(request.GET)
        if searchform.is_valid():
            data = searchform.cleaned_data
            asset = data.get('asset','')
            asset_old = data.get('asset_old','')
            type = data.get('type','')
            subtype = data.get('subtype','')
            manufacturer = data.get('manufacturer','')
            model = data.get('model','')
            building = data.get('building','')
            location = data.get('location','')
            consignee = data.get('consignee','')
            hostname = data.get('hostname','')
            vendor = data.get('vendor','')
            status = '' if data.get('status','') == None else data.get('status')
            list_items = Devices.objects.filter(asset__icontains = asset,
                                                asset_old__icontains = asset_old,
                                                type__icontains = type,
                                                subtype__icontains = subtype,
                                                manufacturer__icontains = manufacturer,
                                                model__icontains = model,
                                                server__building__icontains = building,
                                                server__location__icontains = location,
                                                server__consignee__icontains = consignee,
                                                server__hostname__icontains = hostname,
                                                maninfo__vendor__icontains = vendor,
                                                status__status__icontains = status
                                                )
            count = list_items.count()
            paginator = Paginator(list_items ,15)

            try:
                page = int(request.GET.get('page', '1'))
            except ValueError:
                page = 1
            try:
                list_items = paginator.page(page)
            except :
                list_items = paginator.page(paginator.num_pages)
    else:
        searchform = AssetSearch()

    return render(request, "assets/server_search.html", locals())