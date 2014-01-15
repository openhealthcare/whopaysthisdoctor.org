"""
Views relating to the register.
"""
import datetime as dt

from django.core.urlresolvers import reverse_lazy, reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView
from extra_views import CreateWithInlinesView, InlineFormSet, UpdateWithInlinesView
from extra_views import NamedFormsetsMixin
import simplejson

from doctors import models, forms

class JsonResponse(HttpResponse):
    """
        JSON response
    """
    def __init__(self, content, mimetype='application/json', status=None, content_type=None):
        super(JsonResponse, self).__init__(
            content=simplejson.dumps(content),
            mimetype=mimetype,
            status=status,
            content_type=content_type,
        )

class EstablishIdentityView(FormView):
    """
    View to establish the identity of a user so they can
    edit their public record.
    """
    template_name='establish_identity.html'
    form_class = forms.IdentityForm
    success_url = '/declare/pending'

    def form_valid(self, form):
        form.create_declaration_link()
        return super(EstablishIdentityView, self).form_valid(form)

class ReEstablishIdentityView(FormView):
    """
    View to reestablish the identity of a user so they can
    edit their public record.
    """
    template_name='re_establish_identity.html'
    form_class = forms.ReEstablishIdentityForm
    success_url = reverse_lazy('re-establish-identity-pending')

    def dispatch(self, *args, **kwargs):
        self.doctor = get_object_or_404(models.Doctor, pk=kwargs['pk'])
        return super(ReEstablishIdentityView, self).dispatch(*args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(ReEstablishIdentityView, self).get_context_data(*args, **kwargs)
        context['doctor'] = self.doctor
        return context

    def get_initial(self):
        print self.doctor
        return {'gmc': self.doctor.gmc_number}

    def form_valid(self, form):
        form.create_declaration_link()
        return super(ReEstablishIdentityView, self).form_valid(form)


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
    form_class = forms.DoctorForm

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

    def dispatch(self, *args, **kwargs):
        link = get_object_or_404(models.DeclarationLink, key=kwargs['key'])
        if link.expires < timezone.now():
            raise Http404
        doctor = models.Doctor.objects.filter(email=link.email).count()
        if doctor > 0:
            kwargs['pk'] = models.Doctor.objects.get(email=link.email).pk
            return redirect(reverse('add', kwargs=kwargs))
        self.link = link
        return super(DeclareView, self).dispatch(*args, **kwargs)

    def forms_valid(self, form, inlines):
        """
        If the form and formsets are valid, save the associated models.
        """
        self.object = form.save()
        self.object.email = self.link.email
        self.object.save()

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

        self.link.delete()
        self.object.send_declaration_thanks()
        return HttpResponseRedirect(self.get_success_url())


class AddDeclarationView(NamedFormsetsMixin, UpdateWithInlinesView):
    """
    Declaring your interests
    """
    template_name = 'declare.html'
    model = models.Doctor
    form_class = forms.DoctorForm

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

    def dispatch(self, *args, **kwargs):
        link = get_object_or_404(models.DeclarationLink, key=kwargs['key'])
        if link.expires < timezone.now():
            raise Http404
        self.link = link
        return super(AddDeclarationView, self).dispatch(*args, **kwargs)

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

        self.link.delete()
        self.object.send_declaration_thanks()
        return HttpResponseRedirect(self.get_success_url())


class DoctorDetailView(DetailView):
    queryset = models.Doctor.objects.all()
    context_object_name = 'doctor'

class DoctorJSONView(DetailView):
    queryset = models.Doctor.objects.all()

    def get(self, *args, **kw):
        return JsonResponse(self.get_object().to_dict())

class DoctorListView(ListView):
    template_name = 'doctors/doctor_list.html'
    context_object_name = 'doctors'

    # This is dynamic to avoid the date being process-start bounded.
    def get_queryset(self):
        return set(
            models.Doctor.objects.filter(
                declaration__dt_created__lte=dt.datetime.now()-dt.timedelta(days=1)
                )
            )
