from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from taggit.managers import TaggableManager
from PIL import Image
from ckeditor_uploader.fields import RichTextUploadingField
import markdown
from django.utils.html import strip_tags



class Category(models.Model):
    name = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name



class ArticlePost(models.Model):

    objects = models.Manager()

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    # 文章标题图
    avatar = models.ImageField(upload_to='article/%Y%m%d/', blank=True)
    title = models.CharField(max_length=100)
    # 文章简介
    summary = models.CharField(max_length=200, blank=True)
    body = models.TextField()
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = TaggableManager(blank=True)
    # 浏览量 PositiveIntegerField 正整数字段
    total_views = models.PositiveIntegerField(default=0)

    # save() model 内置方法，model实例保存时调用
    def save(self, *args, **kwargs):
        # 如果没有填写摘要
        if not self.summary:
            # 首先实例化一个 Markdown 类，用于渲染 body 的文本
            md = markdown.Markdown(extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
            ])
            # 先将 Markdown 文本渲染成 HTML 文本
            # strip_tags 去掉 HTML 文本的全部 HTML 标签
            # 从文本摘取前 100 个字符赋给 summary
            self.summary = strip_tags(md.convert(self.body))[:100]

        # 调用父类原有的 save() 方法，保存数据，先保存图片，后进行缩放处理，否则会报找不到图片错误
        article = super(ArticlePost, self).save(*args, **kwargs)

        # 缩放图片
        if self.avatar:
            img = Image.open(self.avatar)
            # 原始图片大小，按比例缩放
            (x, y) = img.size
            rate = 1.0  # 压缩率

            # 根据图像大小设置压缩率
            if x >= 2000 or y >= 2000:
                rate = 0.3
            elif x >= 1000 or y >= 1000:
                rate = 0.5
            elif x >= 500 or y >= 500:
                rate = 0.9

            new_x = int(x * rate)
            new_y = int(y * rate)
            resized_img = img.resize((new_x, new_y), Image.ANTIALIAS)
            # self.avatar.name: 文件名路径 .path: 完整路径
            resized_img.save(self.avatar.path)

        return article

    class Meta:
        # 按创建时间排序
        ordering = ('-created',)

    # 新建文章，更新文章后 返回详细视图
    def get_absolute_url(self):
        return reverse('article:article-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title

    '''
        一般来说，要使用某个类的方法，需要先实例化一个对象再调用方法。
        而使用 @staticmethod 或 @classmethod，就可以不需要实例化，直接类名.方法名()来调用。
        这有利于组织代码，把某些应该属于某个类的函数给放到那个类里去，同时有利于命名空间的整洁。
        如果在 @staticmethod 中要调用到这个类的一些属性方法，只能直接类名.属性名或类名.方法名。
        而 @classmethod 因为持有 cls 参数，可以来调用类的属性，类的方法，实例化对象等，避免硬编码。

        上一篇：小于当前 id 的第一篇，下一篇：大于当前 id 的第一篇
        @staticmethod 不需要表示自身对象的 self 和自身类的 cls 参数，就跟使用函数一样
        @classmethod 不需要 self 参数，但第一个参数需要是表示自身类的 cls 参数。
    '''
    # 上一篇
    @classmethod
    def get_pre_article(cls, pk):
        pre_article = cls.objects.filter(id__lt=pk).order_by('-id')
        # 取出相邻前一篇文章
        if pre_article.count() > 0:
            pre_article = pre_article[0]
        else:
            pre_article = None
        return pre_article

    # 下一篇
    @classmethod
    def get_next_article(cls, pk):
        next_article = cls.objects.filter(id__gt=pk).order_by('id')
        # 取出相邻后一篇文章
        if next_article.count() > 0:
            next_article = next_article[0]
        else:
            next_article = None
        return next_article
