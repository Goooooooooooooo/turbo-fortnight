from django import forms
from django.core.exceptions import NON_FIELD_ERRORS

from .models import ArticlePost


# 写文章的表单类
class ArticlePostForm(forms.ModelForm):

    class Meta:
        # 指明数据模型来源
        model = ArticlePost
        # 定义表单包含的字段
        fields = ('author', 'title', 'category', 'tags', 'body')
        error_messages = {
            NON_FIELD_ERRORS: {
                'unique_together': "%(model_name)s's %(field_labels)s are not unique.",
            }
        }
