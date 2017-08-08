#coding=utf-8
from __future__ import unicode_literals
from django.db import models



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


class User_table(models.Model):
    """
    Registered users
    """
    username=models.CharField(null=False,max_length=18)
    password=models.CharField(null=False,max_length=88)
    email=models.EmailField(null=False)
    nickname=models.CharField(null=False,max_length=42)
    contact_number = models.CharField(max_length=20, blank=True, null=True)
    generatetime=models.DateTimeField()
    def __unicode__(self):
        return self.username
    class Meta:
        db_table = 'User_table'
        verbose_name_plural="用户表"



class Project_table(models.Model):
    projectname=models.CharField(null=False,max_length=40)
    username=models.ForeignKey(User_table, db_column='username',on_delete=models.CASCADE)
    Assessmenttype=models.SmallIntegerField(null=False,choices=ASSESSTYPE.items(),default=1)       #就是到底是什么行业的评估，对应datatable的dataname
    level=models.SmallIntegerField(null=False,choices=LEVEL.items())
    generatetime=models.DateTimeField()
    class Meta:
        unique_together = ('projectname', 'username')
        ordering=('-generatetime',)
        db_table = 'Project_table'
        verbose_name_plural="项目表"
    def __unicode__(self):
        return '%s,%s'%(self.projectname,self.username)

class Data_table(models.Model):
    Assessmenttype=models.SmallIntegerField(null=False,choices=ASSESSTYPE.items(),default=1)   #就是到底是什么行业的评估
    level=models.SmallIntegerField(choices=LEVEL.items(),null=False)
    Requirement=models.SmallIntegerField(choices=REQUIREMENT.items(),null=True)
    datatype=models.SmallIntegerField(choices=DATATYPE.items(),null=False)
    content=models.TextField()
    class Meta:
        ordering=('-Assessmenttype',)
        db_table = 'Data_table'
        verbose_name_plural="数据表"
    def __unicode__(self):
        return '%s'%(self.pk)  

class Assessment_table(models.Model):
    project=models.ForeignKey(Project_table,on_delete=models.CASCADE)
    Assessmenttype=models.SmallIntegerField(null=False,choices=ASSESSTYPE.items(),default=1) #就是到底是什么行业的评估
    level=models.SmallIntegerField(choices=LEVEL.items(),null=False)
    Requirement=models.SmallIntegerField(choices=REQUIREMENT.items(),null=True,default=1)
    datatype=models.SmallIntegerField(choices=DATATYPE.items(),null=False)
    content=models.ForeignKey(Data_table,on_delete=models.CASCADE)                 #数据表的id
    match=models.SmallIntegerField(choices=MATCH.items(),null=True,blank=True)
    username=models.ForeignKey(User_table,db_column='username',on_delete=models.CASCADE)             #用户id
    generatetime=models.DateTimeField()
    class Meta:
        ordering=('datatype',)
        db_table = 'Assessment_table'
        verbose_name_plural="评估表"
    def __unicode__(self):
        return '%s'%(self.pk)

class File_table(models.Model):
    username=models.ForeignKey(User_table, db_column='username',on_delete=models.CASCADE)
    project=models.ForeignKey(Project_table,on_delete=models.CASCADE)
    file=models.CharField(null=True,max_length=100)
    def __unicode__(self):
        return self.username
    class Meta:
        unique_together = ('project', 'username')
        ordering=('pk',)
    class Meta:
        db_table = 'File_table'
        verbose_name_plural="文件表"

