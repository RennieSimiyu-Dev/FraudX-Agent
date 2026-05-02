# Quick Start Guide - Authentication Setup

## ✅ Demo Account Ready!

Your demo account has been created and is ready to use:

- **Analyst ID**: `demo_analyst`
- **Password**: `demo123`
- **Full Name**: Demo Analyst
- **Email**: demo@fraudx.local
- **Review Desk**: Fraud Operations

## 🚀 How to Start the Application

### Step 1: Install Dependencies (if not already done)

```bash
pip install fastapi uvicorn pydantic streamlit requests pandas pytest python-jose passlib bcrypt python-multipart
```

### Step 2: Start the Backend Server

Open a terminal and run:

```bash
python Backend/main.py
```

Or use the batch file:

```bash
start_backend.bat
```

The backend will start on `http://localhost:8001`

### Step 3: Start the Frontend

Open a **new terminal** and run:

```bash
streamlit run Frontend/streamlit_app.py
```

Or use the batch file:

```bash
start_frontend.bat
```

The frontend will open in your browser automatically.

### Step 4: Sign In

1. You'll see the sign-in page
2. Enter:
   - **Analyst ID**: `demo_analyst`
   - **Password**: `demo123`
3. Click "Sign In"
4. You should be logged in and see the main workspace!

## 🆕 Creating a New Account

If you want to create your own account:

1. On the sign-in page, click "Don't have an account? Sign Up"
2. Fill in the registration form:
   - Choose a unique Analyst ID
   - Enter your full name
   - Provide your email
   - Create a password (min 6 characters)
   - Confirm your password
   - Select your review desk
3. Click "Create Account"
4. You'll be automatically signed in!

## ❌ Troubleshooting

### "Cannot connect to backend"

**Problem**: The backend server isn't running.

**Solution**: 
1. Make sure you started the backend server first
2. Check that it's running on port 8001
3. Look for any error messages in the backend terminal

### "Invalid analyst ID or password"

**Problem**: Credentials don't match.

**Solution**:
1. Make sure you're using the correct credentials:
   - Analyst ID: `demo_analyst` (case-sensitive)
   - Password: `demo123`
2. If you created your own account, use those credentials instead

### Backend won't start - "ModuleNotFoundError"

**Problem**: Required packages aren't installed.

**Solution**:
```bash
pip install fastapi uvicorn pydantic python-jose passlib bcrypt python-multipart
```

### Frontend won't start - "ModuleNotFoundError"

**Problem**: Streamlit or other packages aren't installed.

**Solution**:
```bash
pip install streamlit requests pandas
```

## 📝 What's New?

### Security Features Added:

1. **Password Hashing**: All passwords are hashed with bcrypt
2. **JWT Authentication**: Secure token-based authentication
3. **Session Management**: Tokens expire after 8 hours
4. **Sign Up Feature**: Users can create their own accounts
5. **Enhanced Sign In**: Proper authentication with the backend

### How It Works:

1. When you sign in, your credentials are sent to the backend
2. The backend verifies your password against the hashed version
3. If correct, you receive a JWT token
4. This token is stored in your session
5. You stay logged in until you sign out or the token expires

## 🔒 Security Notes

- Passwords are **never** stored in plain text
- All passwords are hashed using bcrypt
- JWT tokens are used for authentication
- Sessions are cleared when you sign out
- Default secret key should be changed in production

## 📚 More Information

For detailed authentication documentation, see:
- `AUTHENTICATION_GUIDE.md` - Complete authentication documentation
- `README.md` - General project documentation
- `DEPLOYMENT_GUIDE.md` - Deployment instructions

## 🎉 You're All Set!

Your authentication system is now fully configured and ready to use. Enjoy your secure FraudX Agent application!