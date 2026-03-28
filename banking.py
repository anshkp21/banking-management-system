from flask import Blueprint, request, redirect, render_template, session, jsonify
from models import db, User, Transaction
from datetime import datetime

bank = Blueprint('bank', __name__)

def get_current_user():
    uid = session.get('user_id')
    return User.query.get(uid) if uid else None

@bank.route('/dashboard')
def dashboard():
    user = get_current_user()
    if not user:
        return redirect('/login')
    
    # Get last 5 transactions
    recent_txns = Transaction.query.filter_by(user_id=user.id)\
                .order_by(Transaction.timestamp.desc()).limit(5).all()
    
    return render_template('dashboard.html', balance=user.balance, transactions=recent_txns)

@bank.route('/deposit', methods=['POST'])
def deposit():
    user = get_current_user()
    amt = float(request.form['amount'])
    
    user.balance += amt
    
    # Record transaction
    txn = Transaction(user_id=user.id, type='deposit', amount=amt, description='Deposit')
    db.session.add(txn)
    
    db.session.commit()
    return redirect('/dashboard')

@bank.route('/withdraw', methods=['POST'])
def withdraw():
    user = get_current_user()
    amt = float(request.form['amount'])
    
    if user.balance >= amt:
        user.balance -= amt
        
        # Record transaction
        txn = Transaction(user_id=user.id, type='withdraw', amount=amt, description='Withdrawal')
        db.session.add(txn)
        db.session.commit()
    
    return redirect('/dashboard')

@bank.route('/balance')
def balance():
    user = get_current_user()
    return f"Your Balance: ₹{user.balance}"

@bank.route('/history')
def history():
    user = get_current_user()
    if not user:
        return redirect('/login')
    
    all_txns = Transaction.query.filter_by(user_id=user.id)\
               .order_by(Transaction.timestamp.desc()).all()
    
    return render_template('history.html', transactions=all_txns, balance=user.balance)
# 🔗 Simple API: Get balance as JSON
@bank.route('/api/balance')
def api_balance():
    user = get_current_user()
    if not user:
        return jsonify({"error": "Please login first"}), 401
    
    return jsonify({
        "username": user.username,
        "balance": user.balance,
        "currency": "INR"
    })