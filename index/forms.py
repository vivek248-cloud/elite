from django import forms
from .models import QuoteRequest

class QuoteRequestForm(forms.ModelForm):
    class Meta:
        model = QuoteRequest
        fields = ['name', 'email', 'phone', 'service_type']  # No 'budget_range'

from django import forms

class CareerEmailForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    position = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)
    resume = forms.FileField()