from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from notifications.views import dashboard

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', dashboard, name='student_dashboard'),
    path('doctor/', include('doctor.urls')),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
]
