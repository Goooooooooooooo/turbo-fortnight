"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views

app_name = 'article'

# 类视图时候要加括号:as_view() 普通方法不加括号:views.方法
urlpatterns = [
    path('article-list/', views.ArticleListView.as_view(), name='article-list'),
    # path('article/<int:id>/', views.article_detail, name='article-detail'),
    path('article-detail/<int:pk>/', views.ArticleDetailView.as_view(), name='article-detail'),
    path('article-delete/<int:pk>/', views.article_safe_delete, name='article-safe-delete'),
    path('article-create/', views.ArticleCreateView.as_view(), name='article-create'),
    path('article-portfolio/', views.portfolio, name='article-portfolio'),
]