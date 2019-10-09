from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from taggit.managers import TaggableManager
from PIL import Image
from ckeditor_uploader.fields import RichTextUploadingField



class Category(models.Model):
    name = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name



class ArticlePost(models.Model):

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    # 文章标题图
    avatar = models.ImageField(upload_to='article/%Y%m%d/', blank=True)
    title = models.CharField(max_length=100)
    body = models.TextField()
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = TaggableManager(blank=True)
    # 浏览量 PositiveIntegerField 正整数字段
    total_views = models.PositiveIntegerField(default=0)

    # save() model 内置方法，model实例保存时调用
    def save(self, *args, **kwargs):
        # 调用父类原有的 save() 方法，保存数据，先保存图片，后进行缩放处理，否则会报找不到图片错误
        article = super(ArticlePost, self).save(*args, **kwargs)

        # 缩放图片
        if self.avatar:
            img = Image.open(self.avatar)
            # 原始图片大小，按比例缩放
            (x, y) = img.size
            new_x = 400
            new_y = int(new_x * (y / x))
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

