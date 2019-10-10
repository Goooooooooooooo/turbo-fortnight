from django import template
import markdown
from django.template.defaultfilters import stringfilter

'''
    自定义过滤器 给 form 等添加 class 属性
    便于更改样式（使用类视图，不重写 form 的情况）
    需要在 settings.py [ INSTALLED_APPS ]中注册--例：'article.templatetags',
'''

# 如果不加括号()，会报 TypeError: filter() missing 1 required positional argument: 'self'
register = template.Library()


@register.filter(name='add_class')
def add_class(value, arg):
    return value.as_widget(attrs={'class': arg})

#
@register.simple_tag
def error_msg(error_list):
    if error_list:
        return error_list[0]
    return ''


@register.filter
@stringfilter
def convert_markdown(value):
    md = markdown.Markdown(
        extensions=[
            # 空格 缩进等扩展
            'markdown.extensions.extra',
            # 代码语法高亮扩展
            'markdown.extensions.codehilite',
            # 目录扩展 TOC: Table of Contents
            'markdown.extensions.toc',
        ]
    )
    return md.convert(value)