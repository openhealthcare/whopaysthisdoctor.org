"""
Views for Whopaysthisdoctor
"""
from django.urls import reverse_lazy
from django.views.generic import TemplateView

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
