from django.urls import path
from .views import index, add, edit, update_task_complete, delete_task

urlpatterns = [
    path('', index, name='index'),
    path('add/', add, name='add'),
    path('edit/<int:task_id>/', edit, name='edit'),
    path('update_task_complete/', update_task_complete, name='update_task_complete'),
    path('delete_task/', delete_task, name='delete_task'),
]
