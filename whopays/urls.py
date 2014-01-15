"""
Urls for Whopays This Doctor
"""
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

from django.contrib import admin
admin.autodiscover()

import doctors
from whopays import views

urlpatterns = patterns(
    '',
    # Generic Website Tat
    url(r'^$', views.HomeView.as_view(), name='home'),
    url(r'^about/?$', views.AboutView.as_view(), name='about'),
    url(r'contact$', views.WPContactView.as_view(), name='contact'),
    url(r'contact-ta$', TemplateView.as_view(template_name='contact-ta.html'),
        name='contact-ta'),

    # Making declarations
    url(r'^declare/?$', doctors.views.EstablishIdentityView.as_view(), name='establish-identity'),
    url(r'^restablish-identity/(?P<pk>\d+)?$', doctors.views.ReEstablishIdentityView.as_view(),
        name='re-establish-identity'),
    url(r'^declare/pending?$', TemplateView.as_view(template_name='identity_pending.html'),
        name='identity-pending'),
    url(r'^re-establish/pending$', TemplateView.as_view(template_name='identity_pending.html'),
        name='re-establish-identity-pending'),

    url(r'^declare/(?P<key>[0-9a-z]+)$', doctors.views.DeclareView.as_view(), name='declare'),

    url(r'^declare/(?P<pk>\d+)/add/(?P<key>[0-9a-z]+)/?$', doctors.views.AddDeclarationView.as_view(), name='add'),

    # Register of conflicts of interest
    url(r'^doctor/(?P<pk>\d+)/?$', doctors.views.DoctorDetailView.as_view(), name='doctor-detail'),
    url(r'^doctor/(?P<pk>\d+)[.]json$', doctors.views.DoctorJSONView.as_view(), name='doctor-json'),
    url(r'^doctors/?$', doctors.views.DoctorListView.as_view(), name='doctor-list'),

    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += staticfiles_urlpatterns()
