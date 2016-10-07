from django.test import TestCase
from wechat_member.models import Member
from .api import WalletApi

# Create your tests here.

class WalletApiTest(TestCase):

    def test_get_log_list(self):
        me, status = Member.objects.get_or_create(
                name='chen',
                avatar='null',
                city='luoyang',
                )
        #print(me)
        w = WalletApi(me.id)
        print("Your balance is: " + str(w.get_balance()))
        #self.assertIs(w.wallet.balance, True)
        return w

    def test_trade(self):
        w = self.test_get_log_list()
        print("init balance:" + str(w.get_balance()))
        w.make_trade(200, "test recharge 200")
        print("result balance:" + str(w.get_balance()))
        print(w.get_log_list())
