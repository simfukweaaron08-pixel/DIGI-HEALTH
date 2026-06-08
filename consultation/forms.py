from django import forms
from .models import Consultation

class ConsultationForm(forms.ModelForm):
    class Meta:
        model  = Consultation
        fields = ['symptoms', 'duration', 'severity', 'image', 'video']
        widgets = {
            'symptoms': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'e.g. I have been having a severe headache and dizziness since yesterday...',
            }),
            'duration': forms.Select(attrs={
                'class': 'form-select',
            }),
            'severity': forms.RadioSelect(attrs={
                'class': 'severity-radio',
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
            'image':    'Upload Image (optional)',
            'video':    'Upload Video (optional)',
        }
