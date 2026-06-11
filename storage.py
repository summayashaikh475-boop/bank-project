import json
from models import BankAccount

accounts = {}

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

def from_dict(data):
     acc = BankAccount(data["name"], data["pin"], data["balance"])
     acc.history = data.get("history", [])
     acc.attempts = data.get("attempts", 3)
     acc.locked = data.get("locked", False)
     acc.lock_time = data.get("lock_time", None)
     return acc
