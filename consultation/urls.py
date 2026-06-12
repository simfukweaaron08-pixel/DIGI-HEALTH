from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_consultation, name='create_consultation'),
    path('success/', views.consultation_success, name='consultation_success'),
]