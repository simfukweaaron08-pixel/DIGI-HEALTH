from django.db import models
from django.conf import settings  

class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('CONSULT', 'Consultation Update'),
        ('LAB', 'Lab Result Ready'),
        ('PHARMA', 'Prescription Ready'),
    )

    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    title = models.CharField(max_length=200)
    message = models.TextField()
    category = models.CharField(max_length=10, choices=NOTIFICATION_TYPES)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.category}: {self.title} for {self.recipient.username}"