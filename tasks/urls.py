from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="list"),
    path('add/netflix/', views.add_netflix, name='add_netflix'),
    path('add/amazon/', views.add_amazon, name='add_amazon'),
    path('add/appletv/', views.add_appletv, name='add_appletv'),
    path('update_task/<str:pk>/', views.updateTask, name="update_task"),
    path('delete_task/<str:pk>/', views.deleteTask, name="delete"),
    path('delete_all/', views.deleteAllTasks, name='delete_all'),
]