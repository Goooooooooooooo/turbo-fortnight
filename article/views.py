from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import generic
from .models import ArticlePost, Category
from taggit.models import Tag
from django.utils import timezone
from .forms import ArticlePostForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.db.models.aggregates import Count
from comment.models import Comment
from comment.forms import CommentForm
import markdown
import logging

logging.getLogger().setLevel(logging.INFO)

'''
    # 复写 get_context_data 方法为上下文对象添加额外的变量，以便在模板中访问
    # 复写 get_queryset 方法过滤数据
    # get_object方法默认情况下获取 id 为pk_url_kwarg 的对象
    # 需要在获取过程中对获取对象做一些处理，可以通过复写 get_object 实现
    # [@login_required] 修饰器，不改动View的情况下，额外添加功能
    # 因为所有的请求方法在类视图中最终都会通过diapatch这个方法，
    # 所以我们需要重写dispatch方法，并且继承至父类的dispatch方法。
    def dispatch(self, request, *args, **kwargs):
       return super(Profileview,self).dispatch(request,*args,**kwargs)
    # 直接在类视图上面添加装饰器 同样可以实现给类视图的所有方法添加装饰器功能
    # @method_decorator(my_decorator, name='dispatch')  
    # model = ArticlePost                   # 指定模型
    # template_name = 'article/index.html'  # 指定模板
    # context_object_name = 'article_list'  # 指定列表模型在模板中的名称
    # paginate_by = 10                      # 每页展示数据条数
    # ordering = 'created'                  # 排序（以创建时间）
    # page_kwarg = 'p'                      # 指定页面参数，默认为 page(包含page_obj类，paginator类) 以 GET 方式传递数据
    # Paginator和Page类都是用来做分页的。他们在Django中的路径为django.core.paginator.Paginator和django.core.paginator.Page。
    # Paginator常用属性和方法：
    # count：总共有多少条数据。
    # num_pages：总共有多少页。
    # page_range：页面的区间。比如有三页，那么就range(1,4)。
    # article.save(update_fields=['total_views']) # update_fields=['files_name'] 只更新指定字段
    # page类的常用属性和方法：
    # has_next：是否还有下一页。
    # has_previous：是否还有上一页。
    # next_page_number：下一页的页码。
    # previous_page_number：上一页的页码。
    # number：当前页。 只有这一个是属性，其他的都是方法
    # start_index：当前这一页的第一条数据的索引值。
    # end_index：当前这一页的最后一条数据的索引值
    # render方法有4个参数。1.request, 2.模板的名称和位置，3.需要传递给模板的内容, 也被称为context object。4.可选参数content_type（内容类型)
    # 展示对象列表（比如所有用户，所有文章）- ListView
    # 展示某个对象的详细信息（比如用户资料，比如文章详情) - DetailView
    # 通过表单创建某个对象（比如创建用户，新建文章）- CreateView
    # 通过表单更新某个对象信息（比如修改密码，修改文字内容）- UpdateView
    # 用户填写表单后转到某个完成页面 - FormView
    # 删除某个对象 - DeleteView
    # 上述常用通用视图一共有6个，前2个属于展示类视图(Display view), 后面4个属于编辑类视图(Edit view)。
    # 重要：如果你要使用 Edit view，请务必在模型 models 里定义 get_absolute_url() 方法，否则会出现错误。这是因为通用视图在对一个对象完成编辑后，需要一个返回链接。
    # raise Http404() 直接返回 404 错误
    # form_valid() :
    # 虽然 form_valid 方法不是必需，但当用户提交的数据是有效的时候，你可以通过定义此方法做些别的事情，比如发送邮件，存取额外的数据。
    # 定义表对象没有添加失败后跳转到的页面。
    def form_invalid(self, form):
    # 取出验证失败的信息,方便定位问题,给用用户提示
     Error_Dict = ArticlePostForm.errors
     for value in  Error_Dict.values():
         logger.debug(value)
         return HttpResponse(ErrorDict.__repr__())
         return HttpResponse('Error {}'.format(Error_Dict))
    # 从url中获取pk值，根据pk值找到对应的数据
    # pk = self.kwargs.get(self.pk_url_kwarg) 
    # 设置默认值
    # form.instance.project = get_object_or_404(ArticlePost, pk=pk)
    #  普通获取方法
    def article_detail(request,pk):
        article = ArticlePost.objects.get(pk=pk) # OR article = get_object_or_404(ArticlePost, pk=pk)
        context = {'article': article}
        return render(request, 'article/detail.html', context)
'''

# 全局 400 处理函数
def bad_request(request, exception=None):
    from django.shortcuts import render_to_response
    # django 内置函数生成 response 对象，可以传递参数 context{}
    response = render_to_response('400.html', {})
    # 设置状态码
    response.status_code = 400
    return response

# 全局 403 处理函数
def permission_denied(request, exception=None):
    from django.shortcuts import render_to_response
    response = render_to_response('403.html', {})
    response.status_code = 403
    return response

# 全局 404 处理函数
def page_not_found(request, exception=None):
    from django.shortcuts import render_to_response
    response = render_to_response('404.html', {})
    response.status_code = 404
    return response

# 全局 500 处理函数
def server_error(request, exception=None):
    from django.shortcuts import render_to_response
    response = render_to_response('500.html', {})
    response.status_code = 500
    return response


# 单纯的迁移画面，不做额外的处理
def portfolio(request):
    return render(request, 'article/portfolio.html')



@login_required(login_url='/account/login/')
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

    # 过滤数据
    def get_queryset(self):
        search = self.request.GET.get('search')
        category = self.request.GET.get('category')
        tag = self.request.GET.get('tag')

        article_list = ArticlePost.objects.all()
        if search:
            article_list = article_list.filter(Q(title__icontains=search) | Q(body__icontains=search))
        if category is not None and category.isdigit():
            article_list = article_list.filter(category=category)
        if tag and tag != 'None':
            article_list = article_list.filter(tags__name__in=[tag])
        return article_list

    def get_context_data(self, **kwargs):
        # 继承至父模板的get_context_data方法，否则我们有很多方法将不能使用
        context = super(ArticleListView, self).get_context_data(**kwargs)
        # paginator = context.get('paginator')  # paginator类
        context['now'] = timezone.now
        context['search'] = self.request.GET.get('search')
        context['tags'] = Tag.objects.all()
        # Count 计算分类下的文章数，其接受的参数为需要计数的模型的名称
        context['category_list'] = Category.objects.annotate(num_posts=Count('articlepost'))
        return context



# 单篇文章详细
class ArticleDetailView(generic.DeleteView):

    model = ArticlePost
    template_name = 'article/detail.html'
    context_object_name = 'article_detail'
    pk_url_kwarg = 'pk'


    def get_object(self, queryset=None):
        article = super(ArticleDetailView, self).get_object()
        if self.request.user != article.author:
            article.total_views += 1
            # 只更新浏览数字段
            article.save(update_fields=['total_views'])
        return article

    def get_context_data(self, **kwargs):
        context = super(ArticleDetailView, self).get_context_data(**kwargs)
        pk = self.kwargs.get(self.pk_url_kwarg)
        comments = Comment.objects.filter(article=pk)
        md = markdown.Markdown(extensions=['markdown.extensions.toc',])
        context['toc'] = md.toc
        context['comments'] = comments
        context['comment_form'] = CommentForm()
        context['next_article'] = context['article_detail'].get_pre_article(pk=pk)
        context['pre_article'] = context['article_detail'].get_next_article(pk=pk)
        return context




# 创建新文章
class ArticleCreateView(LoginRequiredMixin, generic.CreateView):
    # 如果用户未登录 跳转到登录页面
    login_url = '/accounts/login/'

    model = ArticlePost
    form_class = ArticlePostForm
    template_name = 'article/create.html'

    # 确认 form 的值是不是有效，可以设置默认值
    def form_valid(self, form):
        # 文章作者默认为当前登录用户
        form.instance.author = self.request.user
        form.instance.avatar = self.request.FILES.get('file_img')
        return super().form_valid(form)



class ArticleUpdateView(LoginRequiredMixin, generic.UpdateView):
    login_url = '/account/login/'
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





