from django.urls import path
from .views import *


urlpatterns = [
    # path('articles/', article_list_create_api_view, name='article_list'),
    # path('articles/<int:pk>', article_detail_api_view, name='article_detail'),
    path('articles_all/', ArticleListCreateView.as_view(), name='article_all'),
    path('articles_detail/<int:pk>', ArticleDetailAPIView.as_view(), name='article_list_detail'),
    path('author/', JournalistListCreateView.as_view(), name='author_list'),
]
