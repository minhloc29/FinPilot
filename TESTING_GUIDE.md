# 🚀 Testing Authentication & Chat Flow

Complete guide to test the full-stack authentication system with real backend integration.

## ✅ What's Already Connected

Your React frontend is now **fully connected** to the FastAPI backend:

### Backend (FastAPI)
- ✅ User registration endpoint (`/api/v1/auth/register`)
- ✅ User login endpoint (`/api/v1/auth/login`)  
- ✅ Get user info endpoint (`/api/v1/auth/me`)
- ✅ Chat endpoint with authentication (`/api/v1/chat`)
- ✅ JWT token generation & validation
- ✅ Password hashing with bcrypt
- ✅ Database models for users, conversations, messages

### Frontend (React)
- ✅ Login/Register form with validation
- ✅ AuthContext for global auth state
- ✅ Token persistence in localStorage
- ✅ Protected routes (optional)
- ✅ User dropdown in navbar
- ✅ Chat panel using real backend API
- ✅ Error handling with toast notifications

## 🎯 Quick Start (2 Steps)

### Terminal 1 - Start Backend
```bash
cd /Users/macbook/Documents/Code/ai_agent_finance

# Option A: Use the startup script
./start_backend.sh

# Option B: Manual start
cd backend
python -c "from app.db.init_db import init_db; init_db()"
uvicorn app.main:app --reload
```

### Terminal 2 - Start Frontend
```bash
cd /Users/macbook/Documents/Code/ai_agent_finance

# Option A: Use the startup script
./start_frontend.sh

# Option B: Manual start
cd frontend
npm run dev
```

## 📝 Testing Steps

### 1️⃣ Test User Registration

1. Open browser: `http://localhost:3000/login`
2. Click **"Sign up"**
3. Fill in the form:
   - Email: `test@example.com`
   - Username: `testuser`
   - Full Name: `Test User` (optional)
   - Password: `password123`
   - Confirm Password: `password123`
4. Click **"Register"**

**Expected Result:**
- ✅ Success toast notification
- ✅ Redirected to home page
- ✅ Username appears in navbar dropdown (top right)
- ✅ Welcome message: "Welcome back, Test User!"

### 2️⃣ Test Chat with Authentication

1. On the home page, type a message in the chat:
   - "What is the current price of AAPL?"
2. Press Enter or click Send

**Expected Result:**
- ✅ Your message appears
- ✅ Loading indicator shows
- ✅ AI response appears from backend
- ✅ Conversation ID persists for follow-up questions

### 3️⃣ Test Token Persistence

1. While logged in, refresh the page (`F5` or `Cmd+R`)

**Expected Result:**
- ✅ Still logged in (no redirect to login page)
- ✅ Username still shows in navbar
- ✅ Welcome message still shows your name

### 4️⃣ Test Logout

1. Click on your username dropdown (top right)
2. Click **"Logout"**

**Expected Result:**
- ✅ Redirected to login page
- ✅ Token removed from localStorage
- ✅ Navbar shows "Login" button again

### 5️⃣ Test Login

1. On login page, enter:
   - Email: `test@example.com`
   - Password: `password123`
2. Click **"Login"**

**Expected Result:**
- ✅ Success toast notification
- ✅ Redirected to home page
- ✅ Username appears in navbar

### 6️⃣ Test Conversation Continuity

1. Send a message: "Tell me about AAPL stock"
2. Wait for response
3. Send follow-up: "What about its P/E ratio?"

**Expected Result:**
- ✅ Both messages use same conversation_id
- ✅ Backend maintains context
- ✅ Chat history persists

## 🔍 Verify Backend Connection

### Check if backend is running:
```bash
curl http://localhost:8000/api/v1/health
```

**Expected:** `{"status":"healthy",...}`

### Test registration via curl:
```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "curl@test.com",
    "password": "password123",
    "username": "curluser"
  }'
```

**Expected:** Returns user object and JWT token

### Test login via curl:
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "curl@test.com",
    "password": "password123"
  }'
```

**Expected:** Returns user object and JWT token

### Test authenticated chat:
```bash
# First, get token from login/register
TOKEN="your_token_here"

curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "message": "What stocks should I invest in?"
  }'
```

## 🐛 Troubleshooting

### "Database not found" error
```bash
cd backend
python -c "from app.db.init_db import init_db; init_db()"
```

### "Module not found" error
```bash
cd backend
pip install -r requirements.txt
```

### CORS errors in browser console
- Check backend `main.py` has `http://localhost:3000` in `ALLOWED_ORIGINS`
- Verify frontend `.env.development` has `VITE_API_URL=http://localhost:8000`

### "Token expired" or "Invalid token"
- Clear localStorage in browser DevTools
- Login again

### Chat not working
- Check backend terminal for errors
- Check browser Network tab for API calls
- Verify backend is running on port 8000

### Frontend shows old login button after login
- Hard refresh: `Ctrl+Shift+R` (Windows/Linux) or `Cmd+Shift+R` (Mac)
- Check if token is in localStorage (DevTools > Application > Local Storage)

## 📊 Check Logs

### Backend Logs
Look at the terminal running `uvicorn`:
```
INFO:     User registered successfully: test@example.com
INFO:     User logged in successfully: test@example.com
INFO:     Received chat request: What is...
```

### Frontend Logs
Open browser DevTools (F12) > Console:
- Should see successful API calls
- No CORS errors
- No 401/403 errors after login

## 🎉 Success Indicators

You know everything is working when:

1. ✅ Backend starts without errors
2. ✅ Frontend starts without errors
3. ✅ Can register new user
4. ✅ Can login with credentials
5. ✅ Username shows in navbar dropdown
6. ✅ Chat sends messages to backend
7. ✅ AI responses come from backend
8. ✅ Token persists on page refresh
9. ✅ Logout works correctly
10. ✅ Can login again

## 📝 Next Steps

Once everything works:

1. ✅ Test with multiple users
2. Add password reset flow
3. Add email verification
4. Implement refresh tokens
5. Add rate limiting
6. Set up production database
7. Deploy to production

## 🔐 Security Notes

**Current Setup (Development):**
- JWT tokens expire in 7 days
- Passwords hashed with bcrypt
- Tokens stored in localStorage
- CORS configured for localhost

**Before Production:**
- Use HTTPS
- Use httpOnly cookies instead of localStorage
- Add refresh tokens
- Implement rate limiting
- Use environment variables for secrets
- Set up proper database with backups

## 📚 API Documentation

Visit `http://localhost:8000/docs` for interactive API documentation (Swagger UI).

## ❓ Need Help?

Check these files for implementation:
- Backend auth: `backend/app/api/routes/auth.py`
- Frontend auth: `frontend/src/contexts/AuthContext.tsx`
- API service: `frontend/src/services/api.ts`
- Chat panel: `frontend/src/components/chat/ChatPanel.tsx`
