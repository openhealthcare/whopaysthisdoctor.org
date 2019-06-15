"""
Models for Who Pays This Doctor.
"""
import datetime as dt
import hashlib
import random

from django.conf import settings
from django.core.urlresolvers import reverse, reverse_lazy
from django.db import models
from django.utils import timezone
import letter

POSTIE = letter.DjangoPostman()

class WPTDMessage(letter.Letter):
    Postie   = POSTIE
    From     = settings.DEFAULT_FROM_EMAIL


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

    def to_dict(self):
        return dict(
            name=self.name,
            gmc_number=self.gmc_number,
            job_title=self.job_title,
            primary_employer=self.primary_employer,
            employment_address=self.employment_address,
            declarations=[d.to_dict() for d in self.declaration_set.all()]
            )

    def send_declaration_thanks(self):
        """
        Send this doctor an Email thanking them for their declaration,
        Explaining that if this is their frist submission it will not
        turn up for 24 hours, and with a link.
        """
        class Message(WPTDMessage):
            To       = self.email
            Subject  = 'Who Pays This Doctor - Thanks for your declaration'
            Template = 'email/declaration_thanks'
            Context  = {
                'doctor'   : self,
                'settings' : settings,
                'register' : reverse('doctor-list')
                }

        Message.send()
        return


class Declaration(models.Model):
    doctor = models.ForeignKey(Doctor)
    interests = models.BooleanField(default=False)
    past_declarations = models.TextField(blank=True, null=True)
    other_declarations = models.TextField(blank=True, null=True)
    date_created = models.DateField(default=lambda: dt.date.today())
    dt_created = models.DateTimeField(default=lambda: dt.datetime.now())

    def __unicode__(self):
        return u'{0} - {1}'.format(getattr(self, 'doctor', 'Declaration'),
                                           self.date_created)

    def to_dict(self):
        return dict(
            date=self.date_created.strftime('%Y-%m-%dT%H:%M:%S'),
            past_declarations=self.past_declarations,
            other_declarations=self.other_declarations,
            benefits=dict(
                pharma=[b.to_dict() for b in self.pharmabenefit_set.all()],
                othermedical=[b.to_dict() for b in self.othermedicalbenefit_set.all()],
                fee=[b.to_dict() for b in self.feebenefit_set.all()],
                grant=[b.to_dict() for b in self.grantbenefit_set.all()]
                )
            )

    @property
    def nothing_to_declare(self):
        the_things = (self.pharmabenefit_set.count() == 0,
                      self.othermedicalbenefit_set.count() == 0,
                      self.feebenefit_set.count() == 0,
                      self.grantbenefit_set.count() == 0,
                      not self.past_declarations,
                      not self.other_declarations)
        return all(the_things)


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

    def to_dict(self):
        return dict(
            company=self.company,
            reason=self.reason,
            band=self.get_band_display()
            )

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

def in_two_weeks():
    now = dt.datetime.now()
    then = now + dt.timedelta(days=14)
    return then


class DeclarationLink(models.Model):
    email = models.EmailField(unique=True)
    expires = models.DateTimeField(default=in_two_weeks)
    key = models.CharField(max_length=64, unique=True, default=lambda: random_token()[:8])

    @property
    def expired(self):
        """
        Has this link expired already?
        """
        return self.expires < timezone.now()

    def expire_tomorrow(self):
        """
        Update the expires date to be tomorrow.
        """
        self.expires = in_one_day()
        self.save()

    def absolute_url(self):
        return 'http://{0}/declare/{1}'.format(settings.DEFAULT_DOMAIN, self.key)

    def send(self):
        """
        Send the link to this email.
        """
        class Message(WPTDMessage):
            To       = self.email
            Subject  = 'Who Pays This Doctor - Edit your public record'
            Template = 'email/edit_public_record'
            Context  = {
                'link'       : self,
                }

        Message.send()

    def new_key(self):
        self.key = random_token()[:8]
        self.save()
        return

class ImportedDoctorCompanyLink(models.Model):
    doctor = models.ForeignKey(Doctor)
    company = models.CharField(max_length=200)
    officer_link = models.URLField(max_length=300)
    company_link = models.URLField(max_length=300)