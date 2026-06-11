import time
from storage import accounts, save_accounts
from utils import valid_pin

def unlock_check(user):
     if user.locked and user.lock_time is not None:
          if time.time() - user.lock_time > 300:
               user.locked = False
               user.attempts = 3
               user.lock_time = None
               save_accounts()
               print("🔓 Account has been unlocked")

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
