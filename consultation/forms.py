from django import forms
from .models import Consultation

class ConsultationForm(forms.ModelForm):
    class Meta:
        model  = Consultation
        fields = ['symptoms', 'duration', 'severity', 'taking_medications', 'medications_details', 'image', 'video']
        widgets = {
            'symptoms': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'e.g. I have been having a severe headache and dizziness since yesterday...',
            }),
            'duration': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. 2 days, since Monday, 1 week...',
            }),
            'severity': forms.RadioSelect(attrs={
                'class': 'severity-radio',
            }),
            'taking_medications': forms.RadioSelect(attrs={
                'class': 'form-check-input',
            }),
            'medications_details': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Please list the medications you are currently taking...',
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*',
            }),
            'video': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': 'video/*',
            }),
        }
        labels = {
            'symptoms': 'Please describe your symptoms',
            'duration': 'How long have you had these symptoms?',
            'severity': 'How bad is it?',
            'taking_medications': 'Are you currently taking any medications?',
            'medications_details': 'If yes, please list the medications',
            'image': 'Upload Image (optional)',
            'video': 'Upload Video (optional)',
        }