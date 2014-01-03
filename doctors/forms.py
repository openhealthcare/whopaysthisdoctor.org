"""
Forms for Who Pays This Doctor
"""
import datetime

from django import forms
from django.forms.models import ModelForm

class BenefitForm(ModelForm):
    class Meta:
        exclude = ['declaration']

class DeclarationForm(ModelForm):
    class Meta:
        exclude = ['date_created']
