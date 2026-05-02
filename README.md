# FraudX Agent 

A real-time fraud detection system that analyzes transactions and identifies suspicious activities using rule-based risk scoring.

Features

- **Real-time Fraud Detection**: Analyzes transactions instantly based on multiple risk factors
- **Risk Scoring**: Calculates fraud risk scores (0-100) with detailed reasoning
- **Automated Decision Making**: Routes transactions based on risk level
- **User Verification**: Requests user confirmation for medium-risk transactions
- **Analyst Queue**: Flags high-risk transactions for manual review
- **RESTful API**: FastAPI backend with comprehensive endpoints
- **Interactive UI**: Streamlit-based frontend for monitoring and testing

Risk Factors

The system evaluates transactions based on:

1. **Transaction Amount**: Compares against user's average spending
   - 5x average: +40 points
   - 3x average: +30 points
   - 2x average: +20 points

2. **Geographic Location**: Detects transactions from new countries (+25 points)

3. **Device Recognition**: Identifies unknown devices (+20 points)

4. **Merchant Verification**: Flags new merchants (+15 points)

Decision Logic

| Risk Score | Action | Description |
|------------|--------|-------------|
| 0-29 | **APPROVE** | Low risk - Process automatically |
| 30-69 | **VERIFY_USER** | Medium risk - Request user confirmation |
| 70-100 | **ANALYST_QUEUE** | High risk - Manual review required |

## 📝 License

This project is licensed under the MIT License.

Known Issues

- Queue is in-memory only (resets on restart)
- No persistent storage for transactions
- Limited to rule-based detection (no ML)

Future Enhancements

- [ ] Machine learning-based fraud detection
- [ ] Database integration for persistence
- [ ] Real-time notifications
- [ ] Advanced analytics dashboard
- [ ] Multi-factor authentication
- [ ] Transaction history tracking
- [ ] Configurable risk thresholds via UI
- [ ] Email/SMS alerts for high-risk transactions

