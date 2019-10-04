from django.contrib import admin
from .models import ArticlePost, Category
# Register your models here.


# 后台显示项目设置
class ArticlePostAdmin(admin.ModelAdmin):
    # 设置列表可显示的字段
    list_display = ('title', 'author',  'created', 'updated', 'category',)
    # 每页显示条目数
    list_per_page = 5
    # 按发布日期排序
    ordering = ('-created',)


# class CategoryAdmin(admin.ModelAdmin):
#     # 下拉菜单改成放大镜检索 单对多关系的选择 raw_id_fields
#     raw_id_fields = ['name',]


admin.site.register(ArticlePost, ArticlePostAdmin)
admin.site.register(Category)
