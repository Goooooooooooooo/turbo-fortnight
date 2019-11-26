from django import forms
from .models import Comment


# 写文章的表单类
class CommentForm(forms.ModelForm):

    class Meta:
        # 指明数据模型来源
        model = Comment
        # fields 表示需要渲染的字段
        fields = ('body',)

        '''
           widgets = {
                # 为各个需要渲染的字段指定渲染成什么html组件，主要是为了添加css样式。
                # 例如 user_name 渲染后的html组件如下：
                # <input type="text" class="form-control" placeholder="Username" aria-describedby="sizing-addon1">
                
                'user_name': forms.TextInput(attrs={
                    'class': 'form-control',
                    'placeholder': "请输入昵称",
                    'aria-describedby': "sizing-addon1",
                }),
                'user_email': forms.TextInput(attrs={
                    'class': 'form-control',
                    'placeholder': "请输入邮箱",
                    'aria-describedby': "sizing-addon1",
                }),
                'body': forms.Textarea(attrs={'placeholder': '我来评两句~'}),
            }
        '''

