import sys
from .models import Wallet, Log

class WalletApi(object):
    """
    wallet api for recharge, cost, etc
    """

    def __init__(self, member_id):
        """ Get wallet by member id """
        """ add a member id check function later """
        self.wallet,created = Wallet.objects.get_or_create(member_id=member_id)

    def get_balance(self):
        """ get balance """
        return self.wallet.balance

    def get_log_list(self):
        """ get log list """
        log_list = self.wallet.logs
        return log_list

    def get_log(self, pk):
        """ check before """
        pass


    def make_trade(self, money, description):
        """ Always change the wallet first, then create log """
        balance = self.wallet.balance
        if (balance + money) < 0:
            print("Balance is not enough")
            return False

        log = Log.objects.create(
                wallet = self.wallet,
                money = money,
                description = description,
                )
        return True
