from django.shortcuts import render,redirect,HttpResponse
from user import forms,models

# Create your views here.

def login(request):
    # print(request.POST)
    obj = ""
    if request.method == 'GET':
        obj = forms.loginForm()
        # print('GET')

    elif request.method == 'POST':
        # print(request.POST)
        obj = forms.loginForm(request.POST)
        errors = {}
        if obj.is_valid():
            data = obj.cleaned_data
            if request.POST.get('auto_login'):
                request.session.set_expiry(60 * 60 * 24 )
            request.session.set_expiry(0)
            request.session['is_login'] = True
            request.session['user'] = data.get('username')
            return redirect('/index')

    return render(request,'page-login.html',{'form':obj})

def register(request):
    # username = models.CharField(max_length=16, verbose_name='用户名')
    # password = models.CharField(max_length=16, verbose_name='密码')
    # nickname = models.CharField(max_length=16,verbose_name='昵称')
    # email = models.EmailField(max_length=16, verbose_name='邮箱')
    # img = models.ImageField(verbose_name='头像',upload_to='static/img/user/',default='static/img/user/1.jpg')
    # ctime = models.DateTimeField(auto_created=True,verbose_name='创建时间')

    if request.method == 'GET':
        obj = forms.RegisterForm()
        return render(request, 'page-register.html', {'form': obj})

    elif request.method == 'POST':
        obj = forms.RegisterForm(request.POST)
        print(obj)
        if obj.is_valid():
            data = obj.cleaned_data
            new_user = models.user_info(
                username=data.get('username'),
                password=data.get('pwd'),
                # email=data.get('email')
            )
            new_user.save()
            request.session['is_login'] = True
            request.session['user'] = data.get('username')
            return redirect('/index')
        else:
            errors = obj.errors
            return render(request, 'page-register.html', {'form': obj})


def logout(request):
    try:
        #删除is_login对应的value值
        request.session['is_login'] = False
        del request.session['user']
    except KeyError:
        pass
    #点击注销之后，直接重定向回登录页面
    return redirect('/login/')


def adjust_goal(request):
    is_login = request.session.get('is_login')
    if not is_login:
        return redirect('/login')

    context = {}
    username = request.session['user']
    context['name'] = username

    return render(request, 'adjust-goal.html', context)


def update_info(request):
    is_login = request.session.get('is_login')
    if not is_login:
        return redirect('/login')

    context = {}
    username = request.session['user']
    context['name'] = username

    return render(request, 'page-profile.html', context)
