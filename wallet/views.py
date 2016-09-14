from django.views.generic import TemplateView, ListView
from django.http import HttpResponse
from django.core.urlresolvers import reverse

from wechat_member.views import WxMemberView
from .models import Rule, Wallet, Log

class BaseView(WxMemberView):
    """
    wallet base view
    if no wallet, create it
    """
    def dispatch(self, request, *args, **kwargs):
        #super(WalletBase, self).dispatch(request, *args, **kwargs)
        try:
            self.wallet = Wallet.objects.get(member=self.wx_member)
        except AttritubeError:
            pass
        except Wallet.DoesNotExist:
            wallet = Wallet.objects.create(member=self.wx_member)
            self.wallet = wallet
        return super(BaseView, self).dispatch(request, *args, **kwargs)


class HomeView(BaseView, TemplateView):
    """
    Home view
    """
    template_name = 'wallet/index.html'
    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        context['recharge_rules'] = Rule.objects.filter(is_show=True)
        context['wallet'] = self.wallet
        return context


class LogListView(BaseView, ListView):
    """
    wallet log list view
    """
    model = Log
    def get_queryset(self, **kwargs):
        return Log.objects.filter(wallet=self.wallet)
