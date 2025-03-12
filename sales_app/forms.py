from django import forms
from .models import Sale, Employee, Product

class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ['employee', 'product', 'quantity', 'date']
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'})
        }