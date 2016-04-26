#!/usr/bin/python
# vim: set fileencoding=utf-8 :
from django.db import models
from wechat_member.models import Member as WxMember

class Rule(models.Model):
    money = models.DecimalField(max_digits=8, decimal_places=2,\
                                verbose_name='充值金额')
    present = models.DecimalField(max_digits=8, decimal_places=2,\
                                  default=0, verbose_name='赠送金额')
    is_show = models.BooleanField(default=True, verbose_name='是否使用')

    def __unicode__(self):
        return unicode(self.money)

    class Meta(object):
        verbose_name = '充值规则'
        verbose_name_plural = '充值规则'
        ordering = ['money']


class Wallet(models.Model):
    member = models.OneToOneField(WxMember, related_name='wallet',\
                                  verbose_name='微信会员')
    money = models.DecimalField(max_digits=8, decimal_places=2, default=0,\
                                verbose_name='余额')
    created = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    def __unicode__(self):
        return unicode(self.money)

    class Meta(object):
        verbose_name = '钱包'
        verbose_name_plural = '钱包'


class Log(models.Model):
    TYPE_CHOICES = (
        ('recharge', '充值'),
        ('cost', '消费'),
    )
    wallet = models.ForeignKey(Wallet, related_name='logs', verbose_name='钱包')
    type = models.CharField(max_length=100, choices=TYPE_CHOICES, verbose_name='类型')
    money = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='金额')
    description = models.CharField(max_length=200, verbose_name='描述')
    trade_num = models.CharField(max_length=100, blank=True, null=True, verbose_name='交易号')
    created = models.DateTimeField(auto_now_add=True, verbose_name='时间')

    def __unicode__(self):
        return self.type

    class Meta(object):
        verbose_name = '记录'
        verbose_name_plural = '记录'
        ordering = ['-created']
