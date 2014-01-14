"""
Models for Who Pays This Doctor.
"""
import datetime as dt
import hashlib
import random

from django.conf import settings
from django.core.urlresolvers import reverse, reverse_lazy
from django.db import models
import letter

POSTIE = letter.DjangoPostman()

class Doctor(models.Model):
    name = models.CharField(max_length=200)
    gmc_number = models.CharField(max_length=100, unique=True)
    job_title = models.CharField(max_length=200)
    primary_employer = models.CharField(max_length=200)
    employment_address = models.TextField()
    email = models.EmailField(blank=True, null=True)

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

def random_token(extra=None, hash_func=hashlib.sha256):
    if extra is None:
        extra = []
    bits = extra + [str(random.SystemRandom().getrandbits(512))]
    return hash_func("".join(bits).encode('utf-8')).hexdigest()

def in_one_day():
    now = dt.datetime.now()
    then = now + dt.timedelta(days=1)
    return then

class DeclarationLink(models.Model):
    email = models.EmailField(unique=True)
    expires = models.DateTimeField(default=in_one_day)
    key = models.CharField(max_length=64, unique=True, default=lambda: random_token())

    def absolute_url(self):
        return 'http://{0}/declare/{1}'.format(settings.DEFAULT_DOMAIN, self.key)

    def send(self):
        """
        Send the link to this email.
        """
        class Message(letter.Letter):
            Postie   = POSTIE

            From     = settings.DEFAULT_FROM_EMAIL
            To       = self.email
            Subject  = 'Who Pays This Doctor - Edit your public record'
            Template = 'email/edit_public_record'
            Context  = {
                'link'       : self,
                }

        Message.send()

    def new_key(self):
        self.key = random_token()
        self.save()
        return
