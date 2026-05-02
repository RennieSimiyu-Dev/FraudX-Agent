# FraudX Agent 🛡️

A real-time fraud detection system that analyzes transactions and identifies suspicious activities using rule-based risk scoring.

## 🌟 Features

- **Real-time Fraud Detection**: Analyzes transactions instantly based on multiple risk factors
- **Risk Scoring**: Calculates fraud risk scores (0-100) with detailed reasoning
- **Automated Decision Making**: Routes transactions based on risk level
- **User Verification**: Requests user confirmation for medium-risk transactions
- **Analyst Queue**: Flags high-risk transactions for manual review
- **RESTful API**: FastAPI backend with comprehensive endpoints
- **Interactive UI**: Streamlit-based frontend for monitoring and testing

## 📋 Risk Factors

The system evaluates transactions based on:

1. **Transaction Amount**: Compares against user's average spending
   - 5x average: +40 points
   - 3x average: +30 points
   - 2x average: +20 points

2. **Geographic Location**: Detects transactions from new countries (+25 points)

3. **Device Recognition**: Identifies unknown devices (+20 points)

4. **Merchant Verification**: Flags new merchants (+15 points)

## 🎯 Decision Logic

| Risk Score | Action | Description |
|------------|--------|-------------|
| 0-29 | **APPROVE** | Low risk - Process automatically |
| 30-69 | **VERIFY_USER** | Medium risk - Request user confirmation |
| 70-100 | **ANALYST_QUEUE** | High risk - Manual review required |

## 🚀 Quick Start

### Prerequisites

- Python 3.10+ (✅ Python 3.14.4 detected)
- pip

### One-Click Deployment (Windows)

Simply double-click:
```
deploy_local.bat
```

This automatically:
1. Checks Python installation
2. Installs dependencies
3. Starts Backend API (http://localhost:8001)
4. Starts Frontend UI (http://localhost:8501)

### Manual Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd "FRAUDX AGENT"
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

### Running the Application

#### Option A: Use Deployment Scripts

**Start Backend:**
```bash
start_backend.bat
```

**Start Frontend (in new terminal):**
```bash
start_frontend.bat
```

#### Option B: Manual Commands

**Start Backend API:**
```bash
cd Backend
python main.py
```
The API will be available at `http://localhost:8001`

**Start Frontend (in new terminal):**
```bash
cd Frontend
streamlit run streamlit_app.py
```
The UI will open in your browser at `http://localhost:8501`

### 📖 Deployment Guides

- **Quick Start**: See [QUICK_START.md](QUICK_START.md)
- **Detailed Guide**: See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)

## 📚 API Documentation

### Endpoints

#### 1. Process Transaction
```http
POST /transaction
```

**Request Body:**
```json
{
  "transaction": {
    "amount": 500.00,
    "country": "US",
    "device": "device_123",
    "merchant": "amazon"
  },
  "profile": {
    "avg_amount": 100.00,
    "countries": ["KE"],
    "devices": ["device_456"],
    "merchants": ["grocery", "fuel"]
  }
}
```

**Response:**
```json
{
  "score": 85,
  "reasons": [
    "Very high amount: $500.00 vs avg $100.00",
    "New country detected: US",
    "Unknown device: device_123",
    "New merchant: amazon"
  ],
  "action": "ANALYST_QUEUE"
}
```

#### 2. Verify Transaction
```http
POST /verify
```

**Request Body:**
```json
{
  "response": "yes"
}
```

**Response:**
```json
{
  "verification_result": "APPROVED_BY_USER"
}
```

Accepted responses:
- **Approve**: yes, y, approve, confirm, ok
- **Block**: no, n, deny, block, reject

#### 3. Get Analyst Queue
```http
GET /queue
```

**Response:**
```json
{
  "queue": [
    {
      "transaction": {...},
      "score": 85,
      "reasons": [...],
      "timestamp": "2026-05-02T09:00:00.000Z",
      "status": "pending"
    }
  ]
}
```

#### 4. Health Check
```http
GET /
```

**Response:**
```json
{
  "status": "healthy",
  "service": "FraudX Agent API",
  "version": "1.0.0"
}
```

### Interactive API Documentation

Once the backend is running, visit:
- Swagger UI: `http://localhost:8001/docs`
- ReDoc: `http://localhost:8001/redoc`

## 🧪 Testing

Run the test suite:

```bash
pytest Tests/test_agent.py -v
```

Run with coverage:

```bash
pytest Tests/test_agent.py -v --cov=Backend --cov-report=html
```

## 📁 Project Structure

```
FRAUDX AGENT/
├── Backend/
│   ├── agent.py              # Fraud detection logic
│   ├── decision.py           # Risk-based decision making
│   ├── verification.py       # User verification handling
│   ├── analyst_queue.py      # Queue management for manual review
│   └── main.py              # FastAPI application
├── Frontend/
│   └── streamlit_app.py     # Streamlit UI
├── Tests/
│   └── test_agent.py        # Comprehensive test suite
├── data/
│   └── user.json            # Sample user profiles
├── requirements.txt          # Python dependencies
└── README.md                # This file
```

## 🔧 Configuration

### User Profiles

User profiles are stored in `data/user.json`:

```json
{
  "user_1": {
    "avg_amount": 40,
    "countries": ["KE"],
    "devices": ["device_1"],
    "merchants": ["grocery", "fuel"]
  }
}
```

### API Configuration

Edit `Backend/main.py` to change:
- Host and port settings
- CORS policies
- API metadata

### Frontend Configuration

Edit `Frontend/streamlit_app.py` to change:
- API endpoint URL
- UI theme and styling
- Page configuration

## 🛠️ Development

### Adding New Risk Factors

1. Update [`fraud_agent()`](Backend/agent.py:8) in `Backend/agent.py`
2. Add corresponding tests in `Tests/test_agent.py`
3. Update documentation

### Modifying Decision Thresholds

Edit the [`decide()`](Backend/decision.py:10) function in `Backend/decision.py`:

```python
def decide(score: int) -> ActionType:
    if score < 30:  # Adjust threshold
        return "APPROVE"
    elif score < 70:  # Adjust threshold
        return "VERIFY_USER"
    else:
        return "ANALYST_QUEUE"
```

## 📊 Example Use Cases

### 1. Normal Transaction
```python
transaction = {
    "amount": 45,
    "country": "KE",
    "device": "device_1",
    "merchant": "grocery"
}
# Result: Score ~0, Action: APPROVE
```

### 2. Suspicious Transaction
```python
transaction = {
    "amount": 500,
    "country": "US",
    "device": "device_999",
    "merchant": "unknown"
}
# Result: Score ~100, Action: ANALYST_QUEUE
```

### 3. Medium Risk Transaction
```python
transaction = {
    "amount": 150,
    "country": "KE",
    "device": "device_1",
    "merchant": "electronics"
}
# Result: Score ~35, Action: VERIFY_USER
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License.

## 🐛 Known Issues

- Queue is in-memory only (resets on restart)
- No persistent storage for transactions
- Limited to rule-based detection (no ML)

## 🚀 Future Enhancements

- [ ] Machine learning-based fraud detection
- [ ] Database integration for persistence
- [ ] Real-time notifications
- [ ] Advanced analytics dashboard
- [ ] Multi-factor authentication
- [ ] Transaction history tracking
- [ ] Configurable risk thresholds via UI
- [ ] Email/SMS alerts for high-risk transactions

## 📧 Support

For issues and questions, please open an issue on GitHub.

---

**Built with ❤️ for secure transactions**