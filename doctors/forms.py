"""
Forms for Who Pays This Doctor
"""
from django import forms
from django.conf import settings
from django.forms import widgets
from django.forms.models import ModelForm, inlineformset_factory

from doctors.models import (
    DeclarationLink, Doctor, DetailedDeclaration, WorkDetails
)


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


def band_validation(name, cleaned_data):
    """
    The bands are the amount that a person has been paid for
    a type of service.

    If a person ticks for example consultancy
    then consultancy_band is required.
    """
    band_name = "{}_band".format(name)
    data = cleaned_data[band_name]
    if cleaned_data[name] and not data:
        print("RETURNING ERROR {}".format(name))
        raise forms.ValidationError("This is required")
    return data


class DetailedDeclarationForm(ModelForm):
    class Meta:
        model = DetailedDeclaration
        exclude = ['dt_created']

    def clean_consultancy_band(self):
        return band_validation("consultancy", self.cleaned_data)

    def clean_academic_band(self):
        return band_validation("academic", self.cleaned_data)

    def clean_other_work_band(self):
        return band_validation("other_work", self.cleaned_data)

    def clean_financial_band(self):
        return band_validation("financial", self.cleaned_data)

    def clean_spousal_band(self):
        return band_validation("spousal", self.cleaned_data)

    def clean_sponsored_band(self):
        return band_validation("sponsored", self.cleaned_data)

    def clean_political_band(self):
        return band_validation("political", self.cleaned_data)


class WorkDetailsForm(ModelForm):
    class Meta:
        model = WorkDetails
        exclude = ['dt_created']


class DeclarationIdentityForm(forms.Form):
    def create_declaration_link(self):
        """
        1. Create a declaration link for this user
        2. Send an email to this user with the declaration link
        3. Profit
        4. There is no step 4.
        """
        link, created = DeclarationLink.objects.get_or_create(
            email=self.cleaned_data['email']
        )
        if not created:
            link.new_key()
            if link.expired:
                link.expire_tomorrow()
        link.send()
        return link


DeclarationIdentityFormSet = inlineformset_factory(
    Doctor, DetailedDeclaration, form=DetailedDeclarationForm, extra=1
)

WorkDetailsFormSet = inlineformset_factory(
    DetailedDeclaration, WorkDetails, form=WorkDetailsForm, extra=1
)


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
