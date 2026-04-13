from flask import Flask, render_template, redirect, request, session
from atm import Atm
from datetime import datetime
import time

app = Flask(__name__)
app.secret_key = 'trainingbasket'

obj = Atm()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods = ['GET', 'POST'])
def register_account():
    if request.method == 'POST':
        name = request.form['name']
        pin = request.form['pin']
        balance = request.form['balance']
        acc = obj.create_account(name, pin, balance)
        return render_template('account_created.html', account_no = acc)
    return render_template('create_account.html')


@app.route('/login', methods = ['GET', 'POST'])
def login_account():
    if request.method == 'POST':
        account_no = request.form['account_no']
        pin = request.form['pin']

        success, msg = obj.login(account_no, pin)

        if success:
            session['account'] = account_no
            return render_template('dashboard.html')
        else:
            return render_template('login_account.html', error = msg)
    return render_template('login_account.html')

@app.route('/logout')
def logout():
    session.pop('account', None)
    return redirect('/')

#----------------------User-Dashboard-----------------------#
@app.route('/dashboard')
def dashboard():
    if 'account' not in session:
        return redirect('/login')
    return render_template('dashboard.html')


#---------Balance---------#
@app.route('/check_balance')
def check_balance():
        if 'account' not in session:
            return redirect('/login')
        account_no = session['account']
        obj = Atm()
        balance = obj.users[account_no]['balance']
        return render_template('check_balance.html', balance = balance)

#---------------change pin-------------#
@app.route('/change_pin', methods = ["GET", 'POST'])
def change_pin():
    
    if request.method == 'POST':
        if 'account' not in session:
            return redirect('/login')
        account_no = session['account']
        old_pin = obj.hash_pin(request.form['old_pin'])
        new_pin = obj.hash_pin(request.form['new_pin'])
        if old_pin == obj.users[account_no]['pin']:
            obj.users[account_no]['pin'] = new_pin
            msg = "Pin changed Successfully"
        else:
            msg = "Wrong pin"

        return render_template('change_pin.html', msg = msg)
    return render_template('change_pin.html')

@app.route('/withdraw', methods = ['GET', 'POST'])
def withdraw_money():
    if request.method == 'POST':
        if 'account' not in session:
            return redirect('/login')
        
        account_no = session['account']
        try:
            amount = float(request.form['amount'])
        except:
            return render_template('withdraw.html', msg = 'Invalid Amount')
        
        #check withdraw limit
        if amount >= obj.users[account_no]['withdraw_limit']:
            return render_template("withdraw.html", msg=f"Withdraw limit exceeded. Max limit: {obj.users[account_no]['withdraw_limit']}")

        # Check sufficient balance
        if amount > float(obj.users[account_no]['balance']):
            return render_template('withdraw.html',
                                   msg="Insufficient balance")        

        #perform withdrawal
        obj.users[account_no]['balance'] = float(obj.users[account_no]['balance']) -  amount
        obj.users[account_no]['transactions'].append({
            'type': 'withdraw',
        'amount': amount,
        'timestamp': str(datetime.now())
        })
        obj.save_users()
        msg = f"Remaining Balance: {obj.users[account_no]['balance']}"
        return render_template('withdraw.html', msg = msg)
    
    return render_template('withdraw.html')


@app.route('/deposit', methods = ['GET', 'POST'])
def deposit_money():
    if request.method == 'POST':
        if 'account' not in session:
            return redirect('/login')

        account_no = session['account']
        try:
            amount = float(request.form['amount'])
        except:
            return render_template('deposit.html', msg = 'Invalid Amount')
        
        #check deposit limit
        if amount >= obj.users[account_no]['deposit_limit']:
            return render_template("deposit.html", msg=f"Deposit limit exceeded. Max limit: {obj.users[account_no]['deposit_limit']}")

        obj.users[account_no]['balance'] += float(amount)
        obj.users[account_no]['transactions'].append({
                'type': 'deposit',
            'amount': amount,
            'timestamp': str(datetime.now())
            })
        obj.save_users()
        msg = f"Current Balance: {obj.users[account_no]['balance']}"
        return render_template('withdraw.html', msg = msg)
    
    return render_template('withdraw.html')



if __name__ == '__main__':
    app.run(debug=True)