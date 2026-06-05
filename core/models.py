from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('STUDENT', 'Student'),
        ('DOCTOR', 'Doctor'),
        ('PHARMACIST', 'Pharmacist'),
        ('LAB_TECH', 'Lab Technician'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='STUDENT')
    phone = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.role}"

class PatientVisit(models.Model):
    STATUS_CHOICES = [
        ('WAITING', 'Waiting'),
        ('IN_CONSULTATION', 'In Consultation'),
        ('COMPLETED', 'Completed'),
        ('PRESCRIPTION_READY', 'Prescription Ready'),
    ]
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='visits')
    queue_number = models.IntegerField(unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='WAITING')
    assigned_doctor = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='assigned_visits')
    check_in_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Queue #{self.queue_number} - {self.student.get_full_name()}"

class Consultation(models.Model):
    visit = models.OneToOneField(PatientVisit, on_delete=models.CASCADE, related_name='consultation')
    symptoms = models.TextField()
    diagnosis = models.TextField()
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Consultation for {self.visit.student.get_full_name()}"

class Prescription(models.Model):
    consultation = models.OneToOneField(Consultation, on_delete=models.CASCADE, related_name='prescription')
    medication_name = models.CharField(max_length=100)
    dosage = models.CharField(max_length=50)
    frequency = models.CharField(max_length=50)
    duration_days = models.IntegerField()
    prescribed_by = models.ForeignKey(User, on_delete=models.CASCADE)
    prescribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Rx: {self.medication_name} for {self.consultation.visit.student.get_full_name()}"