from django import forms
from .models import QuoteRequest

class QuoteRequestForm(forms.ModelForm):
    class Meta:
        model = QuoteRequest
        fields = ['name', 'email', 'phone', 'service_type']  # No 'budget_range'
