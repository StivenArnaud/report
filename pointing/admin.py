from django.contrib import admin

# Register your models here.

from pointing.models import Presence, PrecenceItem


@admin.register(Presence)
class PresenceAdmin(admin.ModelAdmin):
    list_display = ('user', 'month', 'created')


@admin.register(PrecenceItem)
class PrecenceItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'state', 'times', 'identifier')
