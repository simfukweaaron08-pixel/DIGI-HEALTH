from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from core.models import PatientVisit, Prescription
from .forms import PrescriptionForm

@login_required
def dashboard(request):
    """Shows the list of patients assigned to the doctor"""
    patients = PatientVisit.objects.filter(
        assigned_doctor=request.user,
        status__in=['WAITING', 'IN_CONSULTATION']
    ).order_by('queue_number')
    return render(request, 'doctor/dashboard.html', {'patients': patients})

@login_required
def create_prescription(request, visit_id):
    """Handles saving the prescription"""
    visit = get_object_or_404(PatientVisit, id=visit_id)
    
    if request.method == 'POST':
        form = PrescriptionForm(request.POST)
        if form.is_valid():
            prescription = form.save(commit=False)
            prescription.prescribed_by = request.user
            prescription.consultation = visit.consultation
            prescription.save()
            
            # Update queue status
            visit.status = 'PRESCRIPTION_READY'
            visit.save()
            return redirect('doctor:dashboard')
    else:
        form = PrescriptionForm()
        
    return render(request, 'doctor/prescription_form.html', {
        'form': form,
        'patient': visit.student,
        'queue_number': visit.queue_number
    })
