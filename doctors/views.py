"""
Views relating to the register.
"""
import datetime as dt
import json
import operator
from functools import reduce
from django.db.models import Q
from django.conf import settings
from django.db import transaction
from django.urls import reverse, reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import FormView, CreateView, UpdateView

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
        link = form.create_declaration_link()
        if settings.SKIP_EMAIL_VERIFICATION:
            return HttpResponseRedirect(link.absolute_url())
        return super(EstablishIdentityView, self).form_valid(form)


class ReEstablishIdentityView(FormView):
    """
    View to reestablish the identity of a user so they can
    edit their public record.
    """
    template_name = 're_establish_identity.html'
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
        link = form.create_declaration_link()
        if settings.SKIP_EMAIL_VERIFICATION:
            return HttpResponseRedirect(link.absolute_url())
        return super(ReEstablishIdentityView, self).form_valid(form)


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


class HomeView(TemplateView):
    """
    Homepage for Whopaysthisdoctor.
    """
    template_name = 'home.html'


class AboutView(TemplateView):
    """
    Aboutpage for Whopaysthisdoctor.
    """
    template_name = 'about.html'


class DoctorListView(ListView):
    template_name = 'doctors/doctor_list.html'
    context_object_name = 'doctors'

    SEARCH_FIELDS = [
        "name",
        "gmc_number",
        "job_title",
        "primary_employer",
        "employment_address",
        "email",
        "detaileddeclaration__consultancy_details",
        "detaileddeclaration__academic_details",
        "detaileddeclaration__other_work_details",
        "detaileddeclaration__financial_details",
        "detaileddeclaration__spousal_details",
        "detaileddeclaration__sponsored_details",
        "detaileddeclaration__political_details",
        "detaileddeclaration__workdetails__position",
        "detaileddeclaration__workdetails__details",
        "declaration__past_declarations",
        "declaration__other_declarations",
        "declaration__pharmabenefit__company",
        "declaration__othermedicalbenefit__company",
        "declaration__feebenefit__company",
        "declaration__grantbenefit__company",
    ]

    def search(self, some_query):
        """
        splits a string by space and queries
        based on the search fields
        """
        query_values = some_query.split(" ")
        qs = models.Doctor.objects.all()
        for query_value in query_values:
            q_objects = []
            for field in self.SEARCH_FIELDS:
                model_field = "{}__icontains".format(field)
                q_objects.append(Q(**{model_field: query_value}))
            qs = qs.filter(reduce(operator.or_, q_objects))
        return qs

    # This is dynamic to avoid the date being process-start bounded.
    def get_queryset(self):
        query = self.request.GET.get("q")
        if query:
            qs = self.search(query)
        else:
            an_hour_ago = dt.datetime.now()-dt.timedelta(
                hours=1
            )
            qs = models.Doctor.objects.filter(
                Q(detaileddeclaration__dt_created__lte=an_hour_ago) |
                Q(detaileddeclaration=None)
            )

        return qs.distinct().order_by(
            "-detaileddeclaration__dt_created", "-declaration__dt_created"
        )

