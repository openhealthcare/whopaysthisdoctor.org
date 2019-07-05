"""
Views relating to the register.
"""
import datetime as dt
import json
import collections
from django.conf import settings
from django.db import transaction
from django.urls import reverse, reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import FormView, CreateView
from extra_views import (
    CreateWithInlinesView, InlineFormSetView, UpdateWithInlinesView
)
from extra_views import NamedFormsetsMixin

from . import models, forms


class JsonResponse(HttpResponse):
    """
    JSON response
    """
    def __init__(
        self,
        content,
        mimetype='application/json',
        status=None,
        content_type=None
    ):
        super(JsonResponse, self).__init__(
            content=json.dumps(content),
            mimetype=mimetype,
            status=status,
            content_type=content_type,
        )


class EstablishIdentityView(FormView):
    """
    View to establish the identity of a user so they can
    edit their public record.
    """
    template_name = 'establish_identity.html'
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
        print(self.doctor)
        return {'gmc': self.doctor.gmc_number}

    def form_valid(self, form):
        form.create_declaration_link()
        return super(ReEstablishIdentityView, self).form_valid(form)


class DeclarationInline(InlineFormSetView):
    inline_model = models.Declaration
    form_class = forms.DeclarationForm
    max_num = 1

    def get_formset_kwargs(self):
        kw = super(DeclarationInline, self).get_formset_kwargs()
        kw['queryset'] = models.Declaration.objects.none()
        return kw

class PharmaBenefitInline(InlineFormSetView):
    inline_model = models.PharmaBenefit
    form_class = forms.BenefitForm
    can_delete = False
    extra = 3

    def get_formset_kwargs(self):
        kw = super(PharmaBenefitInline, self).get_formset_kwargs()
        kw['queryset'] = models.PharmaBenefit.objects.none()
        return kw


class OtherMedicalBenefitInline(InlineFormSetView):
    inline_model = models.OtherMedicalBenefit
    form_class = forms.BenefitForm
    can_delete = False
    def get_formset_kwargs(self):
        kw = super(OtherMedicalBenefitInline, self).get_formset_kwargs()
        kw['queryset'] = models.OtherMedicalBenefit.objects.none()
        return kw


class FeeBenefitInline(InlineFormSetView):
    inline_model = models.FeeBenefit
    form_class = forms.BenefitForm
    can_delete = False
    def get_formset_kwargs(self):
        kw = super(FeeBenefitInline, self).get_formset_kwargs()
        kw['queryset'] = models.FeeBenefit.objects.none()
        return kw


class GrantBenefitInline(InlineFormSetView):
    inline_model = models.GrantBenefit
    form_class = forms.BenefitForm
    can_delete = False

    def get_formset_kwargs(self):
        kw = super(GrantBenefitInline, self).get_formset_kwargs()
        kw['queryset'] = models.GrantBenefit.objects.none()
        return kw


class DeclareView(CreateView):
    model = models.Doctor
    template_name = 'declare.html'
    fields = '__all__'

    def dispatch(self, *args, **kwargs):
        link = get_object_or_404(models.DeclarationLink, key=kwargs['key'])
        if link.expires < timezone.now():
            raise Http404
        doctor = models.Doctor.objects.filter(email=link.email).count()
        if doctor > 0:
            kwargs['pk'] = models.Doctor.objects.get(email=link.email).pk
            return redirect(reverse('add', kwargs=kwargs))
        self.link = link
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['detaileddeclarationinline'] = forms.DeclarationIdentityFormSet(
                self.request.POST
            )
        else:
            data['detaileddeclarationinline'] = forms.DeclarationIdentityFormSet()

        if self.request.POST:
            data['workdetailsinline'] = forms.WorkDetailsFormSet(
                self.request.POST
            )
        else:
            data['workdetailsinline'] = forms.WorkDetailsFormSet()

        return data

    def is_valid(self):
        form = self.get_form()
        if not form.is_valid():
            return False
        context = self.get_context_data()
        detailed_declaration = context['detaileddeclarationinline']
        work_details = context['workdetailsinline']
        if not detailed_declaration.is_valid():
            return False
        if not work_details.is_valid():
            return False
        return True

    @transaction.atomic
    def form_valid(self, form):
        context = self.get_context_data()
        detailed_declarations = context['detaileddeclarationinline']
        work_details = context['workdetailsinline']
        if not self.is_valid():
            return self.form_invalid(form)

        self.object = form.save()
        detailed_declaration_form = detailed_declarations[0]
        detailed_declaration = detailed_declaration_form.save(commit=False)
        detailed_declaration.doctor = self.object
        detailed_declaration.save()
        for work_detail_form in work_details:
            work_detail = work_detail_form.save(commit=False)
            work_detail.declaration = detailed_declaration
            work_detail.save()
        if not settings.DEBUG:
            self.link.delete()
            self.object.send_declaration_thanks()
        return HttpResponseRedirect(self.get_success_url())


# class DeclareView(NamedFormsetsMixin, CreateWithInlinesView):
#     """
#     Declaring your interests
#     """
#     template_name = 'declare.html'
#     model = models.Doctor
#     form_class = forms.DoctorForm

#     inlines = [
#         DetailedDeclarationInline,
#         # PharmaBenefitInline,
#         # OtherMedicalBenefitInline,
#         # FeeBenefitInline,
#         # GrantBenefitInline
#         ]
#     inlines_names = [
#         'DetailedDeclarationInline',
#         # 'PharmaBenefits',
#         # 'OtherMedicalBenefits',
#         # 'FeeBenefits',
#         # 'GrantBenefits'
#         ]

#     def dispatch(self, *args, **kwargs):
#         link = get_object_or_404(models.DeclarationLink, key=kwargs['key'])
#         if link.expires < timezone.now():
#             raise Http404
#         doctor = models.Doctor.objects.filter(email=link.email).count()
#         if doctor > 0:
#             kwargs['pk'] = models.Doctor.objects.get(email=link.email).pk
#             return redirect(reverse('add', kwargs=kwargs))
#         self.link = link
#         import ipdb; ipdb.set_trace()
#         return super().dispatch(*args, **kwargs)

#     def forms_valid(self, form, inlines):
#         """
#         If the form and formsets are valid, save the associated models.
#         """
#         self.object = form.save()
#         self.object.email = self.link.email
#         self.object.save()

#         for formset in inlines:
#             formset.save()

#         for formset in inlines:
#             if formset.model == models.Declaration:
#                 try:
#                     self.declaration = formset.new_objects[0]
#                     print(self.declaration, self.declaration.pk)
#                 except IndexError:
#                     self.declaration = models.Declaration(doctor=self.object)
#                     self.declaration.save()

#         for formset in inlines:
#             for benefit in formset.new_objects:
#                 print(benefit)
#                 benefit.declaration = self.declaration
#                 benefit.save()
#                 print(benefit.declaration, self.declaration)

#         self.link.delete()
#         self.object.send_declaration_thanks()
#         return HttpResponseRedirect(self.get_success_url())


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
                    print(self.declaration, self.declaration.pk)
                except IndexError:
                    self.declaration = models.Declaration(doctor=self.object)
                    self.declaration.save()

        for formset in inlines:
            for benefit in formset.new_objects:
                print(benefit)
                benefit.declaration = self.declaration
                benefit.save()
                print(benefit.declaration, self.declaration)

        self.link.delete()
        self.object.send_declaration_thanks()
        return HttpResponseRedirect(self.get_success_url())


class DoctorDetailView(DetailView):
    model = models.Doctor
    context_object_name = 'doctor'

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        declarations = collections.defaultdict(list)
        for declaration in self.object.detaileddeclaration_set.all():
            declarations[declaration.for_year].append(
                declarations
            )
        ctx["declarations"] = declarations
        return ctx


class DoctorJSONView(DetailView):
    queryset = models.Doctor.objects.all()

    def get(self, *args, **kw):
        return JsonResponse(self.get_object().to_dict())


class HomeView(TemplateView):
    """
    Homepage for Whopaysthisdoctor.
    """
    template_name='home.html'


class AboutView(TemplateView):
    """
    Aboutpage for Whopaysthisdoctor.
    """
    template_name='about.html'


class DoctorListView(ListView):
    template_name = 'doctors/doctor_list.html'
    context_object_name = 'doctors'

    # This is dynamic to avoid the date being process-start bounded.
    def get_queryset(self):

        return sorted(set(
            models.Doctor.objects.filter(
                declaration__dt_created__lte=dt.datetime.now()-dt.timedelta(hours=1)
                )
            ), reverse=True)

