import time
from models import BankAccount
from storage import accounts, load_accounts, save_accounts
from utils import valid_pin, generate_txn_id, unlock_check


load_accounts()

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
    print("\n🏦 ---MAIN MENU---")
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
                                                 
