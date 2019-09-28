from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views import generic
from .models import ArticlePost
from django.utils import timezone

# Create your views here.


class ArticleListView(generic.ListView):
    model = ArticlePost
    template_name = 'article/index.html'
    context_object_name = 'article_list'
    # paginate_by = 3

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
    template_name = 'article/detail.html'
    context_object_name = 'article_detail'

    class Meta:
        pass

    def get_context_data(self, **kwargs):
        # article = get_object_or_404(ArticlePost, id=self.kwargs.get('pk'))
        context = super(ArticleDetailView, self).get_context_data(**kwargs)
        return context

    # def article_detail(request,id):
    #     article = ArticlePost.objects.get(id=id)
    #     context = {'article': article}
    #
    #     return render(request, 'article/detail.html', context)

