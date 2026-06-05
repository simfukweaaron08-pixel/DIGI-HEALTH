from django.urls import path
from . import views

app_name = 'doctor'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('prescription/create/<int:visit_id>/', views.create_prescription, name='create_prescription'),
]