#coding=utf-8
from django import template
from assessproject.models import Data_table,Assessment_table
from assessproject.forms import Assessmentform
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
import re
register = template.Library()

ASSESSTYPE={
    1:'信息系统安全等级保护基本要求'

    }
LEVEL = {
    1:'第一级',
    2:'第二级',
    3:'第三级',
    4:'第四级',
    5:'第五级',
    }
MATCH = {
    1: '完全符合',
    2: '符合',
    3: '部分符合',
    4: '少数符合',
    5: '不符合',
    }
REQUIREMENT={
    0:'',
    1:'技术要求',
    2:'管理要求',
    }
DATATYPE={
    1:'物理安全',
    2:'网络安全',
    3:'主机安全',
    4:'应用安全',
    5:'数据安全及备份恢复',
    6:'安全管理制度',
    7:'安全管理机构',
    8:'人员安全管理',
    9:'系统建设管理',
    10:'系统运维管理',
    }
# @stringfilter
@register.filter
def mydict(value,arg=None):
    if not value:
        return ''
    else:
        try:
            a=value[arg]
        except KeyError:
            a=''
        return a

@register.filter
def assesstype(value):
    if not int(value):
        return ''
    else:
        try:
            a=ASSESSTYPE[int(value)]
        except KeyError:
            a=''
        return a

@register.filter
def level(value):
    if not value:
        return ''
    else:
        try:
            a=LEVEL[int(value)]
        except KeyError:
            a=''
        return a

@register.filter
def match(value):
    if not value:
        return ''
    else:
        try:
            a=MATCH[int(value)]
        except KeyError:
            a=''
        return a
@register.filter
def Requirement(value):
    if not value:
        return ''
    else:
        try:
            a=REQUIREMENT[int(value)]
        except KeyError:
            a=''
        return a
@register.filter
def datatype(value):
    if not value:
        return ''
    else:
        try:
            a=DATATYPE[int(value)]
        except KeyError:
            a=''
        return a
@register.filter
def getcontent(value):
    if not value:
        return ''
    else:
        try:
            a=Data_table.objects.get(pk__exact=int(value)).content
        except:
            a=''
        return a
@register.filter
def getlevel(value):
    if not value:
        return ''
    else:
        try:
            a=level(Data_table.objects.get(pk__exact=int(value)).level)
        except:
            a=''
        return a
@register.filter
def getobject(value):
    a=get_object_or_404(Assessment_table,pk=int(value))
    if a.match:
        return Assessmentform(instance=a)
    else:
        return Assessmentform()
@register.filter
def getdatatype(value):
    try:
        return value[0].datatype
    except:
        return HttpResponseRedirect('/404/')
@register.filter
def getRequirement(value):
    try:
        return value[0].Requirement
    except:
        return HttpResponseRedirect('/404/')

@register.filter
def strip(value):
    return str(value).replace('\n','')

@register.filter
def selecttech(value):
    a=re.findall(r'(.*?)<option value="6"',value)
    return a[0]+'</select>'
@register.filter
def selectmgt(value):
    a=re.findall(r'(.*?)<option value="1"',value)
    b=re.findall(r'备份恢复</option>(.*?)$',value)
    return a[0]+b[0]