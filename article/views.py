from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
from django.views import generic
from .models import ArticlePost
from django.utils import timezone
from .forms import ArticlePostForm
from django.core.paginator import Paginator

# Create your views here.


def portfolio(request):
    return render(request, 'article/portfolio.html')


@login_required(login_url='/userprofile/login/')
def article_safe_delete(request, pk):
    if request.method == 'POST':
        article = ArticlePost.objects.get(id=pk)
        article.delete()
        return redirect("article:article-list")
    else:
        return HttpResponse("仅允许post请求")


class ArticleListView(generic.ListView):
    model = ArticlePost
    template_name = 'article/index.html'
    context_object_name = 'article_list'
    paginate_by = 5

    class Meta:
        pass

    # def get_queryset(self):
    #     return ArticlePost.objects.filter(title='')

    def get_context_data(self, **kwargs):
        context = super(ArticleListView, self).get_context_data(**kwargs)
        context['now'] = timezone.now
        return context


class ArticleDetailView(generic.DeleteView):
    model = ArticlePost
    # 指定渲染的模板
    template_name = 'article/detail.html'
    # 指定获取的 model 对象名字
    context_object_name = 'article_detail'
    pk_url_kwarg = 'pk'

    # get_object方法默认情况下获取 id 为pk_url_kwarg 的对象
    # 需要在获取过程中对获取对象做一些处理，可以通过复写 get_object 实现
    # def get_object(self, queryset=None):
    #     obj = super(ArticleDetailView, self).get_object()
    #     return obj

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


class ArticleCreateView(generic.CreateView):
    model = ArticlePost
    form_class = ArticlePostForm
    # fields = ['author', 'title', 'category', 'tags', 'body']
    template_name = 'article/create.html'

    def form_valid(self, form):
        # 从url中获取pk值，根据pk值找到对应的数据
        pk = self.kwargs.get(self.pk_url_kwarg)
        # 设置默认值
        # form.instance.project = get_object_or_404(ArticlePost, pk=pk)
        # 文章作者默认为当前登录用户
        form.instance.author = self.request.user.username
        return super().form_valid(form)


class ArticleUpdateView(generic.UpdateView):
    model = ArticlePost
    template_name = 'article/update.html'
    pass




