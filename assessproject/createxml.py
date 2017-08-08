#coding=utf-8
import xlwt
import random
import string
from assessment import settings
from assessproject.models import User_table,Assessment_table,Data_table,File_table
from django.shortcuts import get_object_or_404
# import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')
import os
import time
row0 = [u'id',u'评估类型',u'等级',u'需求类型',u'数据类型',u'内容',u'符合程度']
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
MATCH = {
    1: '完全符合',
    2: '符合',
    3: '部分符合',
    4: '少数符合',
    5: '不符合',
}
def makerandom():
    salt = ''.join(random.sample(string.ascii_letters + string.digits, 8))
    return salt

def makefile(user=None,project=None):
    time.sleep(0.3)
    f=xlwt.Workbook()
    sheet1 = f.add_sheet(u'sheet1') #创建sheet
    #生成第一行
    for i in range(0,len(row0)):
      sheet1.write(0,i,row0[i])
    assessments=Assessment_table.objects.filter(username__exact=user.pk,project__exact=project.pk)
    j=1
    for assessment in assessments:
        # sheet1.write(j,0,j)
        # sheet1.write(j,1,str(ASSESSTYPE[int(assessment.Assessmenttype)]).decode('utf8'))
        # sheet1.write(j,2,str(LEVEL[int(assessment.level)]).decode('utf8'))
        # sheet1.write(j,3,str(REQUIREMENT[int(assessment.Requirement)]).decode('utf8'))
        # sheet1.write(j,4,str(DATATYPE[int(assessment.datatype)]).decode('utf8'))
        # sheet1.write(j,5,str(Data_table.objects.get(pk__exact=assessment.content_id).content).decode('utf8'))
        sheet1.write(j,0,j)
        sheet1.write(j,1,str(ASSESSTYPE[int(assessment.Assessmenttype)]))
        sheet1.write(j,2,str(LEVEL[int(assessment.level)]))
        sheet1.write(j,3,str(REQUIREMENT[int(assessment.Requirement)]))
        sheet1.write(j,4,str(DATATYPE[int(assessment.datatype)]))
        sheet1.write(j,5,str(Data_table.objects.get(pk__exact=assessment.content_id).content))
        if assessment.match:
            sheet1.write(j,6,str(MATCH[int(assessment.match)]))
        j+=1
    myfile=get_object_or_404(File_table,username__exact=user.pk,project__exact=project.pk)
    if myfile.file:
        os.remove(myfile.file)
    filename=makerandom()+'00'+str(project.pk)+'.xls'
    path=settings.MEDIA_ROOT+'\\'+filename
    f.save(path) #保存文件
    myfile.file=str(path)
    myfile.save()
    return myfile.file
