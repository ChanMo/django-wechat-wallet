from __future__ import unicode_literals
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

    def clean_fields(self, exclude=None):
        if self.pk is None and self.wallet_id is not None \
                and self.money is not None:
            wallet = Wallet.objects.get(pk=self.wallet.id)
            result = wallet.balance + self.money
            if result < 0:
                raise ValidationError({
                    'money':_("wallet balance is not enough")
                    })


    def save(self, *args, **kwargs):
        """while create new, change wallet"""
        if self.pk == None:
            wallet = Wallet.objects.get(pk=self.wallet.id)
            wallet.balance += self.money
            wallet.save()
        super(Log, self).save(*args, **kwargs)

    class Meta(object):
        verbose_name = _('log')
        verbose_name_plural = _('log')
        ordering = ['-created']
