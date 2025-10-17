from django.urls import path

from authentication import views

app_name = 'authentication'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.user_register, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('list-users/', views.list_users, name='list_users'),
    path('user-detail/<uuid:user_id>/', views.user_detail, name='user_detail'),
    path('change-password/', views.change_password, name='change_password'),
    path('profile/', views.profile, name='profile')
]