from django.urls import path
from . import views

urlpatterns = [
    path('consultation/new/',     views.new_consultation,   name='new_consultation'),
    path('consultation/success/', views.consultation_success, name='consultation_success'),
]
