from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.db import models
from wechat_member.models import Member

class Rule(models.Model):
    """
    Wallet recharge rules
    """
    money = models.DecimalField(_('money'), max_digits=8, decimal_places=2)
    present = models.DecimalField(_('present'), max_digits=8, \
            decimal_places=2, default=0)
    is_show = models.BooleanField(_('is show'), default=True)

    def __unicode__(self):
        return unicode(self.money)

    class Meta(object):
        verbose_name = _('recharge rules')
        verbose_name_plural = _('recharge rules')
        ordering = ['money']


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
        return unicode(self.money)

    class Meta(object):
        verbose_name = '钱包'
        verbose_name_plural = '钱包'


class Log(models.Model):
    """
    Wallet transaction log
    """
    TYPE_CHOICES = (
        ('recharge', _('recharge')),
        ('spend', _('spend')),
        ('cash', _('cash')),
    )
    wallet = models.ForeignKey(Wallet, related_name='logs',\
            verbose_name=_('wallet'))
    type = models.CharField(_('type'), max_length=100, choices=TYPE_CHOICES)
    money = models.DecimalField(_('money'), max_digits=8, decimal_places=2)
    description = models.CharField(_('description'), max_length=200)
    created = models.DateTimeField(_('created'), auto_now_add=True)

    def __unicode__(self):
        return self.get_type_display()

    class Meta(object):
        verbose_name = _('log')
        verbose_name_plural = _('log')
        ordering = ['-created']
