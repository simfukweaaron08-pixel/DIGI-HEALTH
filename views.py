from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from django.db import models as dm

from .models import QueueEntry, QueueCategory, Notification


# ── Helpers ──────────────────────────────────────────────────────────────────

def is_doctor(user):
    return user.groups.filter(name='Doctors').exists() or user.is_staff

def notify(entry, msg):
    Notification.objects.create(queue_entry=entry, message=msg)


# ── Student Views ─────────────────────────────────────────────────────────────

@login_required
def student_home(request):
    active = QueueEntry.objects.filter(
        student=request.user,
        status__in=['waiting', 'called', 'in_session']
    ).first()
    categories     = QueueCategory.objects.filter(is_active=True)
    total_waiting  = QueueEntry.objects.filter(status='waiting').count()
    unread         = Notification.objects.filter(
        queue_entry__student=request.user, is_read=False
    ).order_by('-created_at')[:5]

    return render(request, 'queue/student_home.html', {
        'active':        active,
        'categories':    categories,
        'total_waiting': total_waiting,
        'notifications': unread,
    })


@login_required
def join_queue(request):
    if request.method != 'POST':
        return redirect('queue:student_home')

    if QueueEntry.objects.filter(
        student=request.user,
        status__in=['waiting', 'called', 'in_session']
    ).exists():
        messages.warning(request, 'You are already in the queue.')
        return redirect('queue:student_home')

    cat_id  = request.POST.get('category')
    reason  = request.POST.get('visit_reason', '').strip()
    cat     = get_object_or_404(QueueCategory, pk=cat_id, is_active=True) if cat_id else None

    entry = QueueEntry.objects.create(
        student=request.user,
        unza_student_id=getattr(request.user, 'username', ''),
        category=cat,
        visit_reason=reason,
    )
    notify(entry, f'You joined the queue. Your ticket is {entry.ticket_number}. '
                  f'Estimated wait: ~{cat.estimated_wait_minutes if cat else 20} mins.')
    messages.success(request, f'Ticket {entry.ticket_number} issued. Please wait to be called.')
    return redirect('queue:student_home')


@login_required
def cancel_queue(request):
    if request.method != 'POST':
        return redirect('queue:student_home')
    entry = QueueEntry.objects.filter(
        student=request.user, status__in=['waiting', 'called']
    ).first()
    if entry:
        entry.status = 'cancelled'
        entry.save()
        notify(entry, 'You have left the queue.')
        messages.info(request, 'You have been removed from the queue.')
    return redirect('queue:student_home')


@login_required
def status_api(request):
    """JSON: student polls every 15s for live updates."""
    entry = QueueEntry.objects.filter(
        student=request.user,
        status__in=['waiting', 'called', 'in_session']
    ).first()
    if not entry:
        return JsonResponse({'in_queue': False})

    new_notifs = list(
        Notification.objects.filter(queue_entry=entry, is_read=False)
        .values_list('message', flat=True)
    )
    Notification.objects.filter(queue_entry=entry, is_read=False).update(is_read=True)

    return JsonResponse({
        'in_queue':       True,
        'ticket':         entry.ticket_number,
        'status':         entry.status,
        'status_display': entry.get_status_display(),
        'position':       entry.queue_position if entry.status == 'waiting' else 0,
        'wait_minutes':   entry.wait_minutes,
        'notifications':  new_notifs,
    })


# ── Doctor Views ──────────────────────────────────────────────────────────────

@login_required
@user_passes_test(is_doctor)
def doctor_dashboard(request):
    waiting       = QueueEntry.objects.filter(status='waiting').select_related('student', 'category')
    called        = QueueEntry.objects.filter(status='called').select_related('student', 'category')
    in_session    = QueueEntry.objects.filter(status='in_session', assigned_doctor=request.user)
    completed_today = QueueEntry.objects.filter(
        status='completed',
        assigned_doctor=request.user,
        completed_at__date=timezone.now().date()
    ).count()

    return render(request, 'queue/doctor_dashboard.html', {
        'waiting':         waiting,
        'called':          called,
        'in_session':      in_session,
        'total_waiting':   waiting.count(),
        'completed_today': completed_today,
    })


@login_required
@user_passes_test(is_doctor)
def call_next(request):
    if request.method != 'POST':
        return redirect('queue:doctor_dashboard')
    nxt = QueueEntry.objects.filter(status='waiting').first()
    if not nxt:
        messages.info(request, 'No patients waiting.')
        return redirect('queue:doctor_dashboard')
    nxt.status          = 'called'
    nxt.called_at       = timezone.now()
    nxt.assigned_doctor = request.user
    nxt.save()
    notify(nxt, f'Ticket {nxt.ticket_number}: Please proceed to the consultation room now.')
    messages.success(request, f'Called {nxt.ticket_number} — {nxt.student.get_full_name()}.')
    return redirect('queue:doctor_dashboard')


@login_required
@user_passes_test(is_doctor)
def start_session(request, pk):
    entry = get_object_or_404(QueueEntry, pk=pk, status='called', assigned_doctor=request.user)
    entry.status         = 'in_session'
    entry.session_started = timezone.now()
    entry.save()
    return redirect('queue:doctor_dashboard')


@login_required
@user_passes_test(is_doctor)
def complete_session(request, pk):
    entry = get_object_or_404(QueueEntry, pk=pk, status='in_session', assigned_doctor=request.user)
    entry.status       = 'completed'
    entry.completed_at = timezone.now()
    entry.save()
    messages.success(request, f'Session completed for {entry.ticket_number}.')
    return redirect('queue:doctor_dashboard')


@login_required
@user_passes_test(is_doctor)
def mark_no_show(request, pk):
    entry = get_object_or_404(QueueEntry, pk=pk, status='called')
    entry.status = 'no_show'
    entry.save()
    messages.warning(request, f'{entry.ticket_number} marked as no-show.')
    return redirect('queue:doctor_dashboard')


@login_required
@user_passes_test(is_doctor)
def live_queue_api(request):
    """JSON: doctor dashboard polls for live queue list."""
    now = timezone.now()
    rows = []
    for e in QueueEntry.objects.filter(status='waiting').select_related('student', 'category'):
        rows.append({
            'id':           e.pk,
            'ticket':       e.ticket_number,
            'name':         e.student.get_full_name() or e.student.username,
            'unza_student_id':   e.unza_student_id,
            'category':     e.category.name if e.category else 'General',
            'reason':       e.visit_reason or '—',
            'wait_minutes': int((now - e.joined_at).total_seconds() / 60),
            'priority':     e.priority,
            'priority_label': e.get_priority_display(),
        })
    return JsonResponse({'waiting': rows, 'count': len(rows)})
