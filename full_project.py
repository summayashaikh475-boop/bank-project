import json
from datetime import datetime


import uuid

def is_sequence(pin):
     for i in range(3):
          if int(pin[i]) + 1 != int(pin[i+1]):
               return False
     return True 

def valid_pin(pin):
     if not pin.isdigit() or len(pin) != 4:
          return False
     
     if pin == pin[0] * 4:
          return False
     
     is_asc = all(int(pin[i]) + 1 == int(pin[i+1]) for i in range(3))
     is_desc = all(int(pin[i])-1 == int(pin[i+1]) for i in range(3))

     if is_asc or is_desc:
          return False
     
     return True


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

    def to_dict(self):
         return{
              "name": self.name,
              "pin": self.pin,
              "balance": self._balance,
              "history": self.history,
              "attempts": self.attempts,
              "locked": self.locked,
              "lock_time": self.lock_time 
         }    

accounts = {}

def from_dict(data):
     acc = BankAccount(data["name"], data["pin"], data["balance"])
     acc.history = data.get("history", [])
     acc.attempts = data.get("attempts", 3)
     acc.locked = data.get("locked", False)
     acc.lock_time = data.get("lock_time", None)
     return acc

def save_accounts():
     data = {}
     for username, acc in accounts.items():
          data[username] = acc.to_dict()

     with open("accounts.json", "w") as f:
          json.dump(data, f)

def load_accounts():
     global accounts
     try:
          with open("accounts.json", "r") as f:
               content = f.read().strip()

               if content == "":
                    accounts = {}
                    return
               
               data = json.loads(content)  

               for username, acc_data in data.items():
                    accounts[username] = from_dict(acc_data)

     except (FileNotFoundError, json.JSONDecodeError):
          accounts = {}


def create_account():
     username = input("Username: ")
     if username in accounts:
          print("❌ Username already exists!")
          return
     
     name = input("Name: ")
     pin1 = input("PIN: ")
     pin2 = input("Confirm PIN: ")

     if pin1 != pin2:
          print("❌ PINs do not match!")
          return
     
     if not valid_pin(pin1):
          print("❌ Weak or Invalid PIN")
          return
     
     accounts[username] = BankAccount(name, pin1)
     save_accounts()
     print("🎉Account created successfully!")

import time 

def unlock_check(user):
     if user.locked and user.lock_time is not None:
          if time.time() - user.lock_time > 300:
               user.locked = False
               user.attempts = 3
               user.lock_time = None
               save_accounts()
               print("🔓 Account has been unlocked")

def generate_txn_id():
     return str(uuid.uuid4())[:8]               

def login():
     username = input("Enter username: ")

     if username not in accounts:
          print("❌ User not found")
          return None
     
     user = accounts[username]

     unlock_check(user)
     
     if user.locked:
          print("🔐 Account is temporarily locked. Try again later.")
          return None
     
     while user.attempts > 0:
          pin = input("Enter PIN: ")

          if not pin.isdigit() or len(pin) != 4:
               print("⚠️ PIN must be 4 digits")
               continue


          if user.check_pin(pin):
               print(f"👋✨ Welcome {user.name}")
               user.attempts = 3
               return user
          else:
               user.attempts -= 1
               print(f"❌ Wrong PIN. Attempts left: {user.attempts}")

               if user.attempts == 0:
                    user.locked = True
                    user.lock_time = time.time()
                    save_accounts()
                    print("🔐 Account locked due to too many failed attempts")
     return None                        
 
def atm(user):

     print("🏦 Welcome to Python Banking System")

     while True:
          print("\n-----🏧 ATM MENU-----")
          print("1. Check Balance")
          print("2. Deposit")
          print("3. Withdraw")
          print("4. Transaction History")
          print("5. Transfer Money")
          print("6. Log out")

          choice = input("Enter choice: ")

          if choice == "1":
               print(f"💰 Balance: {user.balance}")

          elif choice == "2":
               try:
                    amount = int(input("Enter amount: "))
                    user.deposit(amount)
               except ValueError:
                    print("❌ Invalid number")     

          elif choice == "3":
               try:
                    amount = int(input("Enter amount to withdraw: ")) 
                    user.withdraw(amount)
               except ValueError:
                    print("❌ Invalid number")     

          elif choice == "4":
               user.show_history()

          elif choice == "5":
               receiver_name = input("Enter receiver username: ")

               if receiver_name in accounts:
                    try:
                         amount = int(input("Enter amount: "))
                         user.transfer(accounts[receiver_name], amount)
                    except ValueError:
                         print("❌ Invalid number")     
               else:
                    print("❌ Receiver not found")     

          elif choice =="6":
               print("🚪🏃 Logging out.....") 
               break    
          
          else:
               print("❌ Invalid choice")
load_accounts()

while True: 
    print("\n 🏦 ---MAIN MENU---")
    print("\n1. Login")
    print("2. Create Account")
    print("3. Exit")  

    choice = input("Enter choice: ")

    if choice == "1":
        user = login()
        if user:
            atm(user) 
    elif choice == "2":
         create_account()

    elif choice == "3":
        print("🙏 Thank you for using ATM")  
        break

    else:
         print("❌ Invalid choice")
                                                 