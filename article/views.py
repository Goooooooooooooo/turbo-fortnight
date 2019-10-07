from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
from django.views import generic
from .models import ArticlePost
from django.utils import timezone
from .forms import ArticlePostForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q


# 单纯的迁移画面，不做额外的处理
def portfolio(request):
    return render(request, 'article/portfolio.html')


# [@login_required] 修饰器，不改动View的情况下，额外添加功能
@login_required(login_url='/userprofile/login/')
def article_safe_delete(request, pk):
    if request.method == 'POST':
        article = ArticlePost.objects.get(id=pk)
        article.delete()
        return redirect("article:article-list")
    else:
        return HttpResponse("仅允许post请求")



# 主页显示View
class ArticleListView(generic.ListView):
    model = ArticlePost
    template_name = 'article/index.html'
    context_object_name = 'article_list'
    paginate_by = 10

    class Meta:
        pass

    def get_queryset(self):
        search = self.request.GET.get('search')
        category = self.request.GET.get('category')
        tag = self.request.GET.get('tag')

        article_list = ArticlePost.objects.all()
        if search:
            article_list = article_list.filter(Q(title__icontains=search) | Q(body__icontains=search))

        if category is not None and category.isdigit():
            article_list = article_list.filter(column=category)

        if tag and tag != 'None':
            article_list = article_list.filter(tags__name__in=[tag])

        return article_list


    def get_context_data(self, **kwargs):
        context = super(ArticleListView, self).get_context_data(**kwargs)
        context['now'] = timezone.now
        context['search'] = self.request.GET.get('search')
        context['category'] = self.request.GET.get('category')
        context['tag'] = self.request.GET.get('tag')
        return context



# 单篇文章详细
class ArticleDetailView(generic.DeleteView):
    model = ArticlePost
    # 指定渲染的模板
    template_name = 'article/detail.html'
    # 指定获取的 model 对象名字
    context_object_name = 'article_detail'
    pk_url_kwarg = 'pk'

    # get_object方法默认情况下获取 id 为pk_url_kwarg 的对象
    # 需要在获取过程中对获取对象做一些处理，可以通过复写 get_object 实现
    def get_object(self, queryset=None):
        article = super(ArticleDetailView, self).get_object()
        # 浏览数增加 除了作者本人
        if self.request.user != article.author:
            article.total_views += 1
            # 只更新浏览数字段
            article.save(update_fields=['total_views'])
        return article

    '''
    # 复写 get_context_data 方法为上下文对象添加额外的变量，以便在模板中访问
    def get_context_data(self, **kwargs):
        article = get_object_or_404(ArticlePost, id=self.kwargs.get('pk'))
        # context = super(ArticleDetailView, self).get_context_data(**kwargs)
        context = {'article_detail': article}
        return context
    '''

    '''
    # 普通视图获取方法
    def article_detail(request,id):
        article = ArticlePost.objects.get(id=id)
        context = {'article': article}
        return render(request, 'article/detail.html', context)
    '''

# 创建新文章
class ArticleCreateView(LoginRequiredMixin, generic.CreateView):
    # 如果用户未登录 跳转到登录页面
    login_url = '/userprofile/login/'

    model = ArticlePost
    form_class = ArticlePostForm
    template_name = 'article/create.html'

    # 确认 form 的值是不是有效，可以设置默认值
    def form_valid(self, form):
        # 从url中获取pk值，根据pk值找到对应的数据
        pk = self.kwargs.get(self.pk_url_kwarg)

        # 设置默认值
        # form.instance.project = get_object_or_404(ArticlePost, pk=pk)
        # 文章作者默认为当前登录用户
        form.instance.author = self.request.user
        form.instance.avatar = self.request.FILES.get('file_img')
        return super().form_valid(form)

    # # 定义表对象没有添加失败后跳转到的页面。
    # def form_invalid(self, form):
    #     # 取出验证失败的信息,方便定位问题,给用用户提示
    #     Error_Dict = ArticlePostForm.errors
    #     # for value in  Error_Dict.values():
    #     #     logger.debug(value)
    #     # return HttpResponse(ErrorDict.__repr__())
    #     return HttpResponse('Error {}'.format(Error_Dict))


class ArticleUpdateView(LoginRequiredMixin, generic.UpdateView):
    login_url = '/userprofile/login/'
    model = ArticlePost
    context_object_name = 'article'
    template_name = 'article/update.html'
    form_class = ArticlePostForm
    pk_url_kwarg = 'pk'

    def get_object(self, queryset=None):
        article = super(ArticleUpdateView, self).get_object()
        if article.author == self.request.user:
            return article
        else:
            return HttpResponse('无权修改此文章！！！')

    def form_valid(self, form):
        form.instance.avatar = self.request.FILES.get('file_img')
        return super().form_valid(form)





