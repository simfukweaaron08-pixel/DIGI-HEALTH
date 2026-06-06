from django.contrib import admin
from .models import QueueCategory, QueueEntry, Notification

@admin.register(QueueCategory)
class QueueCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon', 'estimated_wait_minutes', 'is_active']

@admin.register(QueueEntry)
class QueueEntryAdmin(admin.ModelAdmin):
    list_display  = ['ticket_number', 'student', 'status', 'priority', 'category', 'joined_at']
    list_filter   = ['status', 'priority', 'category']
    search_fields = ['ticket_number', 'student__username', 'student__first_name']

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['queue_entry', 'message', 'is_read', 'created_at']
