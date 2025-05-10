from django import forms
from .models import QuoteRequest, BudgetRange

class QuoteRequestForm(forms.ModelForm):
    budget_range = forms.ModelChoiceField(
        queryset=BudgetRange.objects.all(),
        empty_label="Select Budget",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = QuoteRequest
        fields = ['name', 'email', 'phone', 'service_type', 'budget_range']
