from django.contrib.auth.models import User
from django.forms import DateInput

from .models import Uav, Rental
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.utils import timezone


class UavForm(forms.ModelForm):
    class Meta:
        model = Uav
        fields = ('name', 'brand', 'category', 'model', 'year', 'weight', 'features', 'price', 'status', 'image',)


class RentalForm(forms.ModelForm):
    start_date = forms.DateTimeField(
        label='Start Date',
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'})
    )
    end_date = forms.DateTimeField(
        label='End Date',
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'})
    )

    class Meta:
        model = Rental
        fields = ('start_date', 'end_date')




