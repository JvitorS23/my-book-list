from django.urls import path

from . import views

app_name = 'user'

urlpatterns = [
    path('register/', views.RegisterUserView.as_view(), name='user-register'),
    path('login/', views.LoginView.as_view(), name='user-login'),
    path('logout/', views.LogoutView.as_view(), name='user-logout'),
    path('me/', views.ManageUserView.as_view(), name='me'),
]
