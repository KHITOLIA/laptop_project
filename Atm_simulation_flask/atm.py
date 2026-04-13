import os
import json
import hashlib
import numpy as np
import time

class Atm:
    
    def __init__(self):
        self.file_path = 'data/users.json'
        self.users = self.load_users()

    def load_users(self):

        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        if not os.path.exists(self.file_path)  or os.path.getsize(self.file_path) == 0:
            with open(self.file_path, 'w') as f:
                json.dump({}, f, indent=4)
            return {}
        with open(self.file_path, 'r') as f:
            return json.load(f)
    
    def save_users(self) -> None:
        with open(self.file_path, 'w') as f:
            json.dump(self.users, f, indent=4)

    def hash_pin(self, pin):
        return hashlib.sha256(str(pin).encode()).hexdigest()
    
    def create_account(self, name, pin, balance)-> None:
        account_no = np.random.randint(0, 9999999, 1)[0]
        account_no = str(account_no)

        if account_no not in self.users:
            self.users[account_no] = {
                'name' : name,
                'pin' : self.hash_pin(pin),
                'balance' : balance,
                'transactions' : [],
                'transfer_transactions' : [],
                'failed_attempts' : 0,
                'is_locked' : False,
                'lock_time' : None,
                'withdraw_limit' : 20000,
                'deposti_limit' : 20000,
                'transfer_limit' : 10000
            }
            self.save_users()
            return account_no
        else:
            print("Account already exist")

    
    def login(self, account_no, pin):

        if account_no not in self.users:
            return False, "Account does not exist"

        user = self.users[account_no]

        # Check if account is locked
        if user['is_locked']:
            current_time = time.time()
            remaining = 60 - (current_time - user['lock_time'])

            if remaining > 0:
                return False, f"Account locked. Try again after {int(remaining)} seconds."
            else:
                # Unlock account after 60 sec
                user['failed_attempts'] = 0
                user['is_locked'] = False
                user['lock_time'] = None
                self.save_users()

        hashed_pin = self.hash_pin(pin)

        if hashed_pin == user['pin']:
            user['failed_attempts'] = 0
            self.save_users()
            return True, "Login successful"

        else:
            user['failed_attempts'] += 1

            if user['failed_attempts'] >= 3:
                user['is_locked'] = True
                user['lock_time'] = time.time()
                self.save_users()
                return False, "Account locked for 60 seconds due to multiple failed attempts."

            remaining_attempts = 3 - user['failed_attempts']
            self.save_users()
            return False, f"Incorrect PIN. {remaining_attempts} attempts remaining."