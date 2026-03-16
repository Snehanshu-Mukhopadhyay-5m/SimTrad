# 📈 SImTrad - Real-Time Virtual Trading Simulator

SImTrad is a full-stack web application designed for users to practice trading stocks and cryptocurrencies in a risk-free environment. Using live-simulated data and high-fidelity charting, it provides an authentic experience of market volatility without the financial risk.

## 🚀 Key Features
* **Live Market Engine:** Real-time price fluctuations across multiple asset classes (Stocks & Cryptos) powered by Python threading.
* **Interactive Visualizations:** Dynamic, responsive line charts built with **Chart.js** to track asset performance.
* **Portfolio Management:** Securely track holdings, cash balance, and transaction history.
* **Dual-Sync Trading:** A "Mirrored UI" system where selecting an asset for trade instantly updates the market chart and vice-versa.
* **Persistent User Data:** Robust authentication and session management with local data persistence for banking and trades.

## 🛠️ Tech Stack
* **Backend:** Python (Flask)
* **Frontend:** HTML5, CSS3, JavaScript (ES6+)
* **UI Framework:** Bootstrap 5 (Responsive Fintech Design)
* **Charting:** Chart.js
* **Data Handling:** JSON (User Records) & CSV (Transaction Logging)

## 📂 Project Structure
```text
SImTrad/
├── Backend/
│   ├── app.py           # Core Flask application & Market Engine
│   ├── static/          # Images, Profile Photos, and CSS
│   ├── templates/       # HTML Screens (Landing, About, Dashboard)
│   ├── records/         # Secure User Authentication data
│   └── transaction/     # User-specific trading logs (CSV)
└── README.md
```


## ⚙️ Installation & Usage
Follow these steps to get a local copy of SImTrad up and running on your machine.

# 1. Prerequisites
Python 3.8+ installed on your system.

Git installed on your system.

# 2. Clone the Repository
Open your terminal or PowerShell and run:

```bash
git clone [https://github.com/Snehanshu-Mukhopadhyay-5m/SImTrad.git](https://github.com/Snehanshu-Mukhopadhyay-5m/SImTrad.git)
cd SImTrad
```
# 3. Set Up a Virtual Environment (Recommended)
This keeps your project dependencies isolated and clean.

PowerShell
## Create the environment
```bash
python -m venv .venv
```
## Activate it (Windows)
```bash
.venv\Scripts\activate
```

# Activate it (Mac/Linux)
```bash
source .venv/bin/activate
```

## 4. Install Dependencies
SImTrad runs on the Flask web framework.

```bash
pip install flask
```

## 5. Launch the Platform
Navigate to the Backend directory and start the server:

```bash
cd Backend
python app.py
```

## 6. Access the Dashboard
```bash
Once the server is running, open your web browser and go to:
http://127.0.0.1:5000
```


## 🔗 Live Demo
🚀 **Check out the app here:** [SimTrad Virtual Trading Simulation](https://simtrad.onrender.com)



👨‍💻 About the Developer
Snehanshu Mukhopadhyay B.Tech CSE (Artificial Intelligence & Machine Learning) | 4th Semester | Jaipur

I am a developer focused on building tools that merge data science with practical software engineering. My interests include AI/ML model development, Cloud Computing (GCP/Azure), and Business Intelligence. Beyond SImTrad, I've worked on Emotion Detection models using Flask and participated in Kaggle Machine Learning competitions.

License: MIT

**Connect:** [LinkedIn-Snehanshu](https://www.linkedin.com/in/snehanshu-mukhopadhyay-a2156a344/) | [LeetCode-Snehanshu](https://leetcode.com/u/Anshu_0561/) 