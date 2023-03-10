from django.urls import path
from .views import TaskList, DetailTask, CreateTask, \
    UpdateTask, DeleteTask, CustomLoginView, \
    RegisterPage, TaskReorder

from django.contrib.auth.views import LogoutView



urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', RegisterPage.as_view(), name='register'),

    path('', TaskList.as_view(), name='tasks'),
    path('task/<int:pk>/', DetailTask.as_view(), name='task'),
    path('task-create/', CreateTask.as_view(), name='task-create'),
    path('task-update/<int:pk>', UpdateTask.as_view(), name='task-update'),
    path('task-delete/<int:pk>', DeleteTask.as_view(), name='task-delete'),

    path('task-reorder/', TaskReorder.as_view(), name='task-reorder'),
]