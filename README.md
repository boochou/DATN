# Project Setup Instructions

> **Note:** These steps must be run on **Ubuntu** (except for the Frontend part).

---

## 🖥️ CLI UI Setup

### 1. Run setup script
```bash
./setup.sh
```

### 2. Navigate to the logic directory
```bash
cd CLI
```
### 3. Install the Python package in editable mode
```bash
pip install -e .
```

### 4. Run the tool
```bash
acktool
```

## 🌐 Web UI Setup
### 🔧 Backend (Server)
1. Run the setup script (Run these commands outside of any virtual environment at first):
```bash
./setup.sh
```

2. Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```
3. Install backend dependencies:
```bash
pip3 install flask flask_cors knock-subdomains
```

4. Navigate to the logic directory and start the server:
```bash
cd logic
python3 server.py
```
### 💻 Frontend (FE)
1. Open a new terminal window.

2. Navigate to the FE directory:
```bash
cd FE
```

3. Install dependencies and start the frontend:
```bash
npm install
npm start
```
