"""
Views relating to the register.
"""
from django.http import HttpResponseRedirect
from django.views.generic import ListView, DetailView
from extra_views import CreateWithInlinesView, InlineFormSet, UpdateWithInlinesView
from extra_views import NamedFormsetsMixin

from doctors import models, forms

class DeclarationInline(InlineFormSet):
    model = models.Declaration
    form_class = forms.DeclarationForm
    max_num = 1
    def get_formset_kwargs(self):
        kw = super(DeclarationInline, self).get_formset_kwargs()
        kw['queryset'] = models.Declaration.objects.none()
        return kw


class PharmaBenefitInline(InlineFormSet):
    model = models.PharmaBenefit
    form_class = forms.BenefitForm
    can_delete = False
    extra = 3
    def get_formset_kwargs(self):
        kw = super(PharmaBenefitInline, self).get_formset_kwargs()
        kw['queryset'] = models.PharmaBenefit.objects.none()
        return kw


class OtherMedicalBenefitInline(InlineFormSet):
    model = models.OtherMedicalBenefit
    form_class = forms.BenefitForm
    can_delete = False
    def get_formset_kwargs(self):
        kw = super(OtherMedicalBenefitInline, self).get_formset_kwargs()
        kw['queryset'] = models.OtherMedicalBenefit.objects.none()
        return kw


class FeeBenefitInline(InlineFormSet):
    model = models.FeeBenefit
    form_class = forms.BenefitForm
    can_delete = False
    def get_formset_kwargs(self):
        kw = super(FeeBenefitInline, self).get_formset_kwargs()
        kw['queryset'] = models.FeeBenefit.objects.none()
        return kw


class GrantBenefitInline(InlineFormSet):
    model = models.GrantBenefit
    form_class = forms.BenefitForm
    can_delete = False
    def get_formset_kwargs(self):
        kw = super(GrantBenefitInline, self).get_formset_kwargs()
        kw['queryset'] = models.GrantBenefit.objects.none()
        return kw


class DeclareView(NamedFormsetsMixin, CreateWithInlinesView):
    """
    Declaring your interests
    """
    template_name = 'declare.html'
    model = models.Doctor
    inlines = [
        DeclarationInline,
        PharmaBenefitInline,
        OtherMedicalBenefitInline,
        FeeBenefitInline,
        GrantBenefitInline
        ]
    inlines_names = [
        'Declaration',
        'PharmaBenefits',
        'OtherMedicalBenefits',
        'FeeBenefits',
        'GrantBenefits'
        ]

    def forms_valid(self, form, inlines):
        """
        If the form and formsets are valid, save the associated models.
        """
        self.object = form.save()
        for formset in inlines:
            formset.save()
        for formset in inlines:
            if formset.model == models.Declaration:
                try:
                    self.declaration = formset.new_objects[0]
                    print self.declaration, self.declaration.pk
                except IndexError:
                    self.declaration = models.Declaration(doctor=self.object)
                    self.declaration.save()

        for formset in inlines:
            for benefit in formset.new_objects:
                print benefit
                benefit.declaration = self.declaration
                benefit.save()
                print benefit.declaration, self.declaration

        return HttpResponseRedirect(self.get_success_url())


class AddDeclarationView(NamedFormsetsMixin, UpdateWithInlinesView):
    """
    Declaring your interests
    """
    template_name = 'declare.html'
    model = models.Doctor
    inlines = [
         DeclarationInline,
         PharmaBenefitInline,
        OtherMedicalBenefitInline,
        FeeBenefitInline,
        GrantBenefitInline
         ]
    inlines_names = [
        'Declaration',
        'PharmaBenefits',
        'OtherMedicalBenefits',
        'FeeBenefits',
        'GrantBenefits'
        ]

    def forms_valid(self, form, inlines):
        """
        If the form and formsets are valid, save the associated models.
        """
        self.object = form.save()
        for formset in inlines:
            formset.save()
        for formset in inlines:
            if formset.model == models.Declaration:
                try:
                    self.declaration = formset.new_objects[0]
                    print self.declaration, self.declaration.pk
                except IndexError:
                    self.declaration = models.Declaration(doctor=self.object)
                    self.declaration.save()

        for formset in inlines:
            for benefit in formset.new_objects:
                print benefit
                benefit.declaration = self.declaration
                benefit.save()
                print benefit.declaration, self.declaration

        return HttpResponseRedirect(self.get_success_url())


class DoctorDetailView(DetailView):
    queryset = models.Doctor.objects.all()
    context_object_name = 'doctor'

class DoctorListView(ListView):
    context_object_name = 'doctors'
    queryset = models.Doctor.objects.all()
