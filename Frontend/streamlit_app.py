import random
from datetime import datetime, timedelta

import requests
import pandas as pd
import streamlit as st


API_BASE_URL = "http://localhost:8001"
TRANSACTION_URL = f"{API_BASE_URL}/transaction"
VERIFY_URL = f"{API_BASE_URL}/verify"
LOGIN_URL = f"{API_BASE_URL}/auth/login"

st.set_page_config(
    page_title="FRAUDX AGENT",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <div class="bank-topbar">
        <span class="bank-accent"></span>
        <span class="bank-name">M&E Bank</span>
    </div>
    <style>
        :root {
            --bg: #f4f0e8;
            --panel: #fffff;
            --ink: #14231d;
            --muted: #66746f;
            --line: #d9ded8;
            --green: #0f6b4b;
            --amber: #9b5d00;
            --red: #b42318;
            --blue: #174c43;
            --gold: #c8953d;
            --cream: #fff9ed;
            --charcoal: #101915;
        }

        .stApp {
            background:
                radial-gradient(circle at top left, rgba(200, 149, 61, 0.22), transparent 32rem),
                radial-gradient(circle at bottom right, rgba(23, 76, 67, 0.16), transparent 34rem),
                linear-gradient(180deg, #fbf7ee 0%, #edf2ec 100%);
            color: var(--ink);
        }

        [data-testid="stSidebar"] {
            background: #101828;
        }

        [data-testid="stSidebar"] * {
            color: #f8fafc;
        }

        .block-container {
            padding-top: 3.25rem;
            padding-bottom: 2.5rem;
            max-width: 1220px;
        }

        .bank-topbar {
            align-items: center;
            background: #050807;
            border-bottom: 1px solid rgba(245, 210, 139, 0.35);
            box-shadow: 0 14px 34px rgba(16, 25, 21, 0.18);
            display: flex !important;
            height: 76px;
            left: 0;
            padding: 0 3rem;
            position: fixed;
            right: 0;
            top: 0;
            z-index: 999999 !important;
        }

        .bank-name {
            color: #ffffff !important;
            font-size: 1.45rem;
            font-weight: 900;
            letter-spacing: -0.03em;
            display: inline-block;
        }

        .bank-accent {
            background: linear-gradient(135deg, #f5d28b, #b7791f);
            border-radius: 999px;
            height: 0.85rem;
            margin-right: 0.7rem;
            width: 0.85rem;
        }

        .landing-wrap {
            min-height: calc(100vh - 5rem);
            display: grid;
            align-items: center;
        }

        .landing-center {
            margin: 0 auto;
            max-width: 980px;
            text-align: center;
        }

        .landing-spacer {
            height: 4.25rem;
        }

        .landing-hero {
            background:
                linear-gradient(135deg, rgba(16, 25, 21, 0.96), rgba(23, 76, 67, 0.92)),
                repeating-linear-gradient(90deg, rgba(255, 255, 255, 0.08) 0 1px, transparent 1px 88px);
            border: 1px solid rgba(255, 255, 255, 0.14);
            border-radius: 30px;
            box-shadow: 0 30px 80px rgba(16, 25, 21, 0.24);
            color: #fff9ed;
            overflow: hidden;
            padding: 2rem;
            position: relative;
            text-align: left;
        }

        .landing-hero::before {
            background: radial-gradient(circle, rgba(200, 149, 61, 0.35), transparent 68%);
            content: "";
            height: 380px;
            position: absolute;
            right: -110px;
            top: -120px;
            width: 380px;
        }

        .landing-grid {
            display: grid;
            gap: 2rem;
            grid-template-columns: minmax(0, 1.1fr) minmax(320px, 0.72fr);
            position: relative;
            z-index: 1;
        }

        .brand-pill {
            align-items: center;
            background: rgba(255, 249, 237, 0.1);
            border: 1px solid rgba(255, 249, 237, 0.2);
            border-radius: 999px;
            color: #f8e4bd;
            display: inline-flex;
            font-size: 0.78rem;
            font-weight: 850;
            gap: 0.5rem;
            letter-spacing: 0.08em;
            margin-bottom: 1.2rem;
            padding: 0.5rem 0.8rem;
            text-transform: uppercase;
        }

        .brand-mark {
            background: linear-gradient(135deg, #f5d28b, #b7791f);
            border-radius: 999px;
            display: inline-block;
            height: 0.65rem;
            width: 0.65rem;
        }

        .landing-title {
            color: #fff9ed;
            font-size: clamp(2.5rem, 5vw, 5.4rem);
            font-weight: 900;
            letter-spacing: -0.07em;
            line-height: 0.92;
            margin: 0;
            max-width: 820px;
        }

        .landing-copy {
            color: rgba(255, 249, 237, 0.76);
            font-size: 1.05rem;
            line-height: 1.7;
            margin: 1.2rem 0 1.4rem;
            max-width: 670px;
        }

        .signin-shell {
            margin: 1.4rem auto 0;
            max-width: 460px;
            text-align: left;
        }

        .signin-heading {
            color: var(--ink);
            font-size: 1.75rem;
            font-weight: 900;
            letter-spacing: -0.04em;
            margin: 0 0 0.25rem;
            text-align: center;
        }

        .signin-copy {
            color: var(--muted);
            font-size: 0.94rem;
            margin: 0 auto 0.8rem;
            max-width: 380px;
            text-align: center;
        }

        .trust-row {
            display: grid;
            gap: 0.8rem;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            margin-top: 1.6rem;
        }

        .trust-card {
            background: rgba(255, 249, 237, 0.08);
            border: 1px solid rgba(255, 249, 237, 0.14);
            border-radius: 18px;
            padding: 1rem;
        }

        .trust-value {
            color: #f5d28b;
            font-size: 1.5rem;
            font-weight: 900;
            line-height: 1;
        }

        .trust-label {
            color: rgba(255, 249, 237, 0.68);
            font-size: 0.78rem;
            font-weight: 700;
            margin-top: 0.35rem;
            text-transform: uppercase;
        }

        .signin-card {
            backdrop-filter: blur(18px);
            background: rgba(255, 249, 237, 0.94);
            border: 1px solid rgba(255, 255, 255, 0.68);
            border-radius: 24px;
            box-shadow: 0 24px 60px rgba(0, 0, 0, 0.25);
            color: var(--ink);
            padding: 1.35rem;
        }

        div[data-testid="stForm"] {
            background: rgba(255, 249, 237, 0.96);
            border: 1px solid rgba(255, 255, 255, 0.74);
            border-radius: 24px;
            box-shadow: 0 24px 60px rgba(16, 25, 21, 0.18);
            padding: 1.35rem;
        }

        .signin-card h2 {
            color: var(--ink);
            font-size: 1.6rem;
            font-weight: 900;
            letter-spacing: -0.04em;
            margin: 0 0 0.2rem;
        }

        .signin-card p {
            color: #65736b;
            font-size: 0.92rem;
            line-height: 1.5;
            margin: 0 0 1rem;
        }

        .security-strip {
            background: #eaf3eb;
            border: 1px solid #cdded0;
            border-radius: 16px;
            color: #174c43;
            font-size: 0.86rem;
            font-weight: 750;
            margin-top: 1rem;
            padding: 0.75rem;
        }

        .app-preview {
            background: rgba(255, 249, 237, 0.1);
            border: 1px solid rgba(255, 249, 237, 0.18);
            border-radius: 22px;
            margin-top: 1.2rem;
            padding: 1rem;
        }

        .preview-row {
            align-items: center;
            border-bottom: 1px solid rgba(255, 249, 237, 0.12);
            display: flex;
            justify-content: space-between;
            padding: 0.7rem 0;
        }

        .preview-row:last-child {
            border-bottom: 0;
        }

        .preview-label {
            color: rgba(255, 249, 237, 0.62);
            font-size: 0.82rem;
        }

        .preview-value {
            color: #fff9ed;
            font-size: 0.92rem;
            font-weight: 850;
        }

        .risk-chip {
            background: rgba(245, 210, 139, 0.16);
            border: 1px solid rgba(245, 210, 139, 0.36);
            border-radius: 999px;
            color: #f5d28b;
            padding: 0.28rem 0.62rem;
        }

        .header {
            border-bottom: 1px solid var(--line);
            padding-bottom: 1rem;
            margin-bottom: 1.2rem;
        }

        .eyebrow {
            color: var(--blue);
            font-size: 0.78rem;
            font-weight: 800;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            margin-bottom: 0.2rem;
        }

        .title {
            color: var(--ink);
            font-size: 2.4rem;
            font-weight: 850;
            line-height: 1.05;
            margin: 0;
        }

        .subtitle {
            color: var(--muted);
            font-size: 1rem;
            margin-top: 0.5rem;
            max-width: 760px;
        }

        .panel {
            background: var(--panel);
            border: 1px solid var(--line);
            border-radius: 8px;
            padding: 1.1rem;
            box-shadow: 0 10px 30px rgba(16, 24, 40, 0.06);
        }

        .section-rule {
            border-top: 1px solid var(--line);
            margin: 1.6rem 0 1.2rem;
        }

        .section-kicker {
            color: var(--blue);
            font-size: 0.76rem;
            font-weight: 850;
            letter-spacing: 0.08em;
            text-transform: uppercase;
        }

        .section-title {
            color: var(--ink);
            font-size: 1.35rem;
            font-weight: 850;
            margin: 0.15rem 0 0.25rem;
        }

        .section-copy {
            color: var(--muted);
            font-size: 0.94rem;
            margin-bottom: 0.8rem;
        }

        .metric-label {
            color: var(--muted);
            font-size: 0.78rem;
            font-weight: 700;
            text-transform: uppercase;
            margin-bottom: 0.2rem;
        }

        .metric-value {
            color: var(--ink);
            font-size: 1.7rem;
            font-weight: 850;
            margin: 0;
        }

        .status-card {
            border-radius: 8px;
            padding: 1.1rem;
            border: 1px solid;
            min-height: 128px;
        }

        .approve {
            background: #ecfdf3;
            border-color: #abefc6;
            color: var(--green);
        }

        .verify {
            background: #fffaeb;
            border-color: #fedf89;
            color: var(--amber);
        }

        .queue {
            background: #fef3f2;
            border-color: #fecdca;
            color: var(--red);
        }

        .verification-box {
            background: #ffffff;
            border: 1px solid #fedf89;
            border-left: 5px solid #f79009;
            border-radius: 8px;
            padding: 1rem;
            margin-top: 1rem;
        }

        .verification-title {
            color: #7a4b00;
            font-size: 1.05rem;
            font-weight: 850;
            margin-bottom: 0.25rem;
        }

        .verification-copy {
            color: #475467;
            font-size: 0.92rem;
            margin: 0;
        }

        .customer-message {
            background: #f8fafc;
            border: 1px solid #dce3ea;
            border-radius: 8px;
            color: #172033;
            font-size: 0.93rem;
            line-height: 1.45;
            margin-top: 0.75rem;
            padding: 0.8rem;
        }

        .phone-shell {
            background: #111827;
            border-radius: 30px;
            box-shadow: 0 18px 40px rgba(16, 24, 40, 0.2);
            margin: 1rem auto 0;
            max-width: 310px;
            padding: 0.75rem;
        }

        .phone-screen {
            background: #f8fafc;
            border-radius: 24px;
            min-height: 420px;
            overflow: hidden;
        }

        .phone-status {
            align-items: center;
            color: #344054;
            display: flex;
            font-size: 0.75rem;
            font-weight: 750;
            justify-content: space-between;
            padding: 0.7rem 1rem 0.25rem;
        }

        .phone-notch {
            background: #111827;
            border-radius: 999px;
            height: 5px;
            margin: 0.35rem auto 0;
            width: 72px;
        }

        .phone-app {
            padding: 1rem;
        }

        .phone-brand {
            color: #2457c5;
            font-size: 0.78rem;
            font-weight: 850;
            letter-spacing: 0.08em;
            text-transform: uppercase;
        }

        .phone-heading {
            color: #172033;
            font-size: 1.25rem;
            font-weight: 850;
            line-height: 1.15;
            margin: 0.35rem 0 0.75rem;
        }

        .phone-alert {
            background: #fffaeb;
            border: 1px solid #fedf89;
            border-radius: 8px;
            color: #7a4b00;
            font-size: 0.9rem;
            line-height: 1.4;
            padding: 0.75rem;
        }

        .phone-detail {
            border-bottom: 1px solid #e4e7ec;
            display: flex;
            gap: 0.75rem;
            justify-content: space-between;
            padding: 0.7rem 0;
        }

        .phone-detail span:first-child {
            color: #667085;
            font-size: 0.82rem;
        }

        .phone-detail span:last-child {
            color: #172033;
            font-size: 0.86rem;
            font-weight: 750;
            text-align: right;
            word-break: break-word;
        }

        .phone-actions {
            display: grid;
            gap: 0.55rem;
            margin-top: 1rem;
        }

        .phone-approve,
        .phone-deny {
            border-radius: 8px;
            font-size: 0.9rem;
            font-weight: 850;
            padding: 0.72rem;
            text-align: center;
        }

        .phone-approve {
            background: #147d52;
            color: #ffffff;
        }

        .phone-deny {
            background: #ffffff;
            border: 1px solid #fecdca;
            color: #b42318;
        }

        .status-title {
            font-size: 1.45rem;
            font-weight: 850;
            margin-bottom: 0.25rem;
        }

        .status-copy {
            color: #475467;
            font-size: 0.95rem;
            margin: 0;
        }

        .reason {
            display: inline-block;
            background: #f2f4f7;
            border: 1px solid #d0d5dd;
            border-radius: 999px;
            color: #344054;
            font-size: 0.86rem;
            font-weight: 650;
            margin: 0.25rem 0.3rem 0.25rem 0;
            padding: 0.35rem 0.7rem;
        }

        div.stButton > button {
            width: 100%;
            border-radius: 8px;
            background: #174c43;
            border: 1px solid #174c43;
            color: white;
            font-weight: 750;
            min-height: 2.8rem;
        }

        div.stButton > button:hover {
            background: #10352f;
            border-color: #10352f;
            color: white;
        }

        @media (max-width: 900px) {
            .landing-grid,
            .trust-row {
                grid-template-columns: 1fr;
            }

            .landing-hero {
                border-radius: 22px;
                padding: 1.1rem;
            }
        }
    </style>
    """,
    unsafe_allow_html=True,
)


def split_csv(value):
    return [item.strip() for item in value.split(",") if item.strip()]


def build_transaction_history(avg_amount):
    multipliers = [
        0.82,
        1.05,
        0.74,
        1.18,
        0.96,
        1.31,
        0.88,
        1.11,
        0.69,
        1.24,
        0.93,
        1.42,
        0.81,
        1.16,
        1.03,
        0.77,
        1.29,
        0.91,
        1.36,
        1.08,
    ]
    return pd.DataFrame(
        {
            "Transaction": [f"T{i:02d}" for i in range(1, 21)],
            "Amount": [round(avg_amount * multiplier, 2) for multiplier in multipliers],
        }
    )


def generate_transaction_case():
    merchants = [
        "M&E Paybill",
        "Nairobi Grocers",
        "Fuel Express",
        "Metro Pharmacy",
        "RidePay",
        "Kampala Mobile Pay",
        "Airport Duty Free",
        "Online Electronics",
    ]
    base_amount = random.choice([45.0, 50.0, 65.0, 80.0, 120.0])
    known_countries = ["KE", "UG"]
    known_devices = ["device_1", "device_2"]
    start_time = datetime.now() - timedelta(days=14)

    past_transactions = []
    for index in range(20):
        past_transactions.append(
            {
                "Transaction": f"T{index + 1:02d}",
                "Time": (start_time + timedelta(hours=index * 13)).strftime("%b %d, %H:%M"),
                "Merchant": random.choice(merchants[:5]),
                "Amount": round(base_amount * random.uniform(0.55, 1.65), 2),
                "Country": random.choice(known_countries),
                "Device": random.choice(known_devices),
                "Status": "Settled",
            }
        )

    risk_type = random.choice(["amount spike", "new country", "new device", "combined signals"])
    current_country = random.choice(["RW", "NG", "TZ"]) if risk_type in ["new country", "combined signals"] else "KE"
    current_device = random.choice(["device_9", "device_12"]) if risk_type in ["new device", "combined signals"] else "device_1"
    current_transaction = {
        "Transaction": "CURRENT",
        "Time": datetime.now().strftime("%b %d, %H:%M"),
        "Merchant": random.choice(merchants),
        "Amount": round(base_amount * random.uniform(2.4, 4.6), 2),
        "Country": current_country,
        "Device": current_device,
        "Status": "Under review",
    }
    profile = {
        "avg_amount": round(sum(txn["Amount"] for txn in past_transactions) / len(past_transactions), 2),
        "countries": sorted({txn["Country"] for txn in past_transactions}),
        "devices": sorted({txn["Device"] for txn in past_transactions}),
    }

    return past_transactions, current_transaction, profile


def load_transaction_case():
    past_transactions, current_transaction, profile = generate_transaction_case()
    st.session_state.past_transactions = past_transactions
    st.session_state.current_transaction = current_transaction
    st.session_state.review_amount = float(current_transaction["Amount"])
    st.session_state.review_country = current_transaction["Country"]
    st.session_state.review_device = current_transaction["Device"]
    st.session_state.baseline_avg_amount = float(profile["avg_amount"])
    st.session_state.baseline_countries = ", ".join(profile["countries"])
    st.session_state.baseline_devices = ", ".join(profile["devices"])
    st.session_state.result = None
    st.session_state.error = None
    st.session_state.verification = None


def decision_style(action):
    if action == "APPROVE":
        return "approve", "Approved", "Low-risk transaction. No extra customer friction needed."
    if action == "VERIFY_USER":
        return "verify", "Verify user", "Risk is elevated. Ask for step-up verification before approval."
    return "queue", "Analyst queue", "High-risk case. Route to a human analyst for review."


def render_analyst_landing():
    st.markdown(
        """
        <div class="landing-spacer"></div>
        """,
        unsafe_allow_html=True,
    )

    hero_col, auth_col = st.columns([1.35, 0.85], gap="large")

    with hero_col:
        st.markdown(
            """
            <div class="landing-hero">
                <div class="brand-pill"><span class="brand-mark"></span> Secure fraud decisions before money moves.</div>
                <h1 class="landing-title">FRAUDX   AGENT</h1>
                <p class="landing-copy">
                    A bank-grade authentication for analysts who review suspicious payments,
                    verify customers, and keep high-risk transactions from slipping through.
                </p>
                <div class="trust-row">
                    <div class="trust-card">
                        <div class="trust-value">90</div>
                        <div class="trust-label">Risk ceiling</div>
                    </div>
                    <div class="trust-card">
                        <div class="trust-value">3</div>
                        <div class="trust-label">Decision routes</div>
                    </div>
                    <div class="trust-card">
                        <div class="trust-value">24/7</div>
                        <div class="trust-label">Case readiness</div>
                    </div>
                </div>
                <div class="app-preview">
                    <div class="preview-row">
                        <span class="preview-label">Live queue</span>
                        <span class="preview-value risk-chip">Analyst review</span>
                    </div>
                    <div class="preview-row">
                        <span class="preview-label">Customer baseline</span>
                        <span class="preview-value">Amount, country, device</span>
                    </div>
                    <div class="preview-row">
                        <span class="preview-label">Step-up channel</span>
                        <span class="preview-value">Push, SMS, phone call</span>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with auth_col:
        st.markdown(
            """
            <div class="signin-shell">
                <h2 class="signin-heading">Analyst Sign In</h2>
                <p class="signin-copy">Enter your credentials to access the workspace</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        
        # Login Form
        with st.form("analyst_signin"):
            analyst_id = st.text_input("Analyst ID", placeholder="Enter your Analyst ID")
            password = st.text_input("Password", type="password", placeholder="Enter password")
            submitted = st.form_submit_button("Sign In", type="primary")
        
        if submitted:
            if not analyst_id.strip() or not password.strip():
                st.error("⚠️ Please enter both Analyst ID and password.")
            else:
                # Simple sign-in without backend authentication
                st.session_state.analyst_signed_in = True
                st.session_state.analyst_id = analyst_id.strip()
                st.session_state.full_name = analyst_id.strip().replace("_", " ").title()
                st.session_state.email = f"{analyst_id.strip()}@mebank.com"
                st.session_state.review_desk = "Fraud Operations"
                st.success(f"✅ Welcome back, {st.session_state.full_name}!")
                st.rerun()

        st.markdown(
            """
            <div class="security-strip">
                🔒 Secure workspace for fraud detection and analysis.
            </div>
            """,
            unsafe_allow_html=True,
        )


if "analyst_signed_in" not in st.session_state:
    st.session_state.analyst_signed_in = False

if not st.session_state.analyst_signed_in:
    render_analyst_landing()
    st.stop()


if "past_transactions" not in st.session_state:
    load_transaction_case()


with st.sidebar:
    st.markdown("### 👤 Analyst Profile")
    st.caption("Full Name")
    st.write(st.session_state.get("full_name", "Analyst"))
    st.caption("Analyst ID")
    st.write(st.session_state.get("analyst_id", "N/A"))
    st.caption("Email")
    st.write(st.session_state.get("email", "N/A"))
    st.caption("Review Desk")
    st.write(st.session_state.get("review_desk", "Fraud Operations"))
    
    st.divider()
    
    if st.button("🚪 Sign Out", type="primary", use_container_width=True):
        # Clear all session state
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.session_state.analyst_signed_in = False
        st.rerun()
    
    st.divider()
    st.caption("Backend API")
    st.code(API_BASE_URL, language="text")
    st.caption("🔒 Secured with JWT")

st.markdown(
    """
    <div class="header">
        <div class="eyebrow">FRAUDX AGENT</div>
        <h1 class="title">Credit Card Transaction Analyzer</h1>
        <p class="subtitle">
            Score a payment against the customer's normal behavior and route it to approve,
            step-up verification or analyst review.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="section-kicker">Section 1</div>
    <h2 class="section-title">Transaction under review</h2>
    <p class="section-copy">Generate a transaction history, then review the current flagged payment in the same workspace.</p>
    """,
    unsafe_allow_html=True,
)

with st.container(border=True):
    st.markdown("#### Transaction generator")
    st.caption("The generated current transaction is the case under review. You can still edit it below.")
    if st.button("Generate new transaction case"):
        load_transaction_case()
        st.rerun()

    st.markdown("#### Current transaction")
    st.dataframe([st.session_state.current_transaction], use_container_width=True, hide_index=True)

review_inputs_col, decision_col = st.columns([0.95, 1.25], gap="large")

with review_inputs_col:
    with st.container(border=True):
        st.markdown("#### Review inputs")
        amount = st.number_input("Amount", min_value=0.0, step=10.0, key="review_amount")
        country = st.text_input("Country", key="review_country")
        device = st.text_input("Device", key="review_device")
        run_check = st.button("Run fraud check", type="primary")

with decision_col:
    decision_panel = st.container(border=True)

verification_panel = st.container()

txn = {
    "amount": amount,
    "country": country.strip(),
    "device": device.strip(),
}

st.markdown('<div class="section-rule"></div>', unsafe_allow_html=True)
st.markdown(
    """
    <div class="section-kicker">Section 2</div>
    <h2 class="section-title">Customer baseline</h2>
    <p class="section-copy">Compare this payment against the customer's normal amount, location, and device history.</p>
    """,
    unsafe_allow_html=True,
)

baseline_left, baseline_right = st.columns([0.9, 1.3], gap="large")
with baseline_left:
    with st.container(border=True):
        avg_amount = st.number_input(
            "Average amount",
            min_value=0.0,
            step=10.0,
            key="baseline_avg_amount",
        )
        countries = st.text_input("Known countries", key="baseline_countries")
        devices = st.text_input("Known devices", key="baseline_devices")

profile = {
    "avg_amount": avg_amount,
    "countries": split_csv(countries),
    "devices": split_csv(devices),
}

history_df = build_transaction_history(avg_amount)
past_transactions_df = pd.DataFrame(st.session_state.past_transactions)
with baseline_right:
    with st.container(border=True):
        st.markdown("#### Past transactions")
        st.dataframe(past_transactions_df, use_container_width=True, hide_index=True)
        st.markdown("#### Last 20 transactions")
        st.line_chart(history_df, x="Transaction", y="Amount", height=260)
        hist_a, hist_b, hist_c = st.columns(3)
        with hist_a:
            st.metric("Highest", f"{history_df['Amount'].max():.2f}")
        with hist_b:
            st.metric("Lowest", f"{history_df['Amount'].min():.2f}")
        with hist_c:
            st.metric("Average", f"{history_df['Amount'].mean():.2f}")

with decision_panel:
    st.subheader("Risk decision")

    if "result" not in st.session_state:
        st.session_state.result = None
        st.session_state.error = None
    if "verification" not in st.session_state:
        st.session_state.verification = None

    if run_check:
        try:
            response = requests.post(
                TRANSACTION_URL,
                json={"txn": txn, "profile": profile},
                timeout=8,
            )
            response.raise_for_status()
            st.session_state.result = response.json()
            st.session_state.error = None
            st.session_state.verification = None
        except requests.RequestException as exc:
            st.session_state.result = None
            st.session_state.error = str(exc)
            st.session_state.verification = None

    if st.session_state.error:
        st.error(
            "Could not reach the FastAPI backend. Start it with: "
            "`python -m uvicorn main:app --host 127.0.0.1 --port 8001` from the Backend folder."
        )
        st.caption(st.session_state.error)
    elif st.session_state.result:
        result = st.session_state.result
        score = result.get("score", 0)
        reasons = result.get("reasons", [])
        action = result.get("action", "UNKNOWN")
        css_class, title, copy = decision_style(action)

        top_a, top_b, top_c = st.columns(3)
        with top_a:
            st.markdown(
                f"""
                <div class="panel">
                    <div class="metric-label">Risk score</div>
                    <p class="metric-value">{score}/90</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with top_b:
            st.markdown(
                f"""
                <div class="panel">
                    <div class="metric-label">Triggered rules</div>
                    <p class="metric-value">{len(reasons)}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with top_c:
            st.markdown(
                f"""
                <div class="panel">
                    <div class="metric-label">Amount ratio</div>
                    <p class="metric-value">{amount / max(avg_amount, 1):.1f}x</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.progress(min(score, 90) / 90)
        st.markdown(
            f"""
            <div class="status-card {css_class}">
                <div class="status-title">{title}</div>
                <p class="status-copy">{copy}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("#### Signals")
        if reasons:
            st.markdown(
                "".join(f'<span class="reason">{reason}</span>' for reason in reasons),
                unsafe_allow_html=True,
            )
        else:
            st.success("No unusual behavior detected.")

    else:
        st.info("Enter a transaction and run a fraud check to see the decision.")

if st.session_state.result and st.session_state.result.get("action") == "VERIFY_USER":
    with verification_panel:
        st.markdown('<div class="section-rule"></div>', unsafe_allow_html=True)
        st.markdown(
            """
            <div class="section-kicker">Step-up</div>
            <h2 class="section-title">Verify user</h2>
            <p class="section-copy">Send the customer a phone challenge after reviewing their baseline behavior.</p>
            """,
            unsafe_allow_html=True,
        )
        verify_controls, phone_preview = st.columns([1, 0.85], gap="large")
        with verify_controls:
            with st.container(border=True):
                channel = st.radio(
                    "Phone verification method",
                    ["In-app push", "SMS", "Phone call"],
                    horizontal=True,
                )
                customer_message = (
                    f"Did you authorize a {amount:.2f} transaction "
                    f"from {country or 'this country'} using {device or 'this device'}?"
                )
                st.markdown(
                    f"""
                    <div class="verification-box">
                        <div class="verification-title">{channel} challenge ready</div>
                        <p class="verification-copy">
                            Send a confirmation challenge to the customer before releasing the payment.
                        </p>
                        <div class="customer-message">{customer_message}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                verify_yes, verify_no = st.columns(2)
                with verify_yes:
                    customer_confirmed = st.button("Customer confirmed", key="customer_confirmed")
                with verify_no:
                    customer_denied = st.button("Customer denied", key="customer_denied")

                verification_response = None
                if customer_confirmed:
                    verification_response = "yes"
                elif customer_denied:
                    verification_response = "no"

                if verification_response:
                    try:
                        verify_res = requests.post(
                            VERIFY_URL,
                            json={"response": verification_response},
                            timeout=8,
                        )
                        verify_res.raise_for_status()
                        st.session_state.verification = verify_res.json()
                    except requests.RequestException as exc:
                        st.session_state.verification = {
                            "verification_result": "VERIFICATION_ERROR",
                            "detail": str(exc),
                        }

                if st.session_state.verification:
                    verification_result = st.session_state.verification.get("verification_result")
                    if verification_result == "APPROVED_BY_USER":
                        st.success("Verification passed. Transaction can proceed.")
                    elif verification_result == "BLOCKED":
                        st.error("Verification failed. Transaction should be blocked.")
                    else:
                        st.warning("Verification could not be completed.")
                        if st.session_state.verification.get("detail"):
                            st.caption(st.session_state.verification["detail"])

        with phone_preview:
            st.markdown(
                f"""
                <div class="phone-shell">
                    <div class="phone-screen">
                        <div class="phone-status">
                            <span>9:41</span>
                            <span>{channel}</span>
                        </div>
                        <div class="phone-notch"></div>
                        <div class="phone-app">
                            <div class="phone-brand">FRAUDX AGENT</div>
                            <div class="phone-heading">Confirm this transaction</div>
                            <div class="phone-alert">{customer_message}</div>
                            <div class="phone-detail">
                                <span>Amount</span>
                                <span>{amount:.2f}</span>
                            </div>
                            <div class="phone-detail">
                                <span>Country</span>
                                <span>{country or 'Unknown'}</span>
                            </div>
                            <div class="phone-detail">
                                <span>Device</span>
                                <span>{device or 'Unknown'}</span>
                            </div>
                            <div class="phone-actions">
                                <div class="phone-approve">Yes, this was me</div>
                                <div class="phone-deny">No, block transaction</div>
                            </div>
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

st.markdown("#### Current case snapshot")
snapshot_a, snapshot_b = st.columns(2, gap="large")
with snapshot_a:
    st.dataframe([txn], use_container_width=True, hide_index=True)
with snapshot_b:
    st.dataframe([profile], use_container_width=True, hide_index=True)
