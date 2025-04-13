from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.PostList.as_view(), name='home'),
    path('post/<slug:slug>/', views.PostDetail.as_view(), name='post_detail'),
    path('category/<slug:slug>/', views.CategoryView.as_view(), name='category'),
    path('archive/<int:year>/', views.ArchiveView.as_view(), name='archive_year'),
    path('archive/<int:year>/<int:month>/', views.ArchiveView.as_view(), name='archive_month'),
    path('about/', views.about, name='about'),
] 