from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ConsultationForm

@login_required
def new_consultation(request):
    if request.method == 'POST':
        form = ConsultationForm(request.POST, request.FILES)
        if form.is_valid():
            consultation = form.save(commit=False)
            consultation.student = request.user  # auto-attach logged-in student
            consultation.save()
            messages.success(request, 'Success! Your consultation has been sent. You will get a notification when a doctor replies.')
            return redirect('consultation_success')
    else:
        form = ConsultationForm()

    return render(request, 'consultation/new_consultation.html', {'form': form})

@login_required
def consultation_success(request):
    return render(request, 'consultation/success.html')
