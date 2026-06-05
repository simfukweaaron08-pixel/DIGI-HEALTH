from django.urls import include, path

from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.home_redirect, name='home'),
    path('login/', views.login_page_view, name='login_page'),
    path('register/', views.register_page_view, name='register_page'),
    path('dashboard/', views.dashboard_page_view, name='dashboard_page'),
    path('auth/register/', views.register_view, name='register'),
    path('auth/login/', views.login_view, name='login'),
    path('auth/logout/', views.logout_view, name='logout'),
    path('auth/dashboard/', views.dashboard_api_view, name='dashboard_api'),
    path('auth/csrf-token/', views.csrf_token_view, name='csrf_token'),
    path('auth/', include('django.contrib.auth.urls')),
]
