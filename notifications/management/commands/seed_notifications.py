from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from notifications.models import Notification

class Command(BaseCommand):
    help = 'Seeds the database with simulated notification data'

    def handle(self, *args, **kwargs):
        
        user, created = User.objects.get_or_create(username='teststudent')
        if created:
            user.set_password('unza2026')
            user.save()

      
        data = [
            {"title": "Consultation Response", "msg": "Dr. Theu has replied to your request.", "cat": "CONSULT"},
            {"title": "Lab Results", "msg": "Your malaria test results have been uploaded.", "cat": "LAB"},
            {"title": "Pharmacy Alert", "msg": "Your prescription is ready for pickup.", "cat": "PHARMA"},
        ]

        for item in data:
            Notification.objects.create(
                recipient=user,
                title=item['title'],
                message=item['msg'],
                category=item['cat']
            )
        
        self.stdout.write(self.style.SUCCESS('Successfully seeded simulated notifications!'))