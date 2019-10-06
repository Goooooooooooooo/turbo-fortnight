from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from .forms import UserLoginForm, UserRegisterForm , ProfileForm


# django 自带 logou 方法
def user_logout(request):
    logout(request)
    return redirect('article:article-list')


# 用户登录
def user_login(request):
    if request.method == 'POST':
        user_login_form = UserLoginForm(data=request.POST)
        if user_login_form.is_valid():
            # .cleaned_data 清洗出合法数据 只有在 is_valid 验证合法的情况下才能用
            data = user_login_form.cleaned_data
            # authenticate 方法:检验账号、密码是否正确匹配数据库中的某个用户
            # 如果均匹配则返回这个 user 对象
            user = authenticate(username=data['username'], password=data['password'])
            if user:
                # 将用户数据保存在 session 中，即实现了登录动作
                login(request, user)
                return redirect("article:article-list")
            else:
                error = user_login_form.errors
                context = {'error': error}
                return render(request, 'userprofile/login.html', context)
        else:
            print('表单验证失败')
            error = user_login_form.errors
            context = {'error': error}
            return render(request, 'userprofile/login.html', context)
    elif request.method == 'GET':
        user_login_form = UserLoginForm()
        context = {'form': user_login_form}
        return render(request, 'userprofile/login.html', context)
    else:
        return HttpResponse("请使用GET或POST请求数据")


# 用户注册
def user_register(request):
    if request.method == 'POST':
        user_register_form = UserRegisterForm(request.POST, request.FILES)
        print('register form check')
        if user_register_form.is_valid():
            print('register form check')
            new_user = user_register_form.save(commit=False)
            new_user.set_password(user_register_form.cleaned_data['password'])
            new_user.save()
            login(request, new_user)
            return redirect('article:article-list')
        else:
            # 把错误信息返回前端页面 显示
            error = user_register_form.errors
            context = {'error': error}
            return render(request, 'userprofile/register.html', context)
    elif request.method == 'GET':
        context = {}
        return render(request, 'userprofile/register.html', context)
    else:
        return HttpResponse('请使用GET或POST请求数据')


# 用户个人信息修改
def user_edit_profile(request):
    if request.method == 'POST':
        return render(request, 'userprofile/edit_profile.html')
    elif request.method == 'GET':
        profile = UserRegisterForm()
        context = {'profile': profile}
        return render(request, 'userprofile/edit_profile.html', context)
    else:
        return HttpResponse('请使用GET或POST请求数据')