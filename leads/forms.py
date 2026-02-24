# leads/forms.py
from django import forms
from .models import Lead

class LeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'source': forms.TextInput(attrs={'class': 'form-control'}),
            'medium': forms.TextInput(attrs={'class': 'form-control'}),
            'campaign': forms.TextInput(attrs={'class': 'form-control'}),
            'assigned_to': forms.Select(attrs={'class': 'form-select'}),
            'remarks': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'roof_type': forms.TextInput(attrs={'class': 'form-control'}),
            'average_monthly_bill': forms.NumberInput(attrs={'class': 'form-control'}),
            'financing_preference': forms.TextInput(attrs={'class': 'form-control'}),
            'sanctioned_load': forms.TextInput(attrs={'class': 'form-control'}),
            'installation_type': forms.Select(attrs={'class': 'form-select'}),
            'profile_pic': forms.FileInput(attrs={'class': 'form-control'}),
            
            # ✅ Follow-up fields
            'follow_up_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'follow_up_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
        }