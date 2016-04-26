#!/usr/bin/python
# vim: set fileencoding=utf-8 :
import time
import random
import xmltodict
from decimal import Decimal
from django.shortcuts import render, get_object_or_404
from django.views.generic.base import View, TemplateView
from django.http import HttpResponse
from django.views.generic import ListView
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse
from django.conf import settings

from wechat import api
from wechat_member.models import Member
from wechat_member.views import WxMemberView
from member_grade.api import GradeApi
from .models import Wallet, Log, Rule
from order.models import Order

class WalletBaseView(WxMemberView):
    def dispatch(self, request, *args, **kwargs):
        try:
            result = Wallet.objects.get_or_create(member_id=request.session['wx_member_id'])
            self.wallet = result[0]
            #Wallet.objects.get_or_create(member=self.wx_member)
        except AttributeError:
            pass
        return super(WalletBaseView, self).dispatch(request, *args, **kwargs)

class IndexView(WalletBaseView, TemplateView):
    template_name = 'wallet/index.html'
    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['wallet'] = self.wallet
        #context['wallet'] = Wallet.objects.get(member=self.wx_member)
        context['recharge_rules'] = Rule.objects.filter(is_show=True)
        return context


class Recharge(WalletBaseView, View):
    def get(self, request, *args, **kwargs):
        rule = Rule.objects.get(id=request.GET['rule_id'])
        total_fee = unicode(int(float(rule.money) * 100))
        param = {
            'xml': {
                'openid': self.wallet.member.openid,
                'body': settings.WECHAT_NAME,
                'out_trade_no': unicode(int(time.time())),
                'total_fee': total_fee,
                'spbill_create_ip': request.META['REMOTE_ADDR'],
                'notify_url': settings.WECHAT_HOST + reverse('wallet:recharge_notify')
            }
        }
        wx = api.Pay()
        wx.set_prepay_id(param)
        return render(request, 'wallet/pay.html', {'data':wx.get_pay_data()})


class Pay(WalletBaseView):
    def post(self, request, *args, **kwargs):
        code = request.POST['code']
        price = request.POST['price']
        description = request.POST['description']

        if float(self.wallet.money) < float(price):
            return HttpResponse('钱包余额不足')

        self.wallet.money = float(self.wallet.money) - float(price)
        self.wallet.save()

        log = Log(
            wallet = self.wallet,
            type = 'cost',
            money = price,
            description = description,
            trade_num = unicode(int(time.time())) + unicode(code),
        )
        log.save()

        order = Order.objects.get(id=code)
        order.is_pay = True
        order.pay_num = log.trade_num
        order.save()

        return render(request, 'wallet/success.html')


class LogList(WalletBaseView, ListView):
    model = Log
    def get_queryset(self, **kwargs):
        return Log.objects.filter(wallet=self.wallet)


# Recharge notify
class PayNotify(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(PayNotify, self).dispatch(request, *args, **kwargs)
    def post(self, request, *args, **kwargs):
        wx = api.Base()
        data = dict(xmltodict.parse(request.body)['xml'])
        result = {}
        try:
            member = Member.objects.get(openid=data['openid'])
            wallet = Wallet.objects.get(member=member)
            money = Decimal(data['total_fee'])/100
            exist_log = Log.objects.get(trade_num=data['transaction_id'])
            result['return_code'] = u'ERROR'
            result['return_msg'] = u'OK'
        except (Member.DoesNotExist, Wallet.DoesNotExist):
            result['return_code'] = u'ERROR'
            result['return_msg'] = u'OK'
        except Log.DoesNotExist:
            wallet.money = wallet.money + money
            wallet.save()

            log = Log(
                wallet = wallet,
                type = 'recharge',
                description = '微信充值',
                money = money,
                trade_num = data['transaction_id'],
            )
            log.save()

            # member grade log add
            grade = GradeApi(member.id)
            grade.add_log('increase', int(money*1), '钱包充值')

            result['return_code'] = u'SUCCESS'
            result['return_msg'] = u'OK'
        result_xml = wx.dict_to_xml(result)
        return HttpResponse(result_xml)
