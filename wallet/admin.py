#!/usr/bin/python
# vim: set fileencoding=utf-8 :
from decimal import Decimal
from django.contrib import messages
from django.contrib import admin
from django.conf.urls import url
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Wallet, Log, Rule
from . import models

class RuleAdmin(admin.ModelAdmin):
    list_display = ('money', 'present', 'is_show')

class LogInline(admin.TabularInline):
    model = Log
    extra = 1
    #readonly_fields = ('type', 'money', 'description', 'trade_num', 'created')
    #can_delete = False

    # def has_add_permission(self, request):
    #     return False

class WalletAdmin(admin.ModelAdmin):
    list_display = ('member', 'money', 'created')
    #readonly_fields = ('member', 'money', 'created')
    inlines = [LogInline]

    # def has_add_permission(self, request):
    #     return False

    # def has_delete_permission(self, request, obj=None):
    #     return False

    # def get_urls(self):
    #     urls = super(WalletAdmin, self).get_urls()
    #     recharge_url = [
    #         url(r'^(?P<pk>[0-9]+)/recharge/$', self.recharge),
    #     ]
    #     return recharge_url + urls

    # def recharge(self, request, pk):
    #     wallet = Wallet.objects.get(pk=pk)
    #     if request.method == 'GET':
    #         return render(
    #             request,
    #             'admin/wallet/wallet/recharge.html',
    #             {'opts':Wallet._meta,'wallet':wallet,}
    #         )
    #     elif request.method == 'POST':
    #         money = request.POST['money']
    #         wallet.money += Decimal(money)
    #         wallet.save()
    #         log = Log(
    #             wallet = wallet,
    #             type = 'recharge',
    #             money = money,
    #             description = u'后台充值%s元' % money,
    #         )
    #         log.save()
    #         messages.add_message(request, messages.INFO, '充值成功!')
    #         return HttpResponseRedirect('/admin/wallet/wallet/' + pk)


admin.site.register(Wallet, WalletAdmin)
admin.site.register(Rule, RuleAdmin)
