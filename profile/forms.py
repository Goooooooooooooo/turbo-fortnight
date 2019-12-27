from django import forms
from django.contrib.auth.models import User
from .models import Profile

'''
    
    from django.forms import widgets as wid  #因为重名，所以起个别名
    widgets = {
        "name":wid.Textarea(attrs={"id":"id1","class":"form-control"}) # 自定义属性
    }
    labels，自定义在前端显示的名字
　　　　labels= { "name":"用户名", }

    Django 内置字段
    model = models.ArticlePost          # 对应的Model中的类
    Field
        fields = "__all__"              # 字段，如果是__all__,就是表示列出所有的字段
        required=True,                  # 是否允许为空
        widget=None,                    # HTML插件
        labels = None                   # 提示信息
        initial=None,                   # 初始值
        help_text='',                   # 帮助信息(在标签旁边显示)
        exclude = None                  # 排除的字段
        error_messages=None,            # 错误信息 {'required': '不能为空', 'invalid': '格式错误'}
        show_hidden_initial=False,      # 是否在当前插件后面再加一个隐藏的且具有默认值的插件（可用于检验两次输入是否一直）
        validators=[],                  # 自定义验证规则
        localize=False,                 # 是否支持本地化
        disabled=False,                 # 是否可以编辑
        label_suffix=None               # Label内容后缀
'''



# 用户登录 form
class UserLoginForm(forms.Form):
    username = forms.CharField(min_length=4,max_length=20,error_messages={'required':'用户名不能为空'},)
    password = forms.CharField(min_length=6,max_length=15,error_messages={'required': "密码不能为空"},)



# 用户信息扩展 form
class ProfileForm(forms.ModelForm):


    class Meta:
        model = Profile
        fields = ('avatar', 'phone', 'bio')



# 用户注册 form
class UserRegisterForm(forms.ModelForm):

    password = forms.CharField(min_length=8, max_length=20)
    password2 = forms.CharField(min_length=8, max_length=20)


    class Meta:
        model = User
        fields = ('username', 'email')

    # 两次输入密码一致验证
    def clean_password2(self):
        data = self.cleaned_data
        if data.get('password') == data.get('password2'):
            return data.get('password')
        else:
            raise forms.ValidationError('密码输入不一致')