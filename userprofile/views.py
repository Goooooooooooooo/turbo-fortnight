from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from .forms import UserLoginForm, UserRegisterForm , ProfileForm
from django.contrib.auth.models import User
from .models import Profile


'''
    # 表单验证失败，返回错误信息
    error = user_login_form.errors
    context = {'error': error}
    return render(request, 'userprofile/login.html', context)
    # user_id 自动生成字段
    profile = Profile.objects.get(user_id=pk)
'''

# django 自带 logou 方法
def user_logout(request):
    logout(request)
    request.session['next'] = request.META.get('HTTP_REFERER', '/')
    # return redirect('article:article-list')
    return HttpResponseRedirect(request.session['next'])


# 用户登录
def user_login(request):

    next = request.GET.get('next', '')

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

                if next == "":
                    if request.session['next'] != "":
                        return HttpResponseRedirect(request.session['next'])
                    return redirect("article:article-list")
                else:
                    return HttpResponseRedirect(next)
            else:
                return render(request, 'userprofile/login.html', context={'form': user_login_form})
        else:
            return render(request, 'userprofile/login.html', context={'form': user_login_form})

    elif request.method == 'GET':
        request.session['next'] = request.META.get('HTTP_REFERER', '/')
        return render(request, 'userprofile/login.html', context = {'form': UserLoginForm()})
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
            return render(request, 'userprofile/register.html', context={'form':user_register_form})
    elif request.method == 'GET':
        context={'form': UserRegisterForm()}
        return render(request, 'userprofile/register.html', context)
    else:
        return HttpResponse('请使用GET或POST请求数据')


# 用户个人信息修改
def user_edit_profile(request,pk):

    user = User.objects.get(id=pk)
    # 因为 Profile 关联的 User 表，user.profile 就可以直接调用 profile

    if request.method == 'POST':

        if user != request.user:
            return HttpResponse('没有权限修改个人信息')

        profile_form = ProfileForm(request.POST,request.FILES)

        if profile_form.is_valid():
            cleaned_dt = profile_form.cleaned_data
            user.profile.phone = cleaned_dt['phone']
            user.profile.bio = cleaned_dt['bio']

            if 'avatar' in request.FILES:
                user.profile.avatar = cleaned_dt['avatar']
            user.save()
            return redirect('userprofile:edit-profile', pk=pk)
        else:
            return render(request, 'userprofilt/edit_profile.html',context={'form':profile_form})

    elif request.method == 'GET':
        context={'form':ProfileForm(), 'user': user}
        return render(request, 'userprofile/edit_profile.html', context)
    else:
        return HttpResponse('请使用GET或POST请求数据')