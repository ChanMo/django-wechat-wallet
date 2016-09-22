from .models import Wallet, Log

class WalletApi(object):
    """
    wallet api for recharge, cost, etc
    """

    def __init__(self, member_id):
        """ Get wallet by member id """
        try:
            self.wallet = Wallet.objects.get(member_id=member_id)
        except Wallet.DoesNotExist:
            print("Wallet does not exist")
            self.wallet = None


    def balance(self):
        """ get balance """
        return self.wallet.balance


    def make_trade(self, money, description):
        """ Always change the wallet first, then create log """
        balance = self.wallet.balance
        change = balance + money
        if (change) > 0:
            self.wallet.balance = change
            self.wallet.save()
        else:
            print("Balance is not enough")
            return False

        log = Log.objects.create(
                wallet = self.wallet,
                money = money,
                description = description,
                )
        return True
