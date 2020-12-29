from django.contrib import admin

from recycle.models import RecycleRequest


@admin.register(RecycleRequest)
class RecycleRequestAdmin(admin.ModelAdmin):
    pass