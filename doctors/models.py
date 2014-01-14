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
        return u'{0} - {1}'.format(getattr(self, 'doctor', 'Declaration'),
                                           self.date_created)

class Benefit(models.Model):
    BAND_CHOICES = (
        (1, u'under \u00a3100'),
        (2, u'\u00a3100- \u00a31000'),
        (3, u'\u00a31000- \u00a32000'),
        (4, u'\u00a32000 - \u00a35000'),
        (5, u'\u00a35000 - \u00a310000'),
        (6, u'\u00a310000 - \u00a350 000'),
        (7, u'\u00a350000- \u00a3100000'),
        (8, u'\u00a3100000+')
    )

    class Meta:
        abstract = True

    doctor = models.ForeignKey(Doctor)
    declaration = models.ForeignKey(Declaration, blank=True, null=True)
    company = models.CharField(max_length=200)
    reason = models.CharField(max_length=200)
    band = models.IntegerField(choices=BAND_CHOICES)

class PharmaBenefit(Benefit): pass
class OtherMedicalBenefit(Benefit): pass
class FeeBenefit(Benefit): pass
class GrantBenefit(Benefit): pass
