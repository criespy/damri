from django.contrib import admin
from . import models

class PemeriksaanInLine(admin.TabularInline):
    model = models.Pemeriksaan

class PemeriksaanAdmin(admin.ModelAdmin):
    inlines = [
        PemeriksaanInLine,
    ]

admin.site.register(models.Pengemudi, PemeriksaanAdmin)
admin.site.register(models.Pemeriksaan)
