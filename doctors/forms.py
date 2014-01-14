"""
Forms for Who Pays This Doctor
"""
import datetime

from django import forms
from django.forms import widgets
from django.forms.models import ModelForm

from doctors.models import DeclarationLink, Doctor

class NHSEmailField(forms.EmailField):
    def validate(self, value):
        super(NHSEmailField, self).validate(value)
        suffixes = ['nhs.uk', 'ac.uk', 'doctors.org.uk', 'deadpansincerity.com', 'msmith.net']
        if not any(value.endswith(x) for x in suffixes):
            raise forms.ValidationError('Email must end in one of {0}'.format(', '.join(suffixes)))

class DoctorForm(ModelForm):
    class Meta:
        model = Doctor
        exclude = ['email']

class BenefitForm(ModelForm):
    class Meta:
        exclude = ['declaration']

class DeclarationForm(ModelForm):
    class Meta:
        exclude = ['date_created']

class DeclarationIdentityForm(forms.Form):
    def create_declaration_link(self):
        """
        1. Create a declaration link for this user
        2. Send an email to this user with the declaration link
        3. Profit
        4. There is no step 4.
        """
        link, created = DeclarationLink.objects.get_or_create(
            email=self.cleaned_data['email'])
        if not created:
            link.new_key()
        link.send()
        return


class IdentityForm(DeclarationIdentityForm):
    email = NHSEmailField()

class ReEstablishIdentityForm(DeclarationIdentityForm):
    email = NHSEmailField()
    gmc = forms.CharField(widget=widgets.HiddenInput())

    def clean(self):
        super(ReEstablishIdentityForm, self).clean()

        email, gmc = self.cleaned_data['email'], self.cleaned_data['gmc']
        doctor = Doctor.objects.get(gmc_number=gmc)
        if doctor.email != email:
            raise forms.ValidationError('A different email address was used to submit declarations for that doctor in the past')
        return self.cleaned_data
