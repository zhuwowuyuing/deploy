#coding=utf8
from django.db import models

# Create your models here.

class BaseInfo(models.Model):
    class Meta:
        verbose_name = '基本信息'
        verbose_name_plural = verbose_name
        ordering = ['hostname']

    hostname            = models.CharField('主机名',max_length=60, primary_key=True)
    status              = models.CharField('状态', max_length=20)
    cpu_model           = models.CharField('CPU 型号',max_length=100)
    num_cpus            = models.IntegerField('CPU 数量')
    mem_total           = models.IntegerField('内存')
    os                  = models.CharField('操作系统',max_length=150)
    productname         = models.CharField('服务器型号', max_length=100, null=True)
    manufacturer        = models.CharField('品牌', max_length=100, null=True)
    idc                 = models.CharField('IDC', max_length=100, null=True)
    ingw                = models.CharField('网关', max_length=100, null=True)

    def __unicode__(self):
        return u'%s' % (self.hostname)

class DiskInfo(models.Model):
    class Meta:
        verbose_name = '磁盘信息'
        verbose_name_plural = verbose_name
        ordering = ['hostname', 'mount']

    hostname            = models.ForeignKey(BaseInfo,related_name="disks")
    mount               = models.CharField('状态', max_length=60)
    available           = models.BigIntegerField('可用内存')
    total               = models.BigIntegerField('内存总数')

    def __unicode__(self):
        return u'%s' % (self.hostname)

class NetworkInfo(models.Model):
    class Meta:
        verbose_name = '网卡信息'
        verbose_name_plural = verbose_name
        ordering = ['hostname', 'interface']

    hostname            = models.ForeignKey(BaseInfo,related_name="interfaces")
    interface           = models.CharField('网络接口', max_length=400)
    hwaddr              = models.CharField('物理地址', max_length=60)
    ipaddr              = models.CharField('IP地址', max_length=60)

    def __unicode__(self):
        return u'%s' % (self.hostname)

class ErrorInfo(models.Model):
    class Meta:
        verbose_name = '错误信息'
        verbose_name_plural = verbose_name

    hostname            = models.CharField('主机名',max_length=60)
    info                = models.CharField('信息', max_length=200)

    def __unicode__(self):
        return u'%s' % (self.hostname)

class CheckError(models.Model):
    class Meta:
        verbose_name = '检测脚本错误信息'
        verbose_name_plural = verbose_name
    time                = models.DateTimeField("故障时间")
    hostname            = models.CharField('主机名',max_length=60)
    errormsg            = models.CharField('错误信息', max_length=1000)

    def __unicode__(self):
        return u'%s' % (self.hostname)