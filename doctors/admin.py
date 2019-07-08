"""
Admin config for Doctors app.
"""
from django.contrib import admin
from reversion.admin import VersionAdmin

from doctors import models

class PharmaBenefitInline(admin.StackedInline):
    model = models.PharmaBenefit

class OtherMedicalBenefitInline(admin.StackedInline):
    model = models.OtherMedicalBenefit

class FeeBenefitInline(admin.StackedInline):
    model = models.FeeBenefit

class GrantBenefitInline(admin.StackedInline):
    model = models.GrantBenefit

class DoctorAdmin(VersionAdmin):
    pass

class DeclarationAdmin(VersionAdmin):
    inlines = (PharmaBenefitInline, OtherMedicalBenefitInline,
               FeeBenefitInline, GrantBenefitInline)
    list_display = ['doctor', 'dt_created']
    search_fields = ['doctor__name']
    list_filter = ['doctor__name']

class DeclarationLinkAdmin(admin.ModelAdmin):
    search_fields = ['email']
    list_display = ['email', 'expires', 'key']

admin.site.register(models.Doctor, DoctorAdmin)
admin.site.register(models.Declaration, DeclarationAdmin)
admin.site.register(models.DeclarationLink, DeclarationLinkAdmin)
