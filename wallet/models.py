from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
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
    money = models.DecimalField(_('money'), max_digits=8, decimal_places=2)
    description = models.CharField(_('description'), max_length=200)
    created = models.DateTimeField(_('created'), auto_now_add=True)

    def __unicode__(self):
        return self.description

    def __str__(self):
        return self.description

    class Meta(object):
        verbose_name = _('log')
        verbose_name_plural = _('log')
        ordering = ['-created']
