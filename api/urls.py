from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import register_user, create_task, assign_task, get_tasks_for_user

urlpatterns = [
    path('register/', register_user, name='register_user'),
    path('login/', TokenObtainPairView.as_view(), name='login'), 
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('tasks/', create_task, name='create_task'),
    path('tasks/<int:task_id>/assign/', assign_task, name='assign_task'),
    path('tasks/user/<int:user_id>/', get_tasks_for_user, name='get_tasks_for_user'),
]
