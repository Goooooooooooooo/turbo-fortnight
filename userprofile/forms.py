from django import forms
from django.contrib.auth.models import User
from .models import Profile


# 用户登录 form
class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()


# 用户信息扩展 form
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('avatar', 'phone', 'bio')


# 用户注册 form
class UserRegisterForm(forms.ModelForm):
    username = forms.CharField(min_length=4, max_length=20)
    password = forms.CharField(min_length=8, max_length=20)
    password2 = forms.CharField(min_length=8, max_length=20)

    class Meta:
        model = User
        fields = ('email',)

    # 两次输入密码一致验证
    def clean_password2(self):
        data = self.cleaned_data
        if data.get('password') == data.get('password2'):
            return data.get('password')
        else:
            raise forms.ValidationError('密码输入不一致')