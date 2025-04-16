from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.post_list, name='home'),
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),
    path('category/<slug:slug>/', views.category_view, name='category'),
    path('archive/<int:year>/', views.archive_view, name='archive_year'),
    path('archive/<int:year>/<int:month>/', views.archive_view, name='archive_month'),
    path('about/', views.about, name='about'),
] 