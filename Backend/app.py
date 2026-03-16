import random
import json
import time
import threading
import os
from collections import deque
import csv
from queue import Queue
from flask import Flask, request, jsonify, render_template, session

app = Flask(__name__, template_folder='templates')
app.secret_key = "super_secret_trading_key"

# --- FOLDER SETUP ---
os.makedirs("transaction", exist_ok=True)
os.makedirs("records", exist_ok=True)

active_simulators = {}

class TradingSimulator:
    def __init__(self, username, password="", city="Unknown"):
        self.username = username
        self.password = password
        self.city = city
        self.balance = 0 
        self.portfolio = {"Stocks": {}, "Cryptos": {}}
        self.transaction_history = deque(maxlen=100)
        self.asset_prices = {
            "Stocks": {
                "NIFTY": 18000, "Reliance": 2500, "HDFC Bank": 1500, "PNB": 80,
                "TCS": 3200, "Infosys": 1400, "SBI": 500, "ICICI Bank": 900,
                "Bajaj Finance": 7000, "Wipro": 400, "HUL": 2400, "ITC": 200,
                "Axis Bank": 750, "LT": 1500, "Amazon": 3200, "Google": 2700,
                "InfraTel": 250
            },
            "Cryptos": {
                "Bitcoin": 3800000, "Ethereum": 225000, 
                "Dogecoin": 10, "Binance Coin": 25000
            }
        }
        self.price_history = {cat: {asset: deque(maxlen=50) for asset in assets} 
                            for cat, assets in self.asset_prices.items()}
        self.running = True
        self.log_queue = Queue()
        
        self.csv_path = os.path.join("transaction", "transactions.csv")
        self.json_path = os.path.join("records", f"{self.username}_data.json")
        
        self.init_data()
        self.start_threads()
        self.log_transaction("Login", "System", "Session", 0)

    def init_data(self):
        self.load_user_data()
        self.init_csv()

    def init_csv(self):
        try:
            with open(self.csv_path, 'a+') as f:
                if f.tell() == 0:
                    csv.writer(f).writerow([
                        "Timestamp", "Username", "Type", "Category", 
                        "Asset", "Amount", "Price", "Balance"
                    ])
        except Exception as e:
            print(f"CSV init error: {e}")

    def start_threads(self):
        threading.Thread(target=self.simulate_market, daemon=True).start()
        threading.Thread(target=self.log_worker, daemon=True).start()

    def log_worker(self):
        while self.running:
            batch = []
            while not self.log_queue.empty():
                batch.append(self.log_queue.get())
            if batch:
                try:
                    with open(self.csv_path, 'a', newline='') as f:
                        csv.writer(f).writerows(batch)
                except Exception as e:
                    print(f"Logging error: {e}")
            time.sleep(1)

    def load_user_data(self):
        try:
            with open(self.json_path, "r") as f:
                data = json.load(f)
                self.password = data.get("password", self.password)
                self.city = data.get("city", self.city)
                
                self.balance = data.get("balance", 0) 
                self.portfolio = {"Stocks": {}, "Cryptos": {}}
                loaded_portfolio = data.get("portfolio", {})
                for cat in ["Stocks", "Cryptos"]:
                    if isinstance(loaded_portfolio.get(cat, {}), dict):
                        self.portfolio[cat] = {
                            k: v for k, v in loaded_portfolio[cat].items()
                            if isinstance(v, (int, float))
                        }
                self.transaction_history = deque(
                    data.get("transaction_history", []), 
                    maxlen=100
                )
        except FileNotFoundError:
            pass
        except Exception as e:
            print(f"Load error: {e}")
            self.reset_to_defaults()

    def reset_to_defaults(self):
        self.balance = 0
        self.portfolio = {"Stocks": {}, "Cryptos": {}}
        self.transaction_history = deque(maxlen=100)

    def save_user_data(self):
        data = {
            "password": self.password,
            "city": self.city,
            "balance": self.balance,
            "portfolio": self.portfolio,
            "transaction_history": list(self.transaction_history)
        }
        try:
            with open(self.json_path, "w") as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Save error: {e}")

    def simulate_market(self):
        while self.running:
            self.update_prices()
            time.sleep(5)

    def update_prices(self):
        for cat in self.asset_prices:
            for asset in self.asset_prices[cat]:
                new_price = self.asset_prices[cat][asset] * random.uniform(0.95, 1.05)
                self.asset_prices[cat][asset] = round(max(new_price, 0.01), 2)
                self.price_history[cat][asset].append(self.asset_prices[cat][asset])

    def deposit_funds(self, amount):
        if amount <= 0: return "Invalid deposit amount"
        self.balance += amount
        self.log_transaction("Deposit", "Banking", "Cash", amount)
        self.transaction_history.append(f"Deposited ₹{amount:,.2f}")
        self.save_user_data()
        return None

    def withdraw_funds(self, amount):
        if amount <= 0: return "Invalid withdrawal amount"
        if amount > self.balance: return "Insufficient funds for withdrawal"
        self.balance -= amount
        self.log_transaction("Withdrawal", "Banking", "Cash", amount)
        self.transaction_history.append(f"Withdrew ₹{amount:,.2f}")
        self.save_user_data()
        return None

    def log_transaction(self, transaction_type, category, asset, amount, price=1.0):
        log_entry = [
            time.strftime("%Y-%m-%d %H:%M:%S"), self.username, transaction_type,
            category, asset, amount, price, self.balance
        ]
        self.log_queue.put(log_entry)

    def execute_trade(self, category, asset, amount, action):
        price = self.asset_prices[category][asset]
        total = price * amount
        
        if action == "buy":
            if total > self.balance: return "Insufficient funds"
            self.balance -= total
            self.portfolio[category][asset] = self.portfolio[category].get(asset, 0) + amount
        elif action == "sell":
            if self.portfolio[category].get(asset, 0) < amount: return "Insufficient assets"
            self.balance += total
            self.portfolio[category][asset] -= amount
            if self.portfolio[category][asset] == 0: del self.portfolio[category][asset]
        
        self.log_transaction(action.capitalize(), category, asset, amount, price)
        self.transaction_history.append(f"{action.capitalize()} {amount} {asset} @ ₹{price:,.2f}")
        self.save_user_data()
        
        # --- NEW REPORTING LINE ---
        print(f"REPORT: User {self.username} just {action}ed {amount} of {asset} at ₹{price}")
        
        return None

    def logout(self):
        self.log_transaction("Logout", "System", "Session", 0)
        self.running = False
        self.save_user_data() 
        time.sleep(0.5)
        batch = []
        while not self.log_queue.empty():
            batch.append(self.log_queue.get())
        if batch:
            try:
                with open(self.csv_path, 'a', newline='') as f:
                    csv.writer(f).writerows(batch)
            except Exception: pass


# --- FLASK WEB ROUTES ---

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    city = data.get('city')

    if not username or not password or not city:
        return jsonify({"success": False, "message": "All fields are required"}), 400

    file_path = os.path.join("records", f"{username}_data.json")
    if os.path.exists(file_path):
        return jsonify({"success": False, "message": "Username already exists. Please login."}), 400

    session['username'] = username
    sim = TradingSimulator(username, password, city)
    sim.save_user_data() 
    active_simulators[username] = sim
    
    # --- NEW REPORTING LINE ---
    print(f"REPORT: NEW USER REGISTERED - {username} from {city}")
    
    return jsonify({"success": True})

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"success": False, "message": "Username and password required"}), 400

    file_path = os.path.join("records", f"{username}_data.json")
    if not os.path.exists(file_path):
        return jsonify({"success": False, "message": "User not found. Please register.", "error_code": "user_not_found"}), 404

    with open(file_path, "r") as f:
        user_data = json.load(f)
        if user_data.get("password") != password:
            return jsonify({"success": False, "message": "Incorrect password."}), 401

    session['username'] = username
    if username not in active_simulators:
        active_simulators[username] = TradingSimulator(username, password, user_data.get("city", "Unknown"))
        
    # --- NEW REPORTING LINE ---
    print(f"REPORT: User {username} from {user_data.get('city', 'Unknown')} logged in.")
        
    return jsonify({"success": True})

@app.route('/api/logout', methods=['POST'])
def logout():
    username = session.get('username')
    if username and username in active_simulators:
        active_simulators[username].logout() 
        del active_simulators[username]
    session.pop('username', None)
    return jsonify({"success": True})

@app.route('/api/data', methods=['GET'])
def get_data():
    username = session.get('username')
    if not username or username not in active_simulators:
        return jsonify({"loggedIn": False})
    
    sim = active_simulators[username]
    return jsonify({
        "loggedIn": True,
        "username": sim.username,
        "city": sim.city,
        "balance": sim.balance,
        "prices": sim.asset_prices,
        "portfolio": sim.portfolio,
        "history": {c: {a: list(sim.price_history[c][a]) for a in p} for c, p in sim.price_history.items()}
    })

@app.route('/api/banking', methods=['POST'])
def banking():
    username = session.get('username')
    if not username or username not in active_simulators: return jsonify({"success": False}), 401
    
    data = request.json
    error = active_simulators[username].deposit_funds(float(data.get('amount', 0))) if data.get('action') == 'deposit' else active_simulators[username].withdraw_funds(float(data.get('amount', 0)))
    if error: return jsonify({"success": False, "message": error}), 400
    return jsonify({"success": True})

@app.route('/api/trade', methods=['POST'])
def trade():
    username = session.get('username')
    if not username or username not in active_simulators: return jsonify({"success": False}), 401
    
    data = request.json
    error = active_simulators[username].execute_trade(data['category'], data['asset'], int(data['amount']), data['action'])
    if error: return jsonify({"success": False, "message": error}), 400
    return jsonify({"success": True})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)