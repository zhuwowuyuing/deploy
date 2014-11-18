#coding=utf8
import copy
import types
import datetime
from django.shortcuts import render
from django.core.paginator import Paginator
from models import Devices, Server, Status, ManInfo
from forms import *
from django.http import HttpResponse, HttpResponseRedirect
from tables import *
from django_tables2 import RequestConfig
from servers.models import *
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
    list_items = StatusTable(list_items)
    RequestConfig(request).configure(list_items)
    return render(request, 'assets/status_list.html', locals())

# 编辑使用状态
def status_edit(request, id):
    page_title='编辑使用状态'
    status_instance = Status.objects.get(id = id)

    form = StatusForm(request.POST or None, instance = status_instance)

    if form.is_valid():
        form.save()
    return render(request, 'assets/status_edit.html', locals())

def status_del(request, id):
    Status.objects.get(id = id).delete()
    return HttpResponseRedirect("/assets/status/list/", locals())

# 新建状态记录
def type_create(request):
    page_title='添加设备类别'
    form = TypeForm(request.POST or None)
    if form.is_valid():
        form.save()
        form = TypeForm()

    return render(request, 'assets/type_create.html', locals())

# 状态列表
def type_list(request):
    page_title='设备类别列表'
    list_items = Type.objects.all()
    list_items = TypeTable(list_items)
    RequestConfig(request).configure(list_items)
    return render(request, 'assets/type_list.html', locals())


# 编辑使用状态
def type_edit(request, id):
    page_title='编辑设备类别'
    instance = Type.objects.get(id = id)
    form = TypeForm(request.POST or None, instance = instance)
    if form.is_valid():
        form.save()
    return render(request, 'assets/type_edit.html', locals())

def type_del(request, id):
    Type.objects.get(id = id).delete()
    return HttpResponseRedirect("/assets/type/list/", locals())


# 新建状态记录
def subtype_create(request):
    page_title='添加设备子类别'
    form = SubtypeForm(request.POST or None)
    if form.is_valid():
        form.save()
        form = SubtypeForm()
    return render(request, 'assets/type_create.html', locals())

# 状态列表
def subtype_list(request):
    page_title='设备子类别列表'
    list_items = Subtype.objects.all()
    list_items = SubtypeTable(list_items)
    RequestConfig(request).configure(list_items)
    return render(request, 'assets/type_list.html', locals())


# 编辑使用状态
def subtype_edit(request, id):
    page_title='编辑设备子类别'
    instance = Subtype.objects.get(id = id)

    form = SubtypeForm(request.POST or None, instance = instance)

    if form.is_valid():
        form.save()
    return render(request, 'assets/subtype_edit.html', locals())

def subtype_del(request, id):
    Subtype.objects.get(id = id).delete()
    return HttpResponseRedirect("/assets/subtype/list/", locals())

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
    page_title='新增服务器记录'

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
        device_form     = DeviceForm()
        server_form     = ServerForm()
        maninfo_form    = ManInfoForm()

    return render(request, 'assets/server_create.html', locals())

def modinfo(type, asset, field_list, old_obj, new_obj, username):
    for field in field_list:
        log = ModLog(typename = type,asset=asset,     \
                     mtime = datetime.datetime.now(), \
                     field = old_obj._meta.get_field(field).verbose_name, \
                     oldvalue = getattr(old_obj, field), \
                     newvalue = getattr(new_obj, field), \
                     moduser = username)
        log.save()

# 编辑 assets
def server_edit(request, asset):
    page_title='编辑服务器信息'
    typename = "服务器"
    device_instance     = Devices.objects.get(asset =asset)
    server_instance     = Server.objects.get(asset = asset)
    maninfo_instance    = ManInfo.objects.get(asset = asset)

    old_device_instance = copy.deepcopy(device_instance)
    old_server_instance = copy.deepcopy(server_instance)
    old_maninfo_instance = copy.deepcopy(maninfo_instance)
    list_log = ModLog.objects.filter(asset = asset, typename=typename).order_by('-mtime')

    device_form     = DeviceForm(request.POST or None, instance = device_instance)
    server_form     = ServerForm(request.POST or None, instance = server_instance)
    maninfo_form    = ManInfoForm(request.POST or None, instance = maninfo_instance)
    device_change_fields    = []
    server_change_fields    = []
    maninfo_change_fields   = []

    if device_form.is_valid() and server_form.is_valid() and maninfo_form.is_valid():
        if device_form.has_changed():
            device_change_fields = device_form.changed_data
        if server_form.has_changed():
            server_change_fields = server_form.changed_data
        if maninfo_form.has_changed():
            maninfo_change_fields = maninfo_form.changed_data

        device = device_form.save()
        server = server_form.save(commit=False)
        maninfo = maninfo_form.save(commit=False)
        server.asset = device
        server.save()
        maninfo.asset = device
        maninfo.save()

    if device_change_fields:
        modinfo(typename, asset, device_change_fields , old_device_instance, Devices.objects.get(asset =asset), request.user)
    if server_change_fields:
        modinfo(typename, asset, server_change_fields , old_server_instance, Server.objects.get(asset =asset), request.user)
    if maninfo_change_fields:
        modinfo(typename, asset, maninfo_change_fields , old_maninfo_instance, ManInfo.objects.get(asset =asset), request.user)

    try:
        machine_instance = BaseInfo.objects.get(hostname=Server.objects.get(asset=asset).hostname)
    except:
        machine_instance = None

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

    for field in device_form.fields.keys():
            device_form.fields[field].widget.attrs['disabled'] = True
    for field in server_form.fields.keys():
            server_form.fields[field].widget.attrs['disabled'] = True
    for field in maninfo_form.fields.keys():
            maninfo_form.fields[field].widget.attrs['disabled'] = True

    if server_instance.hostname:
        try:
            machine_instance = BaseInfo.objects.get(hostname=server_instance.hostname)
        except:
            machine_instance = None
    else:
        machine_instance = None

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
            status = data.get('status','')
            type = data.get('type','')
            subtype = data.get('subtype','')
            manufacturer = data.get('manufacturer','')
            model = data.get('model','')
            building = data.get('building','')
            location = data.get('location','')
            consignee = data.get('consignee','')
            hostname = data.get('hostname','')
            vendor = data.get('vendor','')

            list_items = Devices.objects.filter(asset__icontains = asset,
                                                asset_old__icontains = asset_old,
                                                manufacturer__icontains = manufacturer,
                                                model__icontains = model,
                                                server__building__icontains = building,
                                                server__location__icontains = location,
                                                server__consignee__icontains = consignee,
                                                server__hostname__icontains = hostname,
                                                maninfo__vendor__icontains = vendor
                                                )

            if status:
                list_items = list_items.filter(status=status)
            if  type:
                list_items = list_items.filter(type=type)
            if subtype:
                list_items = list_items.filter(subtype=subtype)


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

def modlog_list(request):
    page_title='修改历史'
    if request.method == "GET":
        modlogform = ModLogSearchForm(request.GET)

        if modlogform.is_valid():
            data = modlogform.cleaned_data
            typename = data.get('typename', '')
            asset = data.get('asset', '')
            moduser = data.get('moduser', '')
            field = data.get('field', '')
            comment = data.get('comment', '')
            starttime = data.get('starttime')
            endtime = datetime.datetime.now() if not data.get('endtime') else data.get('endtime')
            # if endtime == None:
            #     endtime = datetime.datetime.now()

            if starttime ==  None or starttime == 'None':
                list_items = ModLog.objects.filter(typename__icontains = typename,
                                                    asset__icontains = asset,
                                                    moduser__icontains = moduser,
                                                    field__icontains = field,
                                                    comment__icontains = comment,
                                                    mtime__lte=endtime
                                                    )
            else:
                list_items = ModLog.objects.filter(typename__icontains = typename,
                                                    asset__icontains = asset,
                                                    moduser__icontains = moduser,
                                                    field__icontains = field,
                                                    comment__icontains = comment,
                                                    mtime__range=(starttime, endtime)
                                                    )
            # count = list_items.count()
            # paginator = Paginator(list_items ,15)
            #
            # try:
            #     page = int(request.GET.get('page', '1'))
            # except ValueError:
            #     page = 1
            # try:
            #     list_items = paginator.page(page)
            # except :
            #     list_items = paginator.page(paginator.num_pages)
            #
            # return render(request, 'assets/modlog_list.html', locals())
            list_items = ModLogTable(list_items)
            RequestConfig(request).configure(list_items)
            return render(request, 'assets/modlog_list.html', locals())
    else:
        modlogform = ModLogSearchForm()
    return render(request, "assets/modlog_list.html", locals())

def network_list(request):
    return 0
def network_create(request):
    page_title='新增网络设备记录'

    if request.method == "POST":
        device_form     = DeviceForm(request.POST)
        network_form    = NetworkForm(request.POST)
        maninfo_form    = ManInfoForm(request.POST)

        if device_form.is_valid() and network_form.is_valid() and maninfo_form.is_valid():
            device = device_form.save()
            network = network_form.save(commit=False)
            maninfo = maninfo_form.save(commit=False)
            network.asset = device
            network.save()
            maninfo.asset = device
            maninfo.save()
    else:
        device_form     = DeviceForm()
        network_form    = NetworkForm()
        maninfo_form    = ManInfoForm()

    return render(request, 'assets/network_create.html', locals())

def network_edit(request, asset):
    page_title='编辑网络设备信息'
    typename = '网络设备'
    device_instance     = Devices.objects.get(asset =asset)
    network_instance     = Network.objects.get(asset = asset)
    maninfo_instance    = ManInfo.objects.get(asset = asset)

    old_device_instance = copy.deepcopy(device_instance)
    old_network_instance = copy.deepcopy(network_instance)
    old_maninfo_instance = copy.deepcopy(maninfo_instance)
    list_log = ModLog.objects.filter(asset = asset, typename=typename).order_by('-mtime')

    device_form     = DeviceForm(request.POST or None, instance = device_instance)
    network_form    = NetworkForm(request.POST or None, instance = network_instance)
    maninfo_form    = ManInfoForm(request.POST or None, instance = maninfo_instance)
    device_change_fields    = []
    network_change_fields    = []
    maninfo_change_fields   = []

    if device_form.is_valid() and network_form.is_valid() and maninfo_form.is_valid():
        if device_form.has_changed():
            device_change_fields = device_form.changed_data
        if network_form.has_changed():
            network_change_fields = network_form.changed_data
        if maninfo_form.has_changed():
            maninfo_change_fields = maninfo_form.changed_data

        device  = device_form.save()
        network = network_form.save(commit=False)
        maninfo = maninfo_form.save(commit=False)
        network.asset = device
        network.save()
        maninfo.asset = device
        maninfo.save()

    if device_change_fields:
        modinfo(typename, asset, device_change_fields , old_device_instance, Devices.objects.get(asset =asset), request.user)
    if network_change_fields:
        modinfo(typename, asset, network_change_fields , old_network_instance, Network.objects.get(asset =asset), request.user)
    if maninfo_change_fields:
        modinfo(typename, asset, maninfo_change_fields , old_maninfo_instance, ManInfo.objects.get(asset =asset), request.user)

    return render(request, 'assets/network_edit.html', locals())

def network_view(request, asset):
    page_title='网络设备详情'
    typename = '网络设备'
    device_instance = Devices.objects.get(asset = asset)
    network_instance = device_instance.network
    maninfo_instance = device_instance.maninfo
    device_form = DeviceForm(None, instance = device_instance)
    network_form = NetworkForm(None, instance = network_instance)
    maninfo_form = ManInfoForm(None, instance = maninfo_instance)

    for field in device_form.fields.keys():
            device_form.fields[field].widget.attrs['disabled'] = True
    for field in network_form.fields.keys():
            network_form.fields[field].widget.attrs['disabled'] = True
    for field in maninfo_form.fields.keys():
            maninfo_form.fields[field].widget.attrs['disabled'] = True

    list_log = ModLog.objects.filter(asset = asset, typename=typename).order_by('-mtime')
    return render(request, 'assets/network_view.html', locals())

def network_delete(request, asset):
    typename="网络设备"
    Devices.objects.get(asset = asset).delete()
    log = ModLog(typename=typename, asset=asset, mtime= datetime.datetime.now(), \
                              moduser=request.user, comment="删除网络设备")
    log.save()
    searchform = NetworkSearch()
    return HttpResponseRedirect("/assets/network/search/",locals())

def network_search(request):
    page_title='搜索网络设备'
    if request.method == "GET":
        searchform = NetworkSearch(request.GET)
        if searchform.is_valid():
            data = searchform.cleaned_data
            asset = data.get('asset','')
            asset_old = data.get('asset_old','')
            status = data.get('status','')
            type = data.get('type','')
            subtype = data.get('subtype','')
            manufacturer = data.get('manufacturer','')
            model = data.get('model','')
            building = data.get('building','')
            location = data.get('location','')
            consignee = data.get('consignee','')


            list_items = Devices.objects.filter(asset__icontains = asset,
                                                asset_old__icontains = asset_old,
                                                manufacturer__icontains = manufacturer,
                                                model__icontains = model,
                                                network__building__icontains = building,
                                                network__location__icontains = location,
                                                network__consignee__icontains = consignee,
                                                )

            if status:
                list_items = list_items.filter(status=status)
            if  type:
                list_items = list_items.filter(type=type)
            if subtype:
                list_items = list_items.filter(subtype=subtype)


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
        searchform = NetworkSearch()

    return render(request, "assets/network_search.html", locals())

def otheremq_list(request):
    return 0
def otheremq_create(request):
    page_title='新增其他设备记录'

    if request.method == "POST":
        device_form     = DeviceForm(request.POST)
        otheremq_form   = OtherEmqForm(request.POST)
        maninfo_form    = ManInfoForm(request.POST)

        if device_form.is_valid() and otheremq_form.is_valid() and maninfo_form.is_valid():
            device = device_form.save()
            otheremq = otheremq_form.save(commit=False)
            maninfo = maninfo_form.save(commit=False)
            otheremq.asset = device
            otheremq.save()
            maninfo.asset = device
            maninfo.save()
    else:
        device_form     = DeviceForm()
        otheremq_form   = OtherEmqForm()
        maninfo_form    = ManInfoForm()

    return render(request, 'assets/otheremq_create.html', locals())

def otheremq_edit(request, asset):
    page_title='编辑其他设备信息'
    typename = "其他设备"
    device_instance     = Devices.objects.get(asset =asset)
    otheremq_instance     = OtherEmq.objects.get(asset = asset)
    maninfo_instance    = ManInfo.objects.get(asset = asset)

    old_device_instance = copy.deepcopy(device_instance)
    old_otheremq_instance = copy.deepcopy(otheremq_instance)
    old_maninfo_instance = copy.deepcopy(maninfo_instance)
    list_log = ModLog.objects.filter(asset = asset, typename=typename).order_by('-mtime')

    device_form     = DeviceForm(request.POST or None, instance = device_instance)
    otheremq_form   = OtherEmqForm(request.POST or None, instance = otheremq_instance)
    maninfo_form    = ManInfoForm(request.POST or None, instance = maninfo_instance)
    device_change_fields    = []
    otheremq_change_fields  = []
    maninfo_change_fields   = []

    if device_form.is_valid() and otheremq_form.is_valid() and maninfo_form.is_valid():
        if device_form.has_changed():
            device_change_fields = device_form.changed_data
        if otheremq_form.has_changed():
            otheremq_change_fields = otheremq_form.changed_data
        if maninfo_form.has_changed():
            maninfo_change_fields = maninfo_form.changed_data

        device = device_form.save()
        otheremq = otheremq_form.save(commit=False)
        maninfo = maninfo_form.save(commit=False)
        otheremq.asset = device
        otheremq.save()
        maninfo.asset = device
        maninfo.save()

    if device_change_fields:
        modinfo(typename, asset, device_change_fields , old_device_instance, Devices.objects.get(asset =asset), request.user)
    if otheremq_change_fields:
        modinfo(typename, asset, otheremq_change_fields , old_otheremq_instance, OtherEmq.objects.get(asset =asset), request.user)
    if maninfo_change_fields:
        modinfo(typename, asset, maninfo_change_fields , old_maninfo_instance, ManInfo.objects.get(asset =asset), request.user)

    return render(request, 'assets/otheremq_edit.html', locals())

def otheremq_view(request, asset):
    page_title='其他设备详情'
    typename = '其他设备'
    device_instance = Devices.objects.get(asset = asset)
    otheremq_instance = device_instance.otheremq
    maninfo_instance = device_instance.maninfo
    device_form = DeviceForm(None, instance = device_instance)
    otheremq_form = OtherEmqForm(None, instance = otheremq_instance)
    maninfo_form = ManInfoForm(None, instance = maninfo_instance)

    for field in device_form.fields.keys():
            device_form.fields[field].widget.attrs['disabled'] = True
    for field in otheremq_form.fields.keys():
            otheremq_form.fields[field].widget.attrs['disabled'] = True
    for field in maninfo_form.fields.keys():
            maninfo_form.fields[field].widget.attrs['disabled'] = True

    list_log = ModLog.objects.filter(asset = asset, typename=typename).order_by('-mtime')
    return render(request, 'assets/otheremq_view.html', locals())

def otheremq_delete(request, asset):
    typename="其他设备"
    Devices.objects.get(asset = asset).delete()
    log = ModLog(typename=typename, asset=asset, mtime= datetime.datetime.now(), \
                              moduser=request.user, comment="删除其他设备")
    log.save()
    searchform = OtherEmqSearch()
    return HttpResponseRedirect("/assets/otheremq/search/",locals())

def otheremq_search(request):
    page_title='搜索网络设备'
    if request.method == "GET":
        searchform = OtherEmqSearch(request.GET)
        if searchform.is_valid():
            data = searchform.cleaned_data
            asset = data.get('asset','')
            asset_old = data.get('asset_old','')
            status = data.get('status','')
            type = data.get('type','')
            subtype = data.get('subtype','')
            manufacturer = data.get('manufacturer','')
            model = data.get('model','')
            building = data.get('building','')
            location = data.get('location','')
            consignee = data.get('consignee','')


            list_items = Devices.objects.filter(asset__icontains = asset,
                                                asset_old__icontains = asset_old,
                                                manufacturer__icontains = manufacturer,
                                                model__icontains = model,
                                                otheremq__building__icontains = building,
                                                otheremq__location__icontains = location,
                                                otheremq__consignee__icontains = consignee,
                                                )

            if status:
                list_items = list_items.filter(status=status)
            if  type:
                list_items = list_items.filter(type=type)
            if subtype:
                list_items = list_items.filter(subtype=subtype)


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
        searchform = OtherEmqSearch()

    return render(request, "assets/otheremq_search.html", locals())