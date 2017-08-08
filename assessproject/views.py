# -*- coding: utf-8 -*-
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render,render_to_response,get_object_or_404
from datetime import datetime
from assessproject.models import User_table,Project_table,Data_table,Assessment_table
from django.contrib.auth import logout as userlogout
from django.core.paginator import Paginator
from assessproject.Captcha import CreatePPCaptcha
import io,os,re
from assessproject.createxml import makefile
from assessment import settings
from assessproject.forms import RegisterForm,ProfileForm,CreateProjectForm,LoginForm,CreateselectForm,Assessmentform
from django.contrib.sessions.models import Session
import json
from django.views.decorators.cache import cache_page
USER_RE = re.compile(r"^\w{6,25}$")
def valid_username(username):
    return username and USER_RE.match(username)
EMAIL_RE  = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
def valid_email(email):
    return email and EMAIL_RE.match(email)

# def checkcheck_code(request):
#     if request.session["CheckCode"].upper()==request.GET.get('check_code').upper():
#         dictvalid={'valid':'Valid captcha!'}
#     else:
#         dictvalid={'error':'Invalid captcha!'}
#     return HttpResponse(
#         json.dumps(dictvalid),
#         content_type='application/json')
# def checkuser(request):
#     username=str(request.GET.get('username'))
#     if not valid_username(username):
#         dictvalid={'error':'Invalid username!'}
#     else:
#         objecttest=User_table.objects.filter(username__exact=username)
#         if objecttest:
#             dictvalid={'error':'This user already exist!'}
#         else:
#             dictvalid={'valid':'Valide username!'}
#     return HttpResponse(
#         json.dumps(dictvalid),
#         content_type='application/json')
    
# def checkemail(request):
#     email=str(request.GET.get('email'))
#     if not valid_email(email):
#         dictvalid={'error':'Invalid email!'}
#     else:
#         objecttest=User_table.objects.filter(email__exact=email)
#         if objecttest:
#             dictvalid={'error':'This email already exist!'}
#         else:
#             dictvalid={'valid':'Valide email!'}
#     return HttpResponse(
#         json.dumps(dictvalid),
#         content_type='application/json')


def captchaFunction(request):
    if request.method=="GET":
        stream = io.BytesIO()
        # img图片对象,code在图像中写的内容
        img, code =CreatePPCaptcha()
        img.save(stream, "JPEG")
        # 图片页面中显示,立即把session中的CheckCode更改为目前的随机字符串值
        request.session["CheckCode"] = code
        return stream.getvalue()
    else:
        return 'error'

def check_code(request):
    # captchaFunction(request)
    return HttpResponse(captchaFunction(request))

    # 代码：生成一张图片，在图片中写文件
    # request.session['CheckCode'] =  图片上的内容

    # 自动生成图片，并且将图片中的文字保存在session中
    # 将图片内容返回给用户

def download(request,projectid=None):
    """                                                                           
    Send a file through Django without loading the whole file into                
    memory at once. The FileWrapper will turn the file object into an             
    iterator for chunks of 26KB.                                                   
    """   
      
    #读取mongodb的文件到临时文件中
    if request.session.get('username',False):
        user=get_object_or_404(User_table,username = request.session.get('username'))
        project=get_object_or_404(Project_table,pk=int(projectid))
        # assessment=Assessment_table.objects.filter(username__exact=user.pk,project__exact=int(projectid))
        name=makefile(user=user,project=project)
        # fileid_=request.GET["fileid"] 
        filepath_ = name #文件全路径  
        # file_=TFiles.objects.get(fileid=int(fileid_))  
        filename_=project.projectname
        filetype_='.xls'
        if os.path.isfile(filepath_):  
            pass  
        else:
            return HttpResponseRedirect('/404/')
            # mongoLoad(fileid_)  
        #下载文件  
        def readFile(fn, buf_size=262144):#大文件下载，设定缓存大小  
            f = open(fn, "rb")  
            while True:#循环读取  
                c = f.read(buf_size)  
                if c:  
                    yield c  
                else:  
                    break  
            f.close()  
        response = HttpResponse(readFile(filepath_), content_type='APPLICATION/OCTET-STREAM') #设定文件头，这种设定可以让任意文件都能正确下载，而且已知文本文件不是本地打开  
        response['Content-Disposition'] = 'attachment; filename='+filename_+ filetype_#设定传输给客户端的文件名称  
        response['Content-Length'] = os.path.getsize(filepath_)#传输给客户端的文件大小  
        return response
    else:
        return HttpResponseRedirect('/login/')



@cache_page(60*15) 
def error404(request):
    return render(request,'404.html')


def user_login(request):
    try:
        if request.method == "POST":
            if not request.POST or len(str(request.POST))>500:
                data={'errors':'Error occured'}
                return HttpResponse(json.dumps(data),content_type='application/json')
            # print(len(request.POST))
            # if request.POST.get('check_code')=='':
                # request.session['loginerror']='input your captcha'
                # return render(request,'login.html', {'form':LoginForm(data=request.POST),'error':'input your captcha'})
            if request.session["CheckCode"].upper()==request.POST.get('check_code').upper():
                request.session["CheckCode"]=''
                MyLoginForm = LoginForm(request.POST)
                if MyLoginForm.is_valid():
                    # return render(request,'indextest.html', {'sessions':str(Session.objects.all().get_decoded()),'Mysessions':str(request.session._get_session_key())})
                    '''the following loop is for the unique session per user'''
                    # print(request.session.session_key)
                    try:
                        for session in Session.objects.all():
                            if 'username' in session.get_decoded():
                                if str(session.get_decoded()['username'])==str(MyLoginForm.cleaned_data['username']):
                                    if str(session)!=str(request.session.session_key):
                                        # print (str(session))
                                        session.delete()
                                        # print (str(request.session.session_key))
                                    # return HttpResponseRedirect('/404/')
                        # request.session['django_timezone'] ='Asia/Shanghai'
                        request.session['logindatauser']=request.POST.get('username')
                        request.session['logindatapass']=request.POST.get('password')
                        request.session['username']=MyLoginForm.cleaned_data['username']
                        # request.session.set_expiry(36000)
                        # request.set_cookie(settings.CSRF_COOKIE_NAME,request.META["CSRF_COOKIE"])
                        # request.COOKIES[str(settings.CSRF_COOKIE_NAME)].set_expiry(0)
                        # print(request.META["CSRF_COOKIE"])
                        # print(str(settings.CSRF_COOKIE_NAME))
                        request.session.cycle_key()
                        # return HttpResponseRedirect('/index/')
                        return HttpResponse('success')
                    except:
                        return HttpResponseRedirect('/404/')
                else:
                    errors=[]
                    for error in MyLoginForm.errors.values():
                        errors+=error
                    data={'errors':errors}
                    # request.session['tempdata']=request.POST
                    return HttpResponse(json.dumps(data),content_type='application/json')
                    # return HttpResponse(data)
            else:
                # return render_to_response('login.html', {'form':LoginForm(data=request.POST),'error':'input your captcha'})
                # request.session['captchaerror']='Captcha not match'
                # request.session['tempdata']=request.POST
                # data={'errors':'Captcha not match',"check_code":captcha}
                request.session["CheckCode"]=''
                data={'errors':{0:'Captcha not match'}}
                return HttpResponse(json.dumps(data),content_type='application/json')
                
        elif request.method == "GET":
            if request.session.get('username',False):
                return HttpResponseRedirect('/index/')
            # if request.session.get('captchaerror',False):
            #     error=request.session.get('captchaerror')
            #     request.session['captchaerror']=''
            #     if request.session.get('tempdata',False):
            #         tempdata=request.session.get('tempdata')
            #         request.session['tempdata']=''
            #         return render(request,'login.html',{'form':LoginForm(data=tempdata),'error':error})
            #     if request.session.get('logindata'):
            #         return render(request,'login.html',{'form':LoginForm(data=request.session.get('logindata')),'error':error})
            #     else:
            #         return render(request,'login.html',{'form':LoginForm(),'error':error})
            # if request.session.get('loginerror',False):
            #     errors=request.session.get('loginerror')
            #     request.session['loginerror']=''
            #     if request.session.get('tempdata',False):
            #         tempdata=request.session.get('tempdata')
            #         request.session['tempdata']=''
            #         return render(request,'login.html',{'form':LoginForm(data=tempdata),'errors':errors})
            #     if request.session.get('logindata',False):
            #         return render(request,'login.html', {'form':LoginForm(data=request.session.get('logindata')),'errors':errors})
            #     else:
            #         return render(request,'login.html', {'form':LoginForm(),'errors':errors})
            
            else:
                return render(request,'login.html')
                # if request.session.get('logindata',False):
                #     return render(request,'login.html', {'form':LoginForm(data=request.session.get('logindata'))})
                # else:
                #     return render(request,'login.html', {'form':LoginForm()})
    except:
        return HttpResponseRedirect('/404/')

def getsession(request):
    if request.method=='POST':
        if request.session.get('logindatauser',False):
            data={'username':request.session['logindatauser'],'password':request.session['logindatapass']}
            return HttpResponse(json.dumps(data),content_type='application/json')
        else:
            # data={"0":''}
            return HttpResponse(json.dumps(''),content_type='application/json')
    else:
        return HttpResponse(json.dumps(''),content_type='application/json')

def user_logout(request):
    try:
        if request.session.get('username',False):
            try:
                # request.session.flush()
                # del request.session[str(request.session.get('username'))]
                # userlogout(request)
                request.session['username']=''
            except KeyError:
                pass
            return HttpResponseRedirect('/login/') 
        else:
            return HttpResponseRedirect('/login/')
    except:
        return HttpResponseRedirect('/404/')



def user_register(request):
    try:
        if request.method == 'POST':
            if request.session["CheckCode"].upper()==request.POST.get('check_code').upper():
                request.session["CheckCode"]=''
                MyRegisterForm = RegisterForm(request.POST)
                if MyRegisterForm.is_valid():
                    new_user=MyRegisterForm.save()
                    return render(request,'login.html', {'form':LoginForm(),'Reminder':'Your Account is created',})
                else:
                    errors=[]
                    for error in MyRegisterForm.errors.values():
                        errors+=error
                    request.session['dataregister']=request.POST
                    request.session['registererror']=errors
                    return HttpResponseRedirect('/register/')
            else:
                request.session['dataregister']=request.POST
                request.session['registererror']='Invalid captcha'
                return HttpResponseRedirect('/register/')
        elif request.method == 'GET':
            if request.session.get('registererror',False):
                if type(request.session.get('registererror'))==type(list()):
                    errors=request.session.get('registererror')
                    error=''
                else:
                    error=request.session.get('registererror')
                    errors=''
                data=request.session.get('dataregister')
                request.session['dataregister']=''
                request.session['registererror']=''
                return render(request,'register.html', {'register_form': RegisterForm(data=data),'errors':errors,'error':error})
            else:
                return render(request,'register.html', {'register_form': RegisterForm()})
        else:
            return HttpResponseRedirect('/404/')
    except:
        return HttpResponseRedirect('/404/')

def profile(request):
    try:
        if request.session.get('username',False):
            # request.session.set_expiry(36000)
            username=request.session.get('username')
            objects=get_object_or_404(User_table,username=username)
            if request.method=="POST":
                Myprofileform=ProfileForm(request.POST)
                Myprofileform.username=request.session.get('username')
                if Myprofileform.is_valid():
                    object1=Myprofileform.save()
                    request.session['reminder']='Update your profile success'
                    return HttpResponseRedirect('/assess/profile/')
                else:
                    errors=[]
                    for error in Myprofileform.errors.values():
                        errors+=error
                    request.session['profileerrors']=errors
                    # return render(request,'profile.html', {'form': ProfileForm(instance=object1),'username':username,'reminder':'Update your profile success','nickname':object1.nickname})1
                return HttpResponseRedirect('/assess/profile/')
            elif request.method == "GET":
                if request.session.get('reminder',False):
                    reminder=request.session.get('reminder')
                    request.session['reminder']=''
                    return render(request,'profile.html', {'form': ProfileForm(instance=objects),'username':username,'nickname':objects.nickname,'reminder':reminder})
                if request.session.get('profileerrors',False):
                    errors=request.session.get('profileerrors')
                    request.session['profileerrors']=''
                    return render(request,'profile.html', {'form': ProfileForm(instance=objects),'username':username,'nickname':objects.nickname,'errors':errors})
                return render(request,'profile.html', {'form': ProfileForm(instance=objects),'username':username,'nickname':objects.nickname})
            else:
                return HttpResponseRedirect('/404/')
        else:
            return HttpResponseRedirect('/login/')
    except:
        return HttpResponseRedirect('/404/')



def index(request):
    try:
        if request.method=='GET' or request.method=='POST': 
            if request.session.get('username',False):
                # request.session.set_expiry(36000)
                username=request.session.get('username')
                nickname=User_table.objects.filter(username__exact = username)[0].nickname
                usernamepk=User_table.objects.filter(username__exact = username)[0].pk
                if Project_table.objects.filter(username__exact=usernamepk):
                    Project_table_objects=Project_table.objects.filter(username__exact=usernamepk)
                    p=Paginator(Project_table_objects,15)
                    page = request.GET.get('page',1)
                    currentpage=p.page(int(page))
                    return render(request,'index.html',{'Project_table_objects':currentpage.object_list,'username':username,'nickname':nickname,'cpage':currentpage,'pages':p})
                else:
                    return render(request,'index.html',{'username':username,'nickname':nickname})
            else:
                return HttpResponseRedirect('/login/')
        else:
            return HttpResponseRedirect('/404/')
    except:
        return HttpResponseRedirect('/404/')



def startproject(request):                           #1
    try:
        if request.session.get('username',False):
            # request.session.set_expiry(36000)
            user=get_object_or_404(User_table,username = request.session.get('username'))
            if request.method== "POST" :
                Mystartform=CreateProjectForm(user=user,data=request.POST)
                if Mystartform.is_valid():
                    project=Mystartform.save()
                    return HttpResponseRedirect('/assess/createselect/projectid=%s/'%project.pk)
                else:
                    errors=''
                    for error in Mystartform.errors.values():
                        errors+=error
                    request.session['projecterror']=errors
                    return HttpResponseRedirect('/assess/startproject/')
                    # return render(request,'createproject.html',{'form':Mystartform,'username':user.username,'nickname':user.nickname})
            elif request.method == "GET":
                try:
                    errors=request.session.get('projecterror')
                    request.session['projecterror']=''
                    return render(request,'createproject.html',{'form':CreateProjectForm(user=user),'username':user.username,'nickname':user.nickname,'errors':errors})
                except:
                    return render(request,'createproject.html',{'form':CreateProjectForm(user=user),'username':user.username,'nickname':user.nickname})
            else:
                return HttpResponseRedirect('/404/')
        else:
            return HttpResponseRedirect('/login/')
    except:
        return HttpResponseRedirect('/404/')

@cache_page(60*15) 
def createselect(request,project_id=None):
    try:
        if request.session.get('username',False):
            # request.session.set_expiry(36000)
            user=get_object_or_404(User_table,username = request.session.get('username'))
            project=get_object_or_404(Project_table,pk=int(project_id),username=int(user.pk)) 
            if request.method== "POST" or request.method == "GET":
                return render(request,'createselect.html',{'form':CreateselectForm(project=project),'username':user.username,'nickname':user.nickname,'project':project})
            else:
                return HttpResponseRedirect('/404/')
        else:
            return HttpResponseRedirect('/login/')
    except:
        return HttpResponseRedirect('/404/')

@cache_page(60*15) 
def projectcontent(request):            #用于跳转到录入评价3
    try: 
        if request.session.get('username',False):
            # request.session.set_expiry(36000)
            if request.method=="POST" or request.method=="GET":
                user=get_object_or_404(User_table,username = request.session.get('username'))
                project_id=request.GET.get('project_id','')
                project=get_object_or_404(Project_table,pk=int(project_id),username=int(user.pk))
                Myform=CreateselectForm(data=request.GET,project=project)
                if Myform.is_valid():
                    if Myform.cleaned_data['Requirement']!='0':
                        contents=Assessment_table.objects.filter(Assessmenttype=project.Assessmenttype,level=project.level,datatype=Myform.cleaned_data['datatype'],Requirement=Myform.cleaned_data['Requirement'],project__exact=int(project.pk))
                    else:
                        contents=Assessment_table.objects.filter(Assessmenttype=project.Assessmenttype,level=project.level,datatype=Myform.cleaned_data['datatype'],project__exact=int(project.pk))
                    return render(request,'projectassess.html',{'username':user.username,'nickname':user.nickname,'contents':contents,'project':project})
                else:
                    return render(request,'createselect.html',{'form':Myform,'username':user.username,'nickname':user.nickname,'project':project})
            else:
                return HttpResponseRedirect('/404/')
        else:
            return HttpResponseRedirect('/login/')
    except:
        return HttpResponseRedirect('/404/')
        
def saveassess(request):
    try:
        if request.session.get('username',False):
            # request.session.set_expiry(36000)
            if request.method=='POST' :
                user=get_object_or_404(User_table,username = request.session.get('username'))
                Myform=Assessmentform(request.POST)
                if Myform.is_valid():
                    # match=Myform.cleaned_data['match']
                    matches=request.POST.getlist('match')
                    assessid=request.POST.getlist('assessid')
                    for i in range(len(matches)):
                        if matches[i]:
                            p=Assessment_table.objects.get(pk__exact=int(assessid[i]))
                            p.match=matches[i]
                            p.generatetime=datetime.now()
                            p.save()
                        else:
                            p=Assessment_table.objects.get(pk__exact=int(assessid[i]))
                            p.match=None
                            p.save()
                    project_id=request.POST.get('project_id')
                    datatype=request.POST.get('datatype')
                    Requirement=request.POST.get('Requirement')
                    project=get_object_or_404(Project_table,pk=int(project_id))
                    contents=Assessment_table.objects.filter(datatype=int(datatype),Requirement=int(Requirement),project__exact=int(project.pk))
                    return render(request,'projectassess.html',{'username':user.username,'nickname':user.nickname,'contents':contents,'project':project})
                else:
                    return HttpResponseRedirect('/404/')
            elif request.method=="GET":
                return HttpResponseRedirect('/assess/startproject/')
            else:
                return HttpResponseRedirect('/404/')
        else:
            return HttpResponseRedirect('/login/')
    except:
        return HttpResponseRedirect('/404/')

# @cache_page(60*15) 
def displaydata(request,project_id=None):          #展示数据
    try:
        if request.method=="POST" or request.method=="GET":
            if request.session.get('username',False):
                # request.session.set_expiry(36000)
                user=get_object_or_404(User_table,username = request.session.get('username'))
                if Project_table.objects.filter(pk__exact = int(project_id),username__exact=int(user.pk)):
                    project=get_object_or_404(Project_table,pk = int(project_id),username=int(user.pk))
                    if Assessment_table.objects.filter(project__exact=int(project.pk)):
                        contents=Assessment_table.objects.filter(project__exact=int(project.pk))
                        p=Paginator(contents,30)
                        page = request.GET.get('page',1)
                        currentpage=p.page(int(page))
                        return render(request,'displaydata.html',{'username':user.username,'nickname':user.nickname,'project':project,'contents':currentpage.object_list,'cpage':currentpage,'pages':p})
                    else:
                        return HttpResponseRedirect('/404/')
                else:
                    return HttpResponseRedirect('/404/')
            else:
                return HttpResponseRedirect('/login/')
        else:
            return HttpResponseRedirect('/404/')
    except:
        return HttpResponseRedirect('/404/')

def delproject(request):
    try:
        if request.method=='POST':
            if request.session.get('username',False):
                # request.session.set_expiry(36000)
                username=request.session.get('username')
                user=get_object_or_404(User_table,username=username)
                project=get_object_or_404(Project_table,pk=int(request.POST.get('projectid')),username=user.pk)
                if project:
                    project.delete()
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
                else:
                    return HttpResponseRedirect('/404/')
            else:
                return HttpResponseRedirect('/login/')
        else:
            return HttpResponseRedirect('/404/')
    except:
        return HttpResponseRedirect('/404/')



def deletepage(request,project_id=None):
    try:
        if request.method=='POST' or request.method=='GET':
            if request.session.get('username',False):
                # request.session.set_expiry(36000)
                username=request.session.get('username')
                nickname=User_table.objects.filter(username__exact = username)[0].nickname
                if Project_table.objects.filter(pk__exact=int(project_id)):
                    project=Project_table.objects.filter(pk__exact=int(project_id))[0]
                    return render(request,'deletepage.html',{'username':username,'nickname':nickname,'project':project})
                else:
                    return HttpResponseRedirect('/index/')
            else:
                return HttpResponseRedirect('/login/')
        else:
            return HttpResponseRedirect('/404/')
    except:
        return HttpResponseRedirect('/404/')