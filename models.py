from datetime import datetime
import time
from utils import generate_txn_id
from storage import save_accounts

class BankAccount:
    def __init__(self, name, pin, balance=0):
        self.name = name
        self.pin = pin
        self._balance = balance
        self.history = []
        self.attempts = 3
        self.locked = False
        self.lock_time = None

    def check_pin(self, pin):
        return self.pin == pin

    @property
    def balance(self):
        return self._balance

    def deposit(self, amount):
            if amount > 0:
                 self._balance += amount
                 txn_id = generate_txn_id()
                 time = datetime.now()

                 self.history.append(
                      f"[{txn_id}] + {amount} | Deposit | {time}"
                 )
                 print(f"⬇️💵 Deposited: {amount}")
                 save_accounts()
            else:
                 print("❌ Invalid amount")
           
    def withdraw(self, amount):
        if amount > self._balance:
            print("⚠️ Insufficient balance")
        elif amount <= 0:
            print("❌ Invalid amount")
        else:
            self._balance -= amount
            txn_id = generate_txn_id()
            time = datetime.now()

            self.history.append(
                 f"[{txn_id}] -{amount} | Withdraw | {time}"
            )
          
            print(f"⬆️💵 Withdrawn: {amount}")
            save_accounts()    

    def show_history(self):
        print("\n📜 Transaction History:")
        if not self.history:
             print("❌ No transactions yet.")
             return
        
        for h in self.history:
             print("🧾", h)

    def transfer(self, other_user, amount):
         if amount <= 0:
              print("❌ Invalid amount")
              return
         if amount > self._balance:
              print("⚠️ Insufficient balance")
              return
         if other_user == self:
              print("🚫 You Cannot transfer to yourself")
              return
         
         self._balance -= amount
         other_user._balance += amount

         txn_id = generate_txn_id()
         time = datetime.now()

         self.history.append(
              f"[{txn_id}] -{amount} | Transfer to {other_user.name} | {time}"
         )

         other_user.history.append(
              f"[{txn_id}] +{amount} | Transfer from {self.name} | {time}"
         )

         print(f"Transferred {amount} to {other_user.name}")

         save_accounts()

    def show_history(self):
        print("\n📜 Transaction History:")
        if not self.history:
             print("❌ No transactions yet.")
             return
        
        for h in self.history:
             print("🧾", h)