from django.urls import path
from .views import *

urlpatterns = [
    path('register/', register_view, name='register'),
    path('', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile_view, name='profile'),
    path('user_list/', user_list_view, name='user-list'), 
    path('user_list/<int:pk>/', user_detail_view, name='user-detail'),
    path('user/edit/<int:pk>/', edit_user_view, name='edit-user'),
    path('user_list/<int:pk>/manage-access/', manage_access_view, name='manage-access')
]