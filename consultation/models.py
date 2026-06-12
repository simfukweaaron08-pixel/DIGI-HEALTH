from django.db import models
from django.conf import settings

class Consultation(models.Model):
    DURATION_CHOICES = [
        ('less_than_a_day', 'Less than a day'),
        ('1_to_3_days',     '1 to 3 days'),
        ('more_than_a_week','More than a week'),
    ]
    SEVERITY_CHOICES = [
        ('Mild',     'Mild'),
        ('Moderate', 'Moderate'),
        ('Severe',   'Severe'),
    ]
    STATUS_CHOICES = [
        ('Pending',     'Pending'),
        ('Assigned',    'Assigned'),
        ('In Progress', 'In Progress'),
        ('Completed',   'Completed'),
    ]

    student              = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    symptoms             = models.TextField()
    duration             = models.CharField(max_length=100)  # Changed to allow custom text
    severity             = models.CharField(max_length=10, choices=SEVERITY_CHOICES)
    taking_medications   = models.BooleanField(default=False)
    medications_details  = models.TextField(blank=True, null=True, help_text="If yes, please list the medications")
    image                = models.ImageField(upload_to='consultations/images/', blank=True, null=True)
    video                = models.FileField(upload_to='consultations/videos/', blank=True, null=True)
    status               = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at           = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.get_full_name()} – {self.severity} – {self.status}"