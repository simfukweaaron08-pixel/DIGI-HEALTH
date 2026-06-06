from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import random, string


def generate_ticket():
    prefix = 'DH-' + random.choice(string.ascii_uppercase)
    num    = str(random.randint(1, 999)).zfill(3)
    ticket = prefix + num
    while QueueEntry.objects.filter(ticket_number=ticket).exists():
        num    = str(random.randint(1, 999)).zfill(3)
        ticket = prefix + num
    return ticket


class QueueCategory(models.Model):
    name                    = models.CharField(max_length=100)
    icon                    = models.CharField(max_length=10, default='🏥')
    estimated_wait_minutes  = models.IntegerField(default=15)
    is_active               = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Queue Categories'


class QueueEntry(models.Model):
    STATUS_CHOICES = [
        ('waiting',    'Waiting'),
        ('called',     'Called'),
        ('in_session', 'In Session'),
        ('completed',  'Completed'),
        ('no_show',    'No Show'),
        ('cancelled',  'Cancelled'),
    ]
    PRIORITY_CHOICES = [
        (1, 'Emergency'),
        (2, 'Urgent'),
        (3, 'Normal'),
    ]

    student          = models.ForeignKey(User, on_delete=models.CASCADE, related_name='queue_entries')
    unza_student_id  = models.CharField(max_length=20, blank=True)
    category         = models.ForeignKey(QueueCategory, on_delete=models.SET_NULL, null=True, blank=True)
    ticket_number    = models.CharField(max_length=10, unique=True, default=generate_ticket)
    priority         = models.IntegerField(choices=PRIORITY_CHOICES, default=3)
    status           = models.CharField(max_length=20, choices=STATUS_CHOICES, default='waiting')
    visit_reason     = models.CharField(max_length=200, blank=True)

    joined_at        = models.DateTimeField(default=timezone.now)
    called_at        = models.DateTimeField(null=True, blank=True)
    session_started  = models.DateTimeField(null=True, blank=True)
    completed_at     = models.DateTimeField(null=True, blank=True)

    assigned_doctor  = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='assigned_entries'
    )

    class Meta:
        ordering = ['priority', 'joined_at']

    def __str__(self):
        return f'{self.ticket_number} – {self.student.get_full_name()}'

    @property
    def wait_minutes(self):
        end = self.called_at or timezone.now()
        return int((end - self.joined_at).total_seconds() / 60)

    @property
    def queue_position(self):
        return QueueEntry.objects.filter(
            status='waiting',
        ).filter(
            models.Q(priority__lt=self.priority) |
            models.Q(priority=self.priority, joined_at__lt=self.joined_at)
        ).count() + 1


class Notification(models.Model):
    queue_entry = models.ForeignKey(QueueEntry, on_delete=models.CASCADE, related_name='notifications')
    message     = models.TextField()
    is_read     = models.BooleanField(default=False)
    created_at  = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_at']
