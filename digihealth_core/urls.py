from django.contrib import admin
from django.urls import path, include
from notifications.views import dashboard

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', dashboard, name='student_dashboard'),
    path('consultations/', include('consultation.urls')),
]