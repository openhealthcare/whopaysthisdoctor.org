"""
Admin config for Doctors app.
"""
from django.contrib import admin
import reversion

from doctors import models

class PharmaBenefitInline(admin.StackedInline):
    model = models.PharmaBenefit

class OtherMedicalBenefitInline(admin.StackedInline):
    model = models.OtherMedicalBenefit

class FeeBenefitInline(admin.StackedInline):
    model = models.FeeBenefit

class GrantBenefitInline(admin.StackedInline):
    model = models.GrantBenefit

class DoctorAdmin(reversion.VersionAdmin):
    pass

class DeclarationAdmin(reversion.VersionAdmin):
    inlines = (PharmaBenefitInline, OtherMedicalBenefitInline,
               FeeBenefitInline, GrantBenefitInline)

admin.site.register(models.Doctor, DoctorAdmin)
admin.site.register(models.Declaration, DeclarationAdmin)
