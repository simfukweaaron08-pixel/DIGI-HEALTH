from django import forms
from core.models import Prescription

class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = ['medication_name', 'dosage', 'frequency', 'duration_days']
        widgets = {
            'medication_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Paracetamol'}),
            'dosage': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 500mg'}),
            'frequency': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Twice daily'}),
            'duration_days': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 7'}),
        }