#coding=utf-8
from __future__ import unicode_literals
from assessproject.models import User_table,Project_table,Data_table,Assessment_table,File_table
from django import forms
# from django.db import models
from datetime import datetime
from django.contrib.auth.hashers import make_password, check_password
import re
from django.shortcuts import get_object_or_404
# USER_RE = re.compile(r"^[a-zA-Z0-9_-]{6,25}$")
USER_RE = re.compile(r"^\w{6,25}$")

def valid_username(username):
    return username and USER_RE.match(username)

NO_RE = re.compile("^[\d|\-|\+|(|)]{6,25}$")

def valid_number(number):
    return number and NO_RE.match(number)

Nick_RE = re.compile(r"^\w{4,20}$")

def valid_nickname(name):
    return name and Nick_RE.match(name)

PASS_RE = re.compile(r"^.{6,30}$")

def valid_password(password):
    return password and PASS_RE.match(password)

EMAIL_RE  = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
def valid_email(email):
    return email and EMAIL_RE.match(email)
ASSESSTYPE_FORM=(
(1,'信息系统安全等级保护基本要求'),

)
LEVEL_FORM = (
(1,'第一级'),
(2,'第二级'),
(3,'第三级'),
(4,'第四级'),
(5,'第五级'),
)
REQUIREMENT_FORM=(
(0,''),
(1,'技术要求'),
(2,'管理要求'),
)
DATATYPE_FORM=(
(1,'物理安全'),
(2,'网络安全'),
(3,'主机安全'),
(4,'应用安全'),
(5,'数据安全及备份恢复'),
(6,'安全管理制度'),
(7,'安全管理机构'),
(8,'人员安全管理'),
(9,'系统建设管理'),
(10,'系统运维管理'),
)
MATCH_FORM = (
(1, '完全符合'),
(2, '符合'),
(3, '部分符合'),
(4, '少数符合'),
(5, '不符合'),
)
class RegisterForm(forms.ModelForm):
    username=forms.CharField(label='用户名(*)',required=True,widget=forms.TextInput(attrs={"class":"form-control",'placeholder':'6 letters or more','autocomplete':'off',"id":"username"}))
    password = forms.CharField(label='密码(*)',required=True,widget=forms.PasswordInput(attrs={"class":"form-control",'placeholder':'6 letters or more','autocomplete':'off',"id":"password"}))
    password2=forms.CharField(label='确定密码(*)',required=True,widget=forms.PasswordInput(attrs={"class":"form-control",'placeholder':'Input the password again','autocomplete':'off',"id":"password2"}))
    email=forms.EmailField(label='电子邮件(*)',required=True,widget=forms.EmailInput(attrs={"class":"form-control","id":"email",'placeholder':'Input your email'}))
    nickname=forms.CharField(label='昵称(*)',required=True,widget=forms.TextInput(attrs={"class":"form-control","id":"nickname",'placeholder':'4 letters or more'}))
    contact_number=forms.CharField(label='联系电话(*)',required=True,widget=forms.TextInput(attrs={"class":"form-control","id":"contact_number",'placeholder':'6 number or more'}))
    class Meta:
        model=User_table
        fields=['username','password','email','nickname','contact_number',]
    def clean_username(self):
        try:
            User_table.objects.get(username=self.cleaned_data['username'])
        except User_table.DoesNotExist:
            if not valid_username(self.cleaned_data['username']):
                raise forms.ValidationError("This username is invalid.")
            else:
                return self.cleaned_data['username']
        raise forms.ValidationError("This username is already in use.Please choose another.")
    def clean_email(self):
        try:
            User_table.objects.get(email=self.cleaned_data['email'])
        except User_table.DoesNotExist:
            if not valid_email(self.cleaned_data['email']):
                raise forms.ValidationError("This email is invalid.")
            else:
                return self.cleaned_data['email']
        raise forms.ValidationError("This email is already in use.Please choose another.")
    def clean_nickname(self):
        if not valid_nickname(self.cleaned_data['nickname']):
            raise forms.ValidationError("This nickname is invalid.")
        else:
            return self.cleaned_data['nickname']
    def clean_password(self):
        if not valid_password(self.cleaned_data['password']):
            raise forms.ValidationError("This password is invalid.")
        else:
            return self.cleaned_data['password']
    def clean_contact_number(self):
        if not valid_number(self.cleaned_data['contact_number']):
            raise forms.ValidationError("This contact number is invalid.")
        else:
            return self.cleaned_data['contact_number']
    def clean(self):
        if 'password' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password'] == self.cleaned_data['password2']:
                return self.cleaned_data
            else:
                raise forms.ValidationError("You must type the same password each time")#➥
        else:
            raise forms.ValidationError("You must type the proper password")
    def save(self):
        user=User_table.objects.create(username=self.cleaned_data['username'],password=make_password(self.cleaned_data['password'], None, 'pbkdf2_sha256'),
                    email=self.cleaned_data['email'],nickname=self.cleaned_data['nickname'],contact_number=self.cleaned_data['contact_number'],
                    generatetime=datetime.now())
        return user




class CreateselectForm(forms.ModelForm):
    Requirement=forms.ChoiceField(label='要求类',required=False,choices=REQUIREMENT_FORM,widget=forms.Select(attrs={"class":"form-control"}))
    datatype=forms.ChoiceField(label='类型',required=True,choices=DATATYPE_FORM,widget=forms.Select(attrs={"class":"form-control"}))
    def __init__(self, project, *args, **kwargs):
        super(CreateselectForm, self).__init__(*args, **kwargs)
        self.project = project
    class Meta:
        model=Assessment_table
        fields=['Requirement','datatype']
    def clean(self):
        if self.cleaned_data['Requirement']!='0':
            if 'datatype' in self.cleaned_data:
                if Assessment_table.objects.filter(Assessmenttype=self.project.Assessmenttype,level=self.project.level,datatype=int(self.cleaned_data['datatype']),Requirement=self.cleaned_data['Requirement']):
                    return self.cleaned_data
                else:
                    raise forms.ValidationError("Invalid submit")
            else:
                raise forms.ValidationError('Select the type which you want to assess.')
        else:
            if 'datatype' in self.cleaned_data:
                if Assessment_table.objects.filter(Assessmenttype=self.project.Assessmenttype,level=self.project.level,datatype=int(self.cleaned_data['datatype'])):
                    return self.cleaned_data
                else:
                    raise forms.ValidationError("Invalid submit")
            else:
                raise forms.ValidationError('Select the type which you want to assess.')



class Assessmentform(forms.ModelForm):
    # match=forms.ChoiceField(required=False,choices=MATCH_FORM,initial=None)
    class Meta:
        fields=['match']
        model=Assessment_table




class CreateProjectForm(forms.ModelForm):
    projectname=forms.CharField(label='项目名称',required=True,widget=forms.TextInput(attrs={"class":"form-control",'autocomplete':'off'}))
    Assessmenttype=forms.ChoiceField(label='项目类型',required=True,choices=ASSESSTYPE_FORM,widget=forms.Select(attrs={"class":"form-control"}))
    level=forms.ChoiceField(label='等级',required=True,choices=LEVEL_FORM,widget=forms.Select(attrs={"class":"form-control"}))
    def __init__(self, user, *args, **kwargs):
        super(CreateProjectForm, self).__init__(*args, **kwargs)
        self.user = user
    class Meta:
        model=Project_table
        fields=['projectname','Assessmenttype','level']
    def clean_projectname(self):
        try:
            Project_table.objects.get(username=self.user.pk,projectname=self.cleaned_data['projectname'])
        except Project_table.DoesNotExist:
            if ' ' in self.cleaned_data['projectname'] or '\'' in self.cleaned_data['projectname'] or '"' in self.cleaned_data['projectname']:
                raise forms.ValidationError("This projectname is invalid.")
            else:
                return self.cleaned_data['projectname']
        raise forms.ValidationError("This projectname is already in use.Please choose another.")
    def save(self):
        project=Project_table.objects.create(projectname=self.cleaned_data['projectname'],Assessmenttype=self.cleaned_data['Assessmenttype'],level=self.cleaned_data['level'],generatetime=datetime.now(),username=self.user)
        file=File_table.objects.create(username=self.user,project=project)
        contents=Data_table.objects.filter(Assessmenttype=self.cleaned_data['Assessmenttype'],level=self.cleaned_data['level'])
        for content in contents:
            a=Assessment_table.objects.create(Assessmenttype=self.cleaned_data['Assessmenttype'],level=self.cleaned_data['level'],
                Requirement=content.Requirement,datatype=content.datatype,match=None,generatetime=datetime.now(),username=self.user,content=content,project=project)
        return project



class LoginForm(forms.ModelForm):
    # username=forms.CharField(widget=forms.TextInput(attrs={'placeholder':'6 letters or more','autocomplete':'off',"id":"username","pattern":"[\w]{6,20}","class":"form-control"}))
    # password =forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'6 letters or more' ,'autocomplete':'off',"class":"form-control","id":"password","pattern":".{6,20}"}))
    username=forms.CharField(widget=forms.TextInput(attrs={'placeholder':'6 letters or more','autocomplete':'off',"id":"username","class":"form-control"}))
    password =forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'6 letters or more' ,'autocomplete':'off',"class":"form-control","id":"password"}))
    class Meta:
        model=User_table
        fields=['username','password']
    def clean_username(self):
        if not valid_username(self.cleaned_data['username']):
            raise forms.ValidationError("This username is invalid and it has to be a string more than 6 chars.")
        else:
            return self.cleaned_data['username']
    def clean_password(self):
        if not valid_password(self.cleaned_data['password']):
            raise forms.ValidationError("This password is invalid and it has to be a string more than 6 chars.")
        else:
            return self.cleaned_data['password']
    def clean(self):
        try:
            if check_password(self.cleaned_data['password'],User_table.objects.get(username=self.cleaned_data['username']).password):
                return self.cleaned_data
            else:
                raise forms.ValidationError("This username or password is not right.")
        except:
            raise forms.ValidationError("This username or password is not right.")




class ProfileForm(forms.ModelForm):
    email=forms.EmailField(label='邮件(*)',required=False,widget=forms.EmailInput(attrs={"class":"form-control","id":"email"}))
    nickname=forms.CharField(label='昵称(*)',required=False,max_length=42,widget=forms.TextInput(attrs={"class":"form-control","id":"nickname"}))
    contact_number=forms.CharField(label='联系电话(*)',max_length=20, required=False,widget=forms.TextInput(attrs={"class":"form-control","id":"contact_number"}))
    class Meta:
        model=User_table
        fields=['email','nickname','contact_number']
    def clean_email(self):
        try:
            if User_table.objects.get(username__exact=self.username).email != self.cleaned_data['email']:
                User_table.objects.get(email__exact=self.cleaned_data['email'])
            else:
                return self.cleaned_data['email']
            raise forms.ValidationError("This email is already in use.Please choose another.")
        except User_table.DoesNotExist:
            if not valid_email(self.cleaned_data['email']):
                raise forms.ValidationError("This email is invalid.")
            else:
                return self.cleaned_data['email']
        raise forms.ValidationError("Error.")
    def clean_nickname(self):
        if not valid_nickname(self.cleaned_data['nickname']):
            raise forms.ValidationError("This nickname is invalid.")

        else:
            return self.cleaned_data['nickname']
    def clean_contact_number(self):
        if not valid_number(self.cleaned_data['contact_number']):
            raise forms.ValidationError("This contact number is invalid.")
        else:
            return self.cleaned_data['contact_number']
    def save(self):
        user=get_object_or_404(User_table,username=self.username)
        user.email=self.cleaned_data['email']
        user.nickname=self.cleaned_data['nickname']
        user.contact_number=self.cleaned_data['contact_number']
        user.save()
        return user