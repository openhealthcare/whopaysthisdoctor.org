"""
Views relating to the register.
"""
import datetime as dt
from functools import reduce
import operator

from django.conf import settings
from django.db import transaction
from django.db.models import Q
from django.urls import reverse_lazy, reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView, CreateView, UpdateView
from extra_views import CreateWithInlinesView, InlineFormSet, UpdateWithInlinesView
from extra_views import NamedFormsetsMixin
import json

from doctors import models, forms

class JsonResponse(HttpResponse):
    """
    JSON response
    """
    def __init__(self, content, mimetype='application/json', status=None, content_type=None):
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
        return {'gmc': self.doctor.gmc_number}

    def form_valid(self, form):
        form.create_declaration_link()
        return super(ReEstablishIdentityView, self).form_valid(form)


class DeclarationInline(InlineFormSet):
    model = models.Declaration
    form_class = forms.DeclarationForm
    factory_kwargs = {'max_num': 1}

    def get_formset_kwargs(self):
        kw = super(DeclarationInline, self).get_formset_kwargs()
        kw['queryset'] = models.Declaration.objects.none()
        return kw


class PharmaBenefitInline(InlineFormSet):
    model = models.PharmaBenefit
    form_class = forms.BenefitForm
    factory_kwargs = {'extra': 3, 'can_delete': False}

    def get_formset_kwargs(self):
        kw = super(PharmaBenefitInline, self).get_formset_kwargs()
        kw['queryset'] = models.PharmaBenefit.objects.none()
        return kw


class OtherMedicalBenefitInline(InlineFormSet):
    model = models.OtherMedicalBenefit
    form_class = forms.BenefitForm
    factory_kwargs = {'can_delete':False}
    def get_formset_kwargs(self):
        kw = super(OtherMedicalBenefitInline, self).get_formset_kwargs()
        kw['queryset'] = models.OtherMedicalBenefit.objects.none()
        return kw


class FeeBenefitInline(InlineFormSet):
    model = models.FeeBenefit
    form_class = forms.BenefitForm
    factory_kwargs = {'can_delete': False}
    def get_formset_kwargs(self):
        kw = super(FeeBenefitInline, self).get_formset_kwargs()
        kw['queryset'] = models.FeeBenefit.objects.none()
        return kw


class GrantBenefitInline(InlineFormSet):
    model = models.GrantBenefit
    form_class = forms.BenefitForm
    factory_kwargs = {'can_delete': False}
    def get_formset_kwargs(self):
        kw = super(GrantBenefitInline, self).get_formset_kwargs()
        kw['queryset'] = models.GrantBenefit.objects.none()
        return kw


class AbstractDeclarView():
    model = models.Doctor
    template_name = 'declare.html'
    fields = '__all__'

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
            if work_detail_form.is_populated():
                work_detail.declaration = detailed_declaration
                work_detail.save()

        self.link.delete()
        if not settings.SKIP_EMAIL_VERIFICATION:
            self.object.send_declaration_thanks()
        return HttpResponseRedirect(self.get_success_url())


class DeclareView(AbstractDeclarView, CreateView):
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

    def get_initial(self, *args, **kwargs):
        initial = super().get_initial(*args, **kwargs)
        initial["email"] = self.link.email
        return initial


class AddDeclarationView(AbstractDeclarView, UpdateView):
    def dispatch(self, *args, **kwargs):
        link = get_object_or_404(models.DeclarationLink, key=kwargs['key'])
        if link.expires < timezone.now():
            raise Http404
        self.link = link
        return super().dispatch(*args, **kwargs)


class DoctorDetailView(DetailView):
    model = models.Doctor
    context_object_name = 'doctor'

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        declarations = self.object.detaileddeclaration_set.order_by(
            "-for_year"
        )
        # python 3.7 dicts maintain order!
        ctx["declarations"] = {}
        for declaration in declarations:
            if declaration.for_year not in ctx["declarations"]:
                ctx["declarations"][declaration.for_year] = []

            ctx["declarations"][declaration.for_year].append(
                declaration
            )
        return ctx


class DoctorDetailArchivedView(DetailView):
    model = models.Doctor
    context_object_name = 'doctor'
    template_name = "doctors/doctor_detail_archived.html"


class DoctorJSONView(DetailView):
    queryset = models.Doctor.objects.all()

    def get(self, *args, **kw):
        return JsonResponse(self.get_object().to_dict())


class DoctorListView(ListView):
    template_name = 'doctors/doctor_list.html'
    context_object_name = 'doctors'

    # This is dynamic to avoid the date being process-start bounded.
    def get_queryset(self):
        an_hour_ago = dt.datetime.now()-dt.timedelta(hours=1)
        qs = models.Doctor.objects.filter(
            Q(detaileddeclaration__dt_created__lte=an_hour_ago) |
            Q(detaileddeclaration=None)
        )

        return qs.distinct().order_by(
            "-detaileddeclaration__dt_created", "-declaration__dt_created"
        )


class SearchView(ListView):
    model = models.DetailedDeclaration

    SEARCH_FIELDS = [
        "consultancy_details",
        "academic_details",
        "other_work_details",
        "financial_details",
        "spousal_details",
        "sponsored_details",
        "political_details",
        "doctor__name",
        "doctor__primary_employer",
        "doctor__gmc_number",
        "workdetails__institution"
    ]

    def get_queryset(self):
        query_term = self.request.GET.get('q', '')
        queryset = self.model.objects.all()
        q_objects = [
            Q(**{"{}__icontains".format(field): query_term})
            for field in self.SEARCH_FIELDS
        ]
        return queryset.filter(reduce(operator.or_, q_objects)).distinct()
