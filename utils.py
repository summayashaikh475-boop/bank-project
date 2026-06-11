import uuid

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

def generate_txn_id():
     return str(uuid.uuid4())[:8]   