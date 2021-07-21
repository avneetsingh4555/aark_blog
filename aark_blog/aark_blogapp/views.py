import json
from django.core.serializers import serialize

from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,redirect
from django.http import HttpResponse, request
from .models import Blog_info
from django.template.loader import get_template
from aark_blogapp.models import Assign_project_info,User_info
from django.contrib.auth.models import User
import datetime
from django.contrib import messages
import json
from django.contrib.gis import serializers


def home(request):
    if request.session.has_key('is_logged'):
        u = request.session['u_email']
        q1 = User_info.objects.filter(user_email=u)
        us1=q1[0].user_name
        w1=Assign_project_info.objects.filter(ap_developers=us1)
        return render(request, 'profile.html',{'q1':q1,'w1':w1})
    
    elif request.session.has_key('iam_admin'):
        q1 = User_info.objects.all()
        return render(request, 'admin_emplist.html', {'q1': q1})
    
    else:
        return render(request, "login_register.html")


def editblog(request):
    if request.session.has_key('is_logged'):
        return render(request, "edit_blog.html")
    elif request.session.has_key('iam_admin'):

        return render(request, 'admin_edit_blog.html')
    else:
        return render(request, "login_register.html")


def profile(request):
    if(request.method == 'POST'):
        q1 = request.POST['var']
        request.session['a_email'] = q1

        q1 = User_info.objects.filter(user_email=q1)
        return render(request, "profile.html", {'q1': q1})

    else:
        u = request.session['u_email']
        q1 = User_info.objects.filter(user_email=u)
        if request.session.has_key('is_logged'):
            return render(request, "profile.html", {'q1': q1})
        else:
            return render(request, "login_User_info.html")


def editprofile(request):
    if request.session.has_key('iam_admin'):
        q1 = request.POST['var']
        request.session['a_email'] = q1
        return render(request, "admin_edit_profile.html")
    else:
        if request.session.has_key('is_logged'):
            return render(request, "edit_profile.html")
        else:
            return render(request, "login_register.html")


def updateprofile(request):
    if request.session.has_key('iam_admin'):
        uname = request.POST['usernm']
        upass = request.POST['upass']
        uphno = request.POST['uphno']
        uskl = request.POST['skills']
        q1 = request.session['a_email']
        w1 = User_info.objects.filter(user_email=q1).update(
            user_name=uname, user_password=upass, user_phno=uphno, user_skills=uskl)
        return render(request, "admin_edit_profile.html")
    else:
        if request.session.has_key('is_logged'):

            u = request.session['u_email']
            uname = request.POST['usernm']

            upass = request.POST['upass']

            uphno = request.POST['uphno']
            q1 = User_info.objects.filter(user_email=u).update(
                user_name=uname, user_password=upass, user_phno=uphno)

            return render(request, "edit_profile.html", {'q1': q1})

        else:
            return render(request, "login_register.html")


def blogsub(request):
    t = request.POST['title']
    s = request.POST['subtitle']
    d = request.POST['description']
    p = request.FILES['blogpic']
    now = datetime.datetime.now()
    u = request.session['u_email']
    u = Blog_info(bi_title=t, bi_subtitle=s, bi_description=d, bi_image=p, bi_event_date=now,bi_creator_name=u)
    u.save()
    if request.session.has_key('is_logged'):
        return render(request, "edit_blog.html")

    # return render()
    else:

        return render(request, 'admin_edit_blog.html')


def bloglist(request): 
    if request.session.has_key('is_logged'):
        u = request.session['u_email']
        alldata = Blog_info.objects.filter(bi_creator_name=u)
        tabdata = {'alldata': alldata}
        return render(request, 'bloglist.html', tabdata)
    elif request.session.has_key('iam_admin'):
        alldata = Blog_info.objects.all()
        tabdata = {'alldata': alldata}
        return render(request, 'admin_bloglist.html', tabdata)
    else:
        return render(request, "login_register.html")


def register(request):

    uname = request.POST['username']
    pwd = request.POST['password']
    em = request.POST['email']
    pno = request.POST['phno']
    skl = request.POST['skills']
    if User_info.objects.filter(user_email=em).exists():
        messages.success(
            request, 'Email already exist! Please select a different email')
        return render(request, 'admin_empregister.html')

    else:
        g = User_info(user_name=uname, user_password=pwd,user_email=em, user_phno=pno, user_skills=skl)
        g.save()

        return render(request, 'admin_empregister.html')


def userlogin(request):
    
    u = request.POST['email']
    p = request.POST['password']
    q1 = User_info.objects.filter(user_email=u)
    if(u == 'admin' and p == 'admin'):
        request.session['u_email'] = u
        request.session['iam_admin'] = True
        q1 = User_info.objects.all()
        return redirect(home)

    elif  q1.filter(user_password=p).exists():
        request.session['u_email'] = u
        request.session['is_logged'] = True
        u = request.session['u_email']
        q1 = User_info.objects.filter(user_email=u)
        us1=q1[0].user_name
        w1=Assign_project_info.objects.filter(ap_developers=us1)
        return redirect(home)

    else:
        return render(request,'login_register.html')    

        


def logout(request):
    if request.session.has_key('is_logged'):
        del request.session["is_logged"]
        return render(request, 'login_register.html')

    elif request.session.has_key('iam_admin'):
        del request.session["iam_admin"]
        return render(request, 'login_register.html')

    else:
        return render(request, 'login_register.html')



def emplist(request):
    if request.session.has_key('iam_admin'):
        q1 = User_info.objects.all()

        return render(request, 'admin_emplist.html', {'q1': q1})


def addemp(request):
    if request.session.has_key('iam_admin'):

        return render(request, 'admin_empregister.html')


def assipro(request):
    if request.session.has_key('iam_admin'):
        q1 = User_info.objects.all()
        return render(request, 'admin_assign_project.html', {'q1': q1})


def assigndata(request):
    if request.session.has_key('iam_admin'):
        ptitle = request.POST['protitle']
        plang = request.POST['languages']
        pdvlp = request.POST['developers']
        pstime = request.POST['subtime']
        g = Assign_project_info(ap_title=ptitle, ap_languages=plang,ap_developers=pdvlp, ap_sub_time =pstime)
        g.save()
        q1 = User_info.objects.all()
        return render(request, 'admin_assign_project.html', {'q1': q1})

def upload(request):
    
    if request.method == 'POST':
        ptitle=request.POST['picdata']
        pt=Assign_project_info.objects.filter(ap_id=ptitle).first()
        
        data=serialize("json",[pt])
        json_data=data
        js=json.loads(json_data) 
        # a=[*json_data.values()]
        # list(json_data.values())
        for tm in js:
           title=(tm['fields']['ap_title'])
           languages=(tm['fields']['ap_languages'])
           developers=(tm['fields']['ap_developers'])
        # a=[pt[0].ap_title,pt[0].ap_developers,pt[0].ap_languages]
        new_data=[title,languages,developers]
        print(new_data)
        return HttpResponse(json.dumps(new_data), content_type="application/json")
        # return HttpResponse(new_data, content_type="application/json")