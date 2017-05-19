from __future__ import unicode_literals
from decimal import Decimal
import time
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from django.db import models
from wechat_member.models import Member

class Wallet(models.Model):
    """
    Wallet based on wechat member
    """
    member = models.OneToOneField(Member, related_name='wallet',\
            verbose_name=_('member'))
    balance = models.DecimalField(_('balance'), max_digits=8, \
            decimal_places=2, default=0)
    created = models.DateTimeField(_('created'), auto_now_add=True)
    updated = models.DateTimeField(_('updated'), auto_now=True)

    def __unicode__(self):
        return self.member.name

    def __str__(self):
        return self.member.name

    def update_balance(self, money, description):
        Log.objects.create(
            wallet = self,
            description = description,
            money = money
        )
        self.balance += Decimal(money)
        self.save()
        return self.balance

    class Meta(object):
        verbose_name = _('wallet')
        verbose_name_plural = _('wallet')


class Log(models.Model):
    """
    Wallet transaction log
    """
    wallet = models.ForeignKey(Wallet, related_name='logs',\
            verbose_name=_('wallet'))
    money = models.DecimalField(_('money'), max_digits=8, decimal_places=2,\
            help_text=_('if is decrease, insert -"'))
    description = models.CharField(_('description'), max_length=200,\
            help_text=_('insert description text'))
    created = models.DateTimeField(_('created'), auto_now_add=True)

    def __unicode__(self):
        return self.description

    def __str__(self):
        return self.description

    #def clean_fields(self, exclude=None):
    #    if self.pk is None and self.wallet_id is not None \
    #            and self.money is not None:
    #        wallet = Wallet.objects.get(pk=self.wallet.id)
    #        result = wallet.balance + self.money
    #        if result < 0:
    #            raise ValidationError({
    #                'money':_("wallet balance is not enough")
    #                })


    #def save(self, *args, **kwargs):
    #    """while create new, change wallet"""
    #    if self.pk == None:
    #        wallet = Wallet.objects.get(pk=self.wallet.id)
    #        wallet.balance += self.money
    #        wallet.save()
    #        """ push wechat message """
    #        # data = {
    #        #     'touser': wallet.member.openid,
    #        #     'template_id': '0KR1CN5azLSdQUC3jjO73NzXeMWQnJBD_hVFn-fOVio',
    #        #     'url': reverse({'wallet':'index'}),
    #        #     'topcolor': '#fb5020',
    #        #     'data': {
    #        #         'first': {'value':'','color':'#ff0000'},
    #        #         'keyword1': {'value':time.strftime('%Y/%m/%d %H:%i'),
    #        #             'color':'#173177'},
    #        #         'keyword2': {'value':self.description,'color':'#173177'},
    #        #         'remark': {'value':'','color':'#173177'},
    #        #     }
    #        # }
    #        # push = Push()
    #        # push.push_message(data)

    #    super(Log, self).save(*args, **kwargs)

    class Meta(object):
        verbose_name = _('log')
        verbose_name_plural = _('log')
        ordering = ['-created']
