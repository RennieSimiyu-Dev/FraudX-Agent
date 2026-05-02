# ⚡ Quick Start - FraudX Agent

## 🚀 One-Click Deployment

Simply double-click this file:
```
deploy_local.bat
```

This will:
1. ✅ Check Python installation
2. ✅ Install dependencies (if needed)
3. ✅ Start Backend API (http://localhost:8001)
4. ✅ Start Frontend UI (http://localhost:8501)

## 🎯 Manual Deployment

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Start Backend
```bash
# Option A: Use script
start_backend.bat

# Option B: Manual
cd Backend
python main.py
```

### Step 3: Start Frontend (New Terminal)
```bash
# Option A: Use script
start_frontend.bat

# Option B: Manual
cd Frontend
streamlit run streamlit_app.py
```

## 🔗 Access URLs

- **Backend API**: http://localhost:8001
- **API Docs**: http://localhost:8001/docs
- **Frontend UI**: http://localhost:8501

## 🧪 Quick Test

Open http://localhost:8501 and try:

**Test Transaction:**
- Amount: 500
- Country: US
- Device: device_123
- Merchant: amazon

**Expected Result:** High risk score, flagged for analyst review

## 📚 Full Documentation

See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for detailed instructions.

---

**Current Status:** Dependencies are being installed. Once complete, run `deploy_local.bat`