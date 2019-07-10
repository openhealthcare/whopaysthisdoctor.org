"""
Forms for Who Pays This Doctor
"""
import datetime

from django import forms
from django.conf import settings
from django.forms import widgets
from django.forms.models import ModelForm, inlineformset_factory

from doctors.models import DeclarationLink, Doctor, DetailedDeclaration, WorkDetails

class NHSEmailField(forms.EmailField):
    def validate(self, value):
        super(NHSEmailField, self).validate(value)
        if not any(value.endswith(x) for x in settings.ALL_SUFFIXES):
            raise forms.ValidationError('Email must end in one of {0}'.format(', '.join(settings.NHS_EMAIL_SUFFIXES)))

class DoctorForm(ModelForm):
    class Meta:
        model = Doctor
        exclude = ['email']

class BenefitForm(ModelForm):
    class Meta:
        exclude = ['declaration']

class DeclarationForm(ModelForm):
    class Meta:
        exclude = ['date_created', 'dt_created']

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
            if link.expired:
                link.expire_tomorrow()
        link.send()
        return

class IdentityForm(DeclarationIdentityForm):
    email = NHSEmailField()

class ReEstablishIdentityForm(DeclarationIdentityForm):
    email = NHSEmailField()
    gmc = forms.CharField(widget=widgets.HiddenInput())


    def clean(self):
        super(ReEstablishIdentityForm, self).clean()
        email = self.cleaned_data.get("email")

        if email:
            gmc = self.cleaned_data['gmc']
            doctor = Doctor.objects.get(gmc_number=gmc)
            if doctor.email != email:
                raise forms.ValidationError('A different email address was used to submit declarations for that doctor in the past')
        return self.cleaned_data


class DetailedDeclarationForm(ModelForm):
    for_year = forms.ChoiceField(label="Declaration period")

    def __init__(self, *a, **k):
        super().__init__(*a, **k)
        year_choices =  [
            (str(i), str(i)) for i in
            range(2010, datetime.date.today().year+1)
        ]
        year_choices.reverse()
        self.fields['for_year'].choices = year_choices

    class Meta:
        model = DetailedDeclaration
        exclude = ['dt_created']


class WorkDetailsForm(ModelForm):
    class Meta:
        model = WorkDetails
        exclude = ['dt_created']

    def is_populated(self):
        fields = ["category", "institution", "job_title"]
        return any(self.cleaned_data.get(i) for i in fields)


DeclarationIdentityFormSet = inlineformset_factory(
    Doctor, DetailedDeclaration, form=DetailedDeclarationForm, extra=1
)

WorkDetailsFormSet = inlineformset_factory(
    DetailedDeclaration, WorkDetails, form=WorkDetailsForm, extra=1
)
