from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('add/', views.add_task, name='add_task'),
    path('complete/<int:task_id>/', views.complete_task, name='complete_task'),
    path('delete/<int:task_id>/', views.delete_task, name='delete_task'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('', views.login, name='login'),
]