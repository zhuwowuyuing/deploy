#coding=utf8
__author__ = 'liangnaihua'

from django import forms
from django.forms import ModelChoiceField
from models import Devices, Status, Server, ManInfo, ModLog, Type, Subtype
import datetime
from django.contrib.admin.widgets import AdminDateWidget


# 资产搜索表单
class AssetSearch(forms.Form):
    asset           = forms.CharField(label='资产编号', max_length=60, required=False)
    asset_old       = forms.CharField(label='旧资产编号', max_length=60, required=False)
    # type            = forms.CharField(label='类别', max_length=60, required=False)
    # subtype         = forms.CharField(label='子类别', max_length=60, required=False)
    type            = forms.ModelChoiceField(label='类别', queryset=Type.objects.all(), required=False)
    subtype         = forms.ModelChoiceField(label='子类别', queryset=Subtype.objects.all(), required=False)
    manufacturer    = forms.CharField(label='品牌', max_length=60, required=False)
    model           = forms.CharField(label='型号', max_length=100, required=False)
    status		    = forms.ModelChoiceField(label='使用状态', queryset=Status.objects.filter(exclusive=False), required=False)
    building        = forms.CharField(label='机房(所处位置)',max_length=60, required=False)
    location        = forms.CharField(label='机柜',max_length=60, required=False)
    consignee       = forms.CharField(label='托管编号',max_length=60, required=False)
    hostname        = forms.CharField(label='主机名',max_length=60, required=False)
    vendor          = forms.CharField(label='供应商',max_length=200, required=False)

# 资产信息表单
class AssetForm(forms.Form):
    asset           = forms.CharField(label='资产编号', max_length=60, required=True)
    asset_old       = forms.CharField(label='旧资产编号', max_length=60, required=False)
    district        = forms.CharField(label='所在地区', max_length=60)
    company         = forms.CharField(label='账上所属公司', max_length=60)
    type            = forms.CharField(label='类别', max_length=60)
    subtype         = forms.CharField(label='子类别', max_length=60)
    status		    = ModelChoiceField(label='使用状态', queryset=Status.objects.filter(exclusive=False), required=False)
    manufacturer    = forms.CharField(label='品牌', max_length=60, required=False)
    model           = forms.CharField(label='型号', max_length=100, required=False)
    serialno        = forms.CharField(label='序列号', max_length=100, required=False)
    size            = forms.CharField(label='尺寸', max_length=60, required=False)
    cpu             = forms.CharField(label='CPU', max_length=200, required=False)
    harddisk        = forms.CharField(label='硬盘', max_length=200, required=False)
    ram             = forms.CharField(label='内存', max_length=200, required=False)
    os              = forms.CharField(label='操作系统',max_length=200, required=False)
    building        = forms.CharField(label='机房(所处位置)', max_length=60, required=False)
    location        = forms.CharField(label='机柜', max_length=60, required=False)
    consignee       = forms.CharField(label='托管编号', max_length=60, required=False)
    hostname        = forms.CharField(label='主机名', max_length=60, required=False)
    dept            = forms.CharField(label='使用部门', max_length=60, required=False)
    business        = forms.CharField(label='业务系统', max_length=60, required=False)
    ownername       = forms.CharField(label='领用人', max_length=60, required=False)
    administrator   = forms.CharField(label='实物管理员',max_length=60, required=False)
    warehousedate   = forms.DateField(label='入库时间', initial=datetime.date.today, required=False)
    receivedate     = forms.DateField(label='领用时间', initial=datetime.date.today, required=False)
    warrantyexpirationdate = forms.DateField(label='保修至', initial=datetime.date(datetime.date.today().year+3,datetime.date.today().month, datetime.date.today().day), required=False)
    scrapDate       = forms.DateField(label='报废时间', required=False)
    purchase_date   = forms.DateField(label='采购时间', initial=datetime.date.today, required=False)
    purchase_cost   = forms.FloatField(label='采购价格', required=False)
    accounting_date = forms.DateField(label='入账时间',initial=datetime.date.today, required=False)
    account_cost    = forms.FloatField(label='入账价格', required=False)
    vendor          = forms.CharField(label='供应商',max_length=200, required=False)
    vendor_contacts = forms.CharField(label='供应商联系方式', widget=forms.Textarea, max_length=2000, required=False)
    accounting_info = forms.CharField(label='入账情况', widget=forms.Textarea, max_length=2000, required=False)
    order_list      = forms.CharField(label='相关单据', widget=forms.Textarea, max_length=2000, required=False)
    changeInfo      = forms.CharField(label='变更信息', widget=forms.Textarea, max_length=4000, required=False)
    comment         = forms.CharField(label='备注', widget=forms.Textarea, max_length=2000, required=False)

class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
    # exclude = [] # uncomment this line and specify any field to exclude it from the form

    def __init__(self, *args, **kwargs):
        super(StatusForm, self).__init__(*args, **kwargs)

class TypeForm(forms.ModelForm):
    class Meta:
        model = Type
    # exclude = [] # uncomment this line and specify any field to exclude it from the form

    def __init__(self, *args, **kwargs):
        super(TypeForm, self).__init__(*args, **kwargs)

class SubtypeForm(forms.ModelForm):
    class Meta:
        model = Subtype
    # exclude = [] # uncomment this line and specify any field to exclude it from the form

    def __init__(self, *args, **kwargs):
        super(SubtypeForm, self).__init__(*args, **kwargs)

class DeviceForm(forms.ModelForm):
    class Meta:
        model = Devices
    # exclude = [] # uncomment this line and specify any field to exclude it from the form

    def __init__(self, *args, **kwargs):
        super(DeviceForm, self).__init__(*args, **kwargs)
        self.fields['status'].queryset = Status.objects.filter(exclusive=False)


class ServerForm(forms.ModelForm):
    class Meta:
        model = Server
        exclude = ['asset'] # uncomment this line and specify any field to exclude it from the form

    def __init__(self, *args, **kwargs):
        super(ServerForm, self).__init__(*args, **kwargs)



class ManInfoForm(forms.ModelForm):
    class Meta:
        model = ManInfo
        exclude = ['asset'] # uncomment this line and specify any field to exclude it from the form

    def __init__(self, *args, **kwargs):
        super(ManInfoForm, self).__init__(*args, **kwargs)
        self.fields['warehousedate'].initial    = datetime.date.today
        self.fields['receivedate'].initial  = datetime.date.today
        self.fields['warrantyexpirationdate'].initial   = datetime.date(datetime.date.today().year+3,datetime.date.today().month, \
                                                                          datetime.date.today().day)
        self.fields['purchase_date'].initial = datetime.date.today
        self.fields['purchase_cost'].initial = 0
        self.fields['accounting_date'].initial  = datetime.date.today
        self.fields['account_cost'].initial = 0

        # self.fields['warehousedate'].widget             = AdminDateWidget
        # self.fields['receivedate'].widget               = AdminDateWidget
        # self.fields['warrantyexpirationdate'].widget    = AdminDateWidget
        # self.fields['scrapDate'].widget                 = AdminDateWidget
        # self.fields['purchase_date'].widget             = AdminDateWidget
        # self.fields['accounting_date'].widget           = AdminDateWidget

class ModLogSearchForm(forms.Form):
    typename        =forms.CharField(label="类型", max_length=60, required=False)
    asset           =forms.CharField(label='资产编号', max_length=60, required=False)
    moduser         =forms.CharField(label='修改人', max_length=60, required=False)
    field           =forms.CharField(label='字段名称',max_length=60, required=False)
    comment         =forms.CharField(label='备注',max_length=500, required=False)
    starttime       =forms.DateTimeField(label="修改时间从", required=False)
    endtime         =forms.DateTimeField(label="修改时间至", required=False)

