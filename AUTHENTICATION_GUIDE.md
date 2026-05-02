# Authentication Guide - FraudX Agent

## Overview

The FraudX Agent now includes a secure authentication system with the following features:

### Security Features

1. **Password Hashing**: Uses bcrypt for secure password storage
2. **JWT Tokens**: JSON Web Tokens for stateless authentication
3. **Session Management**: Secure session handling with token validation
4. **Signup & Login**: Complete user registration and authentication flow

## Default Test Account

For testing purposes, a demo account is pre-configured:

- **Analyst ID**: `demo_analyst`
- **Password**: `demo123`
- **Full Name**: Demo Analyst
- **Email**: demo@fraudx.local
- **Review Desk**: Fraud Operations

## Using the Authentication System

### Sign In

1. Start the backend and frontend servers
2. Navigate to the application
3. Enter your Analyst ID and Password
4. Click "Sign In"
5. Upon successful authentication, you'll be redirected to the main workspace

### Sign Up (Create New Account)

1. On the sign-in page, click "Don't have an account? Sign Up"
2. Fill in the registration form:
   - **Analyst ID**: Unique identifier (min 3 characters)
   - **Full Name**: Your full name
   - **Email**: Valid email address
   - **Password**: Secure password (min 6 characters)
   - **Confirm Password**: Re-enter password
   - **Review Desk**: Select your department
3. Click "Create Account"
4. Upon successful registration, you'll be automatically signed in

### Sign Out

Click the "🚪 Sign Out" button in the sidebar to end your session.

## API Endpoints

### POST /auth/login
Authenticate an analyst and receive an access token.

**Request Body:**
```json
{
  "analyst_id": "demo_analyst",
  "password": "demo123"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "analyst_id": "demo_analyst",
  "full_name": "Demo Analyst",
  "email": "demo@fraudx.local",
  "review_desk": "Fraud Operations"
}
```

### POST /auth/signup
Register a new analyst account.

**Request Body:**
```json
{
  "analyst_id": "new_analyst",
  "password": "secure_password",
  "full_name": "John Doe",
  "email": "john@fraudx.local",
  "review_desk": "Card Payments"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "analyst_id": "new_analyst",
  "full_name": "John Doe",
  "email": "john@fraudx.local",
  "review_desk": "Card Payments"
}
```

### GET /auth/me
Get current authenticated analyst information (requires valid JWT token).

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response:**
```json
{
  "analyst_id": "demo_analyst",
  "full_name": "Demo Analyst",
  "email": "demo@fraudx.local",
  "review_desk": "Fraud Operations"
}
```

## Security Configuration

### Environment Variables

You can customize the JWT secret key by setting the `SECRET_KEY` environment variable:

```bash
# Windows
set SECRET_KEY=your-super-secret-key-here

# Linux/Mac
export SECRET_KEY=your-super-secret-key-here
```

**Important**: Change the default secret key in production!

### Token Expiration

- Default token expiration: 8 hours (480 minutes)
- Tokens are automatically validated on protected endpoints
- Expired tokens will require re-authentication

## Database

Analyst credentials are stored in `data/analysts.json` with the following structure:

```json
{
  "analyst_id": {
    "analyst_id": "demo_analyst",
    "hashed_password": "$2b$12$...",
    "full_name": "Demo Analyst",
    "email": "demo@fraudx.local",
    "review_desk": "Fraud Operations",
    "created_at": "2026-05-02T10:00:00.000000",
    "is_active": true
  }
}
```

**Note**: Passwords are never stored in plain text. Only bcrypt hashes are saved.

## Password Requirements

- Minimum length: 6 characters
- No maximum length
- All characters allowed
- Passwords are case-sensitive

## Best Practices

1. **Use Strong Passwords**: Combine letters, numbers, and special characters
2. **Don't Share Credentials**: Each analyst should have their own account
3. **Sign Out When Done**: Always sign out after completing your work
4. **Change Default Credentials**: Update the demo account password in production
5. **Secure the Secret Key**: Use a strong, random secret key in production

## Troubleshooting

### "Cannot connect to backend"
- Ensure the backend server is running on port 8001
- Check that `API_BASE_URL` is correctly configured

### "Invalid analyst ID or password"
- Verify your credentials are correct
- Analyst IDs are case-sensitive
- Ensure you're using the correct password

### "Analyst ID already registered"
- The analyst ID must be unique
- Try a different analyst ID or sign in with existing credentials

### Token Expired
- Your session has expired after 8 hours
- Simply sign in again to get a new token

## Technical Details

### Dependencies

- **passlib[bcrypt]**: Password hashing
- **python-jose[cryptography]**: JWT token handling
- **python-multipart**: Form data parsing

### Authentication Flow

1. User submits credentials (login) or registration data (signup)
2. Backend validates input and checks credentials/creates account
3. Backend generates JWT token with user data
4. Token is returned to frontend and stored in session state
5. Frontend includes token in subsequent API requests (if needed)
6. Backend validates token on protected endpoints

### Security Measures

- Passwords hashed with bcrypt (cost factor: 12)
- JWT tokens signed with HS256 algorithm
- Tokens include expiration timestamp
- Session state cleared on sign out
- Input validation on all endpoints
- HTTPS recommended for production

## Support

For issues or questions about authentication, please refer to the main README.md or contact the development team.