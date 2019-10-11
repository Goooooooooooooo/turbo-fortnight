from django import forms
from .models import Comment


# 写文章的表单类
class CommentForm(forms.ModelForm):

    class Meta:
        # 指明数据模型来源
        model = Comment
        fields = ('body')

