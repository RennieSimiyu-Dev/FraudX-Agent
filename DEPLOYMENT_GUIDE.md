# 🚀 Local Deployment Guide - FraudX Agent

## Quick Start

### Step 1: Install Dependencies (In Progress)
The dependencies are currently being installed. Wait for the installation to complete.

```bash
pip install -r requirements.txt
```

### Step 2: Start the Backend API

**Option A: Using the batch script (Windows)**
```bash
start_backend.bat
```

**Option B: Manual command**
```bash
cd Backend
python main.py
```

The API will be available at: **http://localhost:8001**

### Step 3: Start the Frontend UI (In a new terminal)

**Option A: Using the batch script (Windows)**
```bash
start_frontend.bat
```

**Option B: Manual command**
```bash
cd Frontend
streamlit run streamlit_app.py
```

The UI will open automatically in your browser at: **http://localhost:8501**

## 📋 System Requirements

- ✅ Python 3.14.4 (Detected)
- ✅ pip package manager
- ✅ Windows 11 OS

## 🔗 Access Points

Once both services are running:

- **Backend API**: http://localhost:8001
- **API Documentation (Swagger)**: http://localhost:8001/docs
- **API Documentation (ReDoc)**: http://localhost:8001/redoc
- **Frontend UI**: http://localhost:8501

## 🧪 Testing the Deployment

### Test 1: Health Check
```bash
curl http://localhost:8001/
```

Expected response:
```json
{
  "status": "healthy",
  "service": "FraudX Agent API",
  "version": "1.0.0"
}
```

### Test 2: Process a Transaction
```bash
curl -X POST http://localhost:8001/transaction ^
  -H "Content-Type: application/json" ^
  -d "{\"transaction\":{\"amount\":500,\"country\":\"US\",\"device\":\"device_123\",\"merchant\":\"amazon\"},\"profile\":{\"avg_amount\":100,\"countries\":[\"KE\"],\"devices\":[\"device_456\"],\"merchants\":[\"grocery\",\"fuel\"]}}"
```

### Test 3: Use the Frontend
1. Open http://localhost:8501 in your browser
2. Enter transaction details
3. Click "Run Fraud Check"
4. View the risk assessment results

## 🛠️ Troubleshooting

### Port Already in Use
If port 8001 or 8501 is already in use:

**Backend (port 8001):**
Edit `Backend/main.py` line 180:
```python
uvicorn.run(app, host="0.0.0.0", port=8002)  # Change to 8002
```

**Frontend (port 8501):**
```bash
streamlit run streamlit_app.py --server.port 8502
```

### Dependencies Installation Issues
If installation fails, try:
```bash
pip install --upgrade pip
pip install -r requirements.txt --no-cache-dir
```

### Module Not Found Errors
Ensure you're in the correct directory:
- Backend commands must be run from the `Backend/` directory
- Frontend commands must be run from the `Frontend/` directory

## 📦 Installed Dependencies

- fastapi==0.109.0 - Web framework for the API
- uvicorn[standard]==0.27.0 - ASGI server
- pydantic==2.5.3 - Data validation
- streamlit==1.31.0 - Frontend UI framework
- requests==2.31.0 - HTTP client
- pandas==2.2.0 - Data manipulation
- pytest==8.0.0 - Testing framework

## 🔄 Stopping the Services

To stop the services:
1. Press `Ctrl+C` in each terminal window
2. Or close the terminal windows

## 📝 Next Steps

After deployment:
1. ✅ Verify both services are running
2. ✅ Test the API endpoints
3. ✅ Explore the Streamlit UI
4. ✅ Review the API documentation at /docs
5. ✅ Run the test suite: `pytest Tests/test_agent.py -v`

## 🎯 Example Transactions to Test

### Low Risk (Should APPROVE)
```json
{
  "transaction": {
    "amount": 45,
    "country": "KE",
    "device": "device_1",
    "merchant": "grocery"
  },
  "profile": {
    "avg_amount": 40,
    "countries": ["KE"],
    "devices": ["device_1"],
    "merchants": ["grocery", "fuel"]
  }
}
```

### Medium Risk (Should VERIFY_USER)
```json
{
  "transaction": {
    "amount": 150,
    "country": "KE",
    "device": "device_1",
    "merchant": "electronics"
  },
  "profile": {
    "avg_amount": 40,
    "countries": ["KE"],
    "devices": ["device_1"],
    "merchants": ["grocery", "fuel"]
  }
}
```

### High Risk (Should ANALYST_QUEUE)
```json
{
  "transaction": {
    "amount": 500,
    "country": "US",
    "device": "device_999",
    "merchant": "unknown"
  },
  "profile": {
    "avg_amount": 40,
    "countries": ["KE"],
    "devices": ["device_1"],
    "merchants": ["grocery", "fuel"]
  }
}
```

---

**Need Help?** Check the main [README.md](README.md) for detailed documentation.