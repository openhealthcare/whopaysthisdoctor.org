"""
Models for Who Pays This Doctor.
"""
import datetime as dt

from django.core.urlresolvers import reverse
from django.db import models

class Doctor(models.Model):
    name = models.CharField(max_length=200)
    gmc_number = models.CharField(max_length=100, unique=True)
    job_title = models.CharField(max_length=200)
    primary_employer = models.CharField(max_length=200)
    employment_address = models.TextField()

    def __unicode__(self):
        return u'{0} - {1}'.format(self.name, self.gmc_number)

    def get_absolute_url(self):
        return reverse('doctor-detail', kwargs={'pk': self.pk})

class Declaration(models.Model):
    doctor = models.ForeignKey(Doctor)
    interests = models.BooleanField(default=False)
    past_declarations = models.TextField(blank=True, null=True)
    other_declarations = models.TextField(blank=True, null=True)
    date_created = models.DateField(default=lambda: dt.date.today())

    def __unicode__(self):
        return u'{0} - {1}'.format(self.doctor, self.date_created)

class Benefit(models.Model):
    class Meta:
        abstract = True

    doctor = models.ForeignKey(Doctor)
    declaration = models.ForeignKey(Declaration, blank=True, null=True)
    company = models.CharField(max_length=200)
    reason = models.CharField(max_length=200)
    amount = models.FloatField()

class PharmaBenefit(Benefit): pass
class OtherMedicalBenefit(Benefit): pass
class FeeBenefit(Benefit): pass
class GrantBenefit(Benefit): pass
