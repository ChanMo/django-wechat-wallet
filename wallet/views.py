from django.views.generic import ListView, DetailView
from wechat_member.views import WxMemberView
from .models import Wallet, Log

class BaseView(WxMemberView):
    """
    wallet base view
    if no wallet, create it
    """
    def dispatch(self, request, *args, **kwargs):
        #super(WalletBase, self).dispatch(request, *args, **kwargs)
        try:
            result = Wallet.objects.get_or_create(
                    member_id = request.session['wx_member_id']
                    )
            self.wallet = result[0]
        except KeyError:
            """ if wx member is not exist """
            pass
        return super(BaseView, self).dispatch(request, *args, **kwargs)


class HomeView(BaseView, DetailView):
    """
    home view of wallet
    """
    model = Wallet
    template_name = 'wallet/index.html'

    def get_object(self):
        return self.wallet


class LogListView(BaseView, ListView):
    """
    wallet log list view
    """
    model = Log
    template_name = 'wallet/logs.html'

    def get_queryset(self, **kwargs):
        return Log.objects.filter(wallet=self.wallet)
