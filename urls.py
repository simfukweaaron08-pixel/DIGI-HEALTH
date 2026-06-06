from django.urls import path
from . import views

app_name = 'queue'

urlpatterns = [
    # Student
    path('',                views.student_home,  name='student_home'),
    path('join/',           views.join_queue,    name='join'),
    path('cancel/',         views.cancel_queue,  name='cancel'),
    path('api/status/',     views.status_api,    name='status_api'),

    # Doctor
    path('doctor/',                     views.doctor_dashboard, name='doctor_dashboard'),
    path('doctor/call-next/',           views.call_next,        name='call_next'),
    path('doctor/start/<int:pk>/',      views.start_session,    name='start_session'),
    path('doctor/complete/<int:pk>/',   views.complete_session, name='complete_session'),
    path('doctor/no-show/<int:pk>/',    views.mark_no_show,     name='no_show'),
    path('doctor/api/live/',            views.live_queue_api,   name='live_api'),
]
