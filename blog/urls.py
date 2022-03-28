from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views
from .tools import search

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('blog/', views.PostListView.as_view(), name='post-list'),
    path('post/create', views.PostCreateView.as_view(), name='post-create'),
    path('category/<slug:slug>/', views.CategoryListView.as_view(), name='category-list'),
    path('post/<slug:slug>/', views.PostDetailView.as_view(), name='post-detail'),
    path('post/<slug:slug>/update', views.PostUpdateView.as_view(), name='post-update'),
    path('post/<slug:slug>/delete', views.PostDeleteView.as_view(), name='post-delete'),
    path('search/', search, name='search')
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)