from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Profile
# Register your models here.


# 定义一个行内 admin
# 显示多个数据表数据在同一页面上之InlineModelAdmin类
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'


# 将 Profile 关联到 User 中
class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)


# 重新注册 User
admin.site.unregister(User)
admin.site.register(User, UserAdmin)