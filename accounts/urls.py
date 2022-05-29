from django.urls import path
from . import views

urlpatterns = [
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('logout', views.logout, name='logout'),
    path('admin_dashboard', views.admin_dashboard, name='admin_dashboard'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('add_images', views.add_images, name='add_images'),
    path('train', views.train, name='train'),
    path('mark_in', views.mark_in, name='mark_in'),
    path('mark_out', views.mark_out, name='mark_out'),
    path('admin_analytics', views.admin_analytics, name='admin_analytics'),
    path('analytics', views.analytics, name='analytics'),
    path('search_by_username', views.search_by_username, name='search_by_username'),
    path('search_by_date', views.search_by_date, name='search_by_date'),
    path('update', views.update, name='update'),
]
