from django.contrib import admin
from django.urls import path, include
from .views import IndexView, ArticleUpdateView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('<int:pk>/update/', ArticleUpdateView.as_view(), name='article-update')
]