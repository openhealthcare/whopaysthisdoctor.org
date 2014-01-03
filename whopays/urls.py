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
    url(r'^$', views.HomeView.as_view(), name='home'),
    url(r'^about/?$', views.AboutView.as_view(), name='about'),
    url(r'contact$', views.WPContactView.as_view(), name='contact'),
    url(r'contact-ta$', TemplateView.as_view(template_name='contact-ta.html'),
        name='contact-ta'),
    url(r'^declare/?$', doctors.views.DeclareView.as_view(), name='declare'),
    url(r'^declare/(?P<pk>\d+)/?$', doctors.views.AddDeclarationView.as_view(), name='add'),
    url(r'^doctor/(?P<pk>\d+)/?$', doctors.views.DoctorDetailView.as_view(), name='doctor-detail'),
    url(r'^doctors/?$', doctors.views.DoctorListView.as_view(), name='doctor-list'),

    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += staticfiles_urlpatterns()
