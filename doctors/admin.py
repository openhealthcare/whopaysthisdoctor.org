from django.contrib import admin
from doctors import models

admin.site.register(models.Doctor)
admin.site.register(models.Declaration)
admin.site.register(models.PharmaBenefit)
admin.site.register(models.OtherMedicalBenefit)
admin.site.register(models.FeeBenefit)
admin.site.register(models.GrantBenefit)
admin.site.register(models.DeclarationLink)
admin.site.register(models.WorkDetails)
admin.site.register(models.DetailedDeclaration)



