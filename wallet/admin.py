from django.contrib import admin
from .models import Wallet, Log
from . import models

class LogAdmin(admin.ModelAdmin):
    list_display = ('wallet', 'description', 'money', 'created')
    list_per_page = 12
    list_filter = ('created',)
    search_fields = ('description',)

class WalletAdmin(admin.ModelAdmin):
    list_display = ('member', 'balance', 'created', 'updated')
    list_per_page = 12
    list_filter = ('created', 'updated')
    readonly_fields = ('balance','member')

admin.site.register(Wallet, WalletAdmin)
admin.site.register(Log, LogAdmin)
