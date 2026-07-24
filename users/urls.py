from django.urls import path

from . import views

urlpatterns = [
    path('users/', views.UserListView.as_view(), name='users'),
    path('users/create/', views.RegisterView.as_view(), name='register'),
    path('users/<int:pk>/update/', views.UserUpdateView.as_view(), name='user_update'),
    path('users/<int:pk>/delete/', views.UserDeleteView.as_view(), name='user_delete'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
]
