import os
import json
import time
from datetime import datetime, date
import numpy as np
import hashlib

class Atm:
    def __init__(self):
        
        self.file_path = 'data/users.json'
        self.users = self.load_users()
# --------------------------------------------------

    def load_users(self):
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        if not os.path.exists(self.file_path) or os.path.getsize(self.file_path) == 0:
            with open(self.file_path, 'w') as f:
                json.dump({}, f, indent = 4)
            return {}
        with open(self.file_path, 'r') as f:
            return json.load(f)
    
    def save_users(self):
        with open(self.file_path, 'w') as f:
            json.dump(self.users, f, indent = 4)

    def start(self):
        while True:
            service = input('''
1. Create Account
2. Login
3. Exit
Choose the service.... ''')
            if service == '1':
                self.create_account()
            elif service == '2':
                self.login() # login into your account
                # pass
            elif service == '3':
                print("Thank you for being our customer")
                break
            else:
                print("Invalid service or service not available at this moment")
        
# ----------------------Creating Accounts----------------------------------------
    def create_account(self):
        
        account_no = str(np.random.randint(0, 999999, 1)[0])
        if account_no in self.users:
            print("Account already exists")
        else:
            self.users[account_no] = {
            'name' :  input("Enter your name: "),
            'pin' :  self.hash_pin(int(input("Enter your Pin: "))),
            'balance' : float(input("Enter your balance: ")),
            'transactions' : [],
            'transfer_transactions' : [],
            'failed_attempts' : 0,
            'is_locked' : False,
            'lock_time' : None,
            'withdraw_limit' : 20000,
            'deposit_limit' : 20000
            }
            self.save_users()
            print(f"Account created successfully {account_no}")
    
    def login(self):
        account_no = input("Enter your account")
        if account_no not in self.users:
            print("Account does not exists")
            return 
        
        user = self.users[account_no]
        if user['is_locked']:
            current_time = time.time()
            if current_time - user['lock_time'] <= 60:
                print("Account is temporarily locked, please try again later")
                return 
            else:
                user['failed_attempts'] = 0
                user['is_locked'] = False
                user['lock_time'] = None
            self.save_users()
                
        pin = self.hash_pin(int(input("Enter your PIN: ")))
        if user and pin == self.users[account_no]['pin']:
            user['failed_attempts'] = 0
            user['is_locked'] = False
            user['lock_time'] = None
            print()
            print(f"Welcome: {self.users[account_no]['name']}")
            self.save_users()
            self.start_menu(account_no)
        else:
            user['failed_attempts'] += 1
            print()
            print("LOGIN FAILED")
            if user['failed_attempts'] > 3:
                user['is_locked'] = True
                user['lock_time'] = time.time()
                print("Account locked for 60s")
        self.save_users()

    
    # def verify_pin(self, account_no, pin):
    #     if pin == self.users[account_no]['pin']:
    #         return "verify"
    #     else:
    #         return "wrong pin"

    def hash_pin(self, pin):
        HASH_pin = hashlib.sha256(str(pin).encode()).hexdigest()
        return HASH_pin
    
    def start_menu(self, account_no):
        while True:
            user_input = input('''
    1. CHECK BALANCE
    2. CHANGE PIN
    3. WITHDRAW MONEY
    4. DEPOSIT MONEY
    5. TRANSACTION HISTORY
    6. TRANSFER MONEY
    CHOOSE THE SERVICE PLEASE... ''')
            if user_input == '1':
                print()
                print(f"Balance: {self.users[account_no]['balance']}")
            
            elif user_input == '2':
                self.change_pin(account_no)
                
            elif user_input == '3':
                self.withdraw_money(account_no)
            
            elif user_input == '4':
                self.deposit_money(account_no)

            elif user_input == '5':
                self.transaction_history(account_no)
            
            elif user_input == '6':
                self.transfer_money(account_no)

            elif user_input == '7':
                self.transfer_transaction_history(account_no)
            
            elif user_input == '8':
                self.change_limit(account_no)

            else:
                print("Thank you for being our customer")
                break
    

    def change_pin(self, account_no):
        old_pin = int(input("Enter old pin: "))
        new_pin = int(input("Enter new pin: "))
        if account_no in self.users:

            if old_pin == self.users[account_no]['pin']:
                self.users[account_no]['pin'] = new_pin
                self.save_users()
                print("Pin changed successfully")
            else:
                print("Wrong Pin")
        else:
            print("Not logged in")

    def withdraw_money(self, account_no):
        amount = float(input("Enter the amount: "))
        if amount <= self.users[account_no]['balance']:
            if amount <= self.users[account_no]['withdraw_limit']:
                self.users[account_no]['balance'] -= amount
                self.users[account_no]['transactions'].append({
                    'type' : 'withdraw',
                    'amount' : amount,
                    'timestamp' : str(datetime.now())
                })
                self.save_users()
            else:
                print("Withdraw limit exceed")
        else:
            print("Insufficient Balance")
    
    def deposit_money(self, account_no):
        amount = float(input("Enter the amount: "))
        if amount <= self.users[account_no]['deposit_limit']:
            self.users[account_no]['balance'] += amount
            self.users[account_no]['transactions'].append({
                'type' : 'deposit',
                'amount' : amount,
                'timestamp' : str(datetime.now())
            })
            self.save_users()
        else:
            print("Deposit limit exceeds")
        
    def transaction_history(self, account_no):
        transactions = self.users[account_no]['transactions']

        for transaction in transactions:
            if transaction['type'] == 'withdraw':
                print(transaction)
            else:
                print(transaction)

    def transfer_money(self, account_no):
        receiver_account_no = input("enter the account no : ")
        if receiver_account_no in self.users:
            amount = float(input("Enter the amount: "))
            self.users[account_no]['balance'] -= amount
            self.users[receiver_account_no]['balance'] += amount
            self.users[account_no]['transfer_transactions'].append({
                'type' : 'send',
                'account_no' : receiver_account_no,
                'amount' : amount,
                'name'  : self.users[receiver_account_no]['name'],
                'timestamp' : str(datetime.now())
            })
            self.users[receiver_account_no]['transfer_transactions'].append({
                'type' : 'receive',
                'account_no' : account_no,
                'amount' : amount,
                'name'  : self.users[account_no]['name'],
                'timestamp' : str(datetime.now())
            })
            self.save_users()
        else:
            print("Please enter a valid account no")

    def transfer_transaction_history(self, account_no):
        transfer_transactions = self.users[account_no]['transfer_transactions']

        for transaction in transfer_transactions:
            if transaction['type'] == 'send':
                print(transaction)

    def change_limit(self, account_no):
        type_limit = input("Enter which limit you want to changes: (w/d)")
        limit_value = float(input("Enter the limit value: "))
        if type_limit == 'w':
            self.users[account_no]['withdraw_limit'] *= limit_value
            self.save_users()
            print("Your Withdraw limit changed")
        else:
            self.users[account_no]['deposit_limit'] *= limit_value
            print("Your Deposit Limit changed")
            self.save_users()

