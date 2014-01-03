"""
Views for Whopaysthisdoctor
"""
from django.core.urlresolvers import reverse_lazy
from django.views.generic import TemplateView
from letter.contrib.contact import ContactView

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


class WPContactView(ContactView):
    """
    Pointless form for people who don't like their email clients
    """
    success_url = reverse_lazy('contact-ta')
