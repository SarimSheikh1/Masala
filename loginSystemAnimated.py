from flask import Flask, render_template, request, jsonify, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import os
import json

app = Flask(__name__)

# Database file
DB_FILE = 'users.json'

def load_users():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
    return {}

def save_users(users):
    with open(DB_FILE, 'w') as f:
        json.dump(users, f)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    users = load_users()
    
    if not username or not password:
        return jsonify({'success': False, 'message': 'Please enter both username and password'})
    
    if username in users:
        if check_password_hash(users[username], password):
            return jsonify({'success': True, 'message': 'Login successful!'})
        else:
            return jsonify({'success': False, 'message': 'Incorrect password'})
    else:
        return jsonify({'success': False, 'message': 'Username not found'})

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    confirm_password = data.get('confirm_password')
    
    users = load_users()
    
    if not username or not password or not confirm_password:
        return jsonify({'success': False, 'message': 'Please fill in all fields'})
    
    if password != confirm_password:
        return jsonify({'success': False, 'message': 'Passwords do not match'})
    
    if username in users:
        return jsonify({'success': False, 'message': 'Username already exists'})
    
    # Hash the password before storing
    users[username] = generate_password_hash(password)
    save_users(users)
    
    return jsonify({'success': True, 'message': 'Registration successful! You can now login.'})

if __name__ == '__main__':
    app.run(debug=True)