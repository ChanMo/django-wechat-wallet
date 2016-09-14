from django.contrib import admin
from .models import Wallet, Log, Rule
from . import models

class RuleAdmin(admin.ModelAdmin):
    pass

class LogInline(admin.TabularInline):
    model = Log
    extra = 1

class WalletAdmin(admin.ModelAdmin):
    list_display = ('member', 'balance', 'created', 'updated')
    list_per_page = 12
    list_filter = ['created', 'updated']
    inlines = [LogInline]

admin.site.register(Rule, RuleAdmin)
admin.site.register(Wallet, WalletAdmin)
