from django import template
import markdown
from django.template.defaultfilters import stringfilter
from django.utils import timezone
import math
import datetime


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


@register.filter(name='timesince_zh')
def time_since_zh(value):
    now = timezone.now()
    diff = now - value

    if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
        return '刚刚'

    if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600:
        return str(math.floor(diff.seconds / 60)) + "分钟前"

    if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400:
        return str(math.floor(diff.seconds / 3600)) + "小时前"

    if diff.days >= 1 and diff.days < 30:
        return str(diff.days) + "天前"

    if diff.days >= 30 and diff.days < 365:
        return str(math.floor(diff.days / 30)) + "个月前"

    if diff.days >= 365:
        return str(math.floor(diff.days / 365)) + "年前"


# 返回指定格式时间
# {% current_time "%Y-%m-%d %I:%M %p" as the_time %} 在模板中保存时间
@register.simple_tag
def current_time(format_string):
    return datetime.datetime.now().strftime(format_string)