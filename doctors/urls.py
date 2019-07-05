"""
Urls for Whopays This Doctor
"""
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path
from django.views.generic import TemplateView
from . import views

from django.contrib import admin
admin.autodiscover()

import doctors

urlpatterns = [
    # Generic Website Tat
    path('', views.HomeView.as_view(), name='home'),
    path('about', views.AboutView.as_view(), name='about'),
    path('contact-ta', TemplateView.as_view(template_name='contact-ta.html'),
        name='contact-ta'),

    # Making declarations
    path('declare', doctors.views.EstablishIdentityView.as_view(), name='establish-identity'),
    path('restablish-identity/<pk>', doctors.views.ReEstablishIdentityView.as_view(),
        name='re-establish-identity'),
    path('declare/pending', TemplateView.as_view(template_name='identity_pending.html'),
        name='identity-pending'),
    path('re-establish/pending', TemplateView.as_view(template_name='identity_pending.html'),
        name='re-establish-identity-pending'),

    path('declare/<slug:key>', doctors.views.DeclareView.as_view(), name='declare'),

    path('declare/<pk>/add/<slug:key>/', doctors.views.AddDeclarationView.as_view(), name='add'),

    # Register of conflicts of interest
    path('doctor/<pk>/', doctors.views.DoctorDetailView.as_view(), name='doctor-detail'),
    path('doctor/<pk>.json', doctors.views.DoctorJSONView.as_view(), name='doctor-json'),
    path('doctors/', doctors.views.DoctorListView.as_view(), name='doctor-list'),
]

urlpatterns += staticfiles_urlpatterns()
