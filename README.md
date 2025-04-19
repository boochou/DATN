# Project Setup Instructions

> **Note:** These steps must be run on **Ubuntu** (except for the Frontend part).

---

## 🖥️ CLI UI Setup

### 1. Run setup script
```bash
./setup.sh
```

### 2. Navigate to the logic directory
``` cd logic
```
### 3. Install the Python package in editable mode
``` pip install -e .
```

### 4. Run the tool
``` acktool
```

## 🌐 Web UI Setup
### 🔧 Backend (Server)
1. Run the setup script (Run these commands outside of any virtual environment at first):
```./setup.sh
```

2. Create and activate a virtual environment:
```python3 -m venv venv
source venv/bin/activate
```
3. Install backend dependencies:
```pip3 install flask flask_cors knock-subdomains
```

4. Navigate to the logic directory and start the server:
```
cd logic
python3 server.py
```
### 💻 Frontend (FE)
1. Open a new terminal window.

2. Navigate to the FE directory:
```cd FE
```

3. Install dependencies and start the frontend:
```npm install
npm start
```
