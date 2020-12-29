from django.contrib import admin

from config.models import SiteConfiguration


@admin.register(SiteConfiguration)
class ConfigAdmin(admin.ModelAdmin):
    pass
