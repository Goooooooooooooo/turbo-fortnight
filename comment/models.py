from django.db import models
from django.contrib.auth.models import User
from article.models import ArticlePost
from mptt.models import MPTTModel, TreeForeignKey


# Create your models here.
#
# class BaseComment(models.Model):
#     # 基础评论模型
#     content = models.TextField('评论', max_length=500)
#     time = models.DateTimeField('评论时间', auto_now_add=True)
#     user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='评论者')
#     class Meta:
#         abstract = True
#
# class ArticleComment(BaseComment):
#     '文章评论'
#     article = models.ForeignKey(ArticlePost, on_delete=models.CASCADE, related_name='comments', verbose_name='评论文章')
#     class Meta:
#         ordering = ['-time']
#
# class ArticleCommentReply(BaseComment):
#     '文章评论回复(二级评论)'
#     comment = models.ForeignKey(ArticleComment, on_delete=models.CASCADE, related_name='replies', verbose_name='一级评论')
#     reply = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, verbose_name='回复对象')
#     class Meta:
#         ordering = ['time']



class Comment(MPTTModel):

    article = models.ForeignKey(ArticlePost, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    body = models.TextField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    # 新增，mptt树形结构
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    # 新增，记录二级评论回复给谁, str
    reply_to = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, related_name='replyers')

    # 替换 Meta 为 MPTTMeta
    # class Meta:
    #     ordering = ('created',)
    class MPTTMeta:
        order_insertion_by = ['created']