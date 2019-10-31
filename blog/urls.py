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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from article.views import ArticleListView

urlpatterns = [
    path('admin/', admin.site.urls),
    # home
    path('', ArticleListView.as_view(), name='home'),
    # 直接返回视图，不渲染
    path('404/',TemplateView.as_view(template_name='404.html'), name='page_404'),
    path('article/', include('article.urls', namespace='article')),
    path('userprofile/', include('userprofile.urls', namespace='userprofile')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    # path('password-reset/', include('password_reset.urls')),
    path('comment/', include('comment.urls', namespace='comment')),
    path('accounts/', include('allauth.urls'))
]

handler400 = "article.views.bad_request"
handler403 = "article.views.permission_denied"
handler404 = "article.views.page_not_found"
handler500 = "article.views.server_error"

# settings.py 中添加了 MEDIA_URL MEDIA_ROOT，在这里配置媒体文件的 URL
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)