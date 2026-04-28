from django.shortcuts import render
from .models import Notification

def dashboard(request):
    
    notes = Notification.objects.all().order_by('-created_at')
    return render(request, 'notifications/dashboard.html', {'notifications': notes})