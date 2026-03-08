# Authentication Integration Guide

Complete guide for the React + FastAPI authentication system.

## Overview

Your authentication system is now fully integrated with:
- ✅ User registration and login
- ✅ JWT token management
- ✅ Protected routes
- ✅ Automatic token persistence
- ✅ User profile dropdown
- ✅ Logout functionality

## Files Created/Modified

### Backend (Already Done)
- `/backend/app/api/routes/auth.py` - Auth endpoints
- `/backend/app/services/auth_service.py` - Auth business logic
- `/backend/app/schemas/auth_schema.py` - Auth data models
- `/backend/app/api/dependencies.py` - JWT verification

### Frontend (Just Created)
- `/frontend/src/contexts/AuthContext.tsx` - Auth state management
- `/frontend/src/components/ProtectedRoute.tsx` - Route protection
- `/frontend/src/services/api.ts` - Updated with auth methods
- `/frontend/src/pages/Login.tsx` - Updated with backend integration
- `/frontend/src/components/layout/Navbar.tsx` - User dropdown & logout
- `/frontend/src/App.tsx` - Wrapped with AuthProvider

## How It Works

### 1. **User Registration Flow**
```typescript
// When user submits registration form:
1. Login.tsx calls register() from useAuth()
2. AuthContext calls apiClient.register()
3. Backend creates user and returns JWT token
4. Token saved to localStorage
5. User redirected to home page
```

### 2. **User Login Flow**
```typescript
// When user submits login form:
1. Login.tsx calls login() from useAuth()
2. AuthContext calls apiClient.login()
3. Backend verifies credentials and returns JWT token
4. Token saved to localStorage
5. User redirected to home page
```

### 3. **Token Persistence**
```typescript
// On app load:
1. AuthContext checks localStorage for token
2. If token exists, fetches user data from /api/v1/auth/me
3. If successful, sets user state
4. If fails, removes invalid token
```

### 4. **Protected Routes**
```typescript
// Wrap any route that requires authentication:
<Route path="/dashboard" element={
  <ProtectedRoute>
    <Dashboard />
  </ProtectedRoute>
} />
```

## Usage Examples

### 1. **Using Auth in Components**

```typescript
import { useAuth } from "@/contexts/AuthContext";

function MyComponent() {
  const { user, token, logout } = useAuth();

  if (user) {
    return <div>Welcome, {user.username}!</div>;
  }

  return <div>Please log in</div>;
}
```

### 2. **Making Authenticated API Calls**

```typescript
import { useAuth } from "@/contexts/AuthContext";
import { apiClient } from "@/services/api";

function ChatComponent() {
  const { token } = useAuth();

  const sendMessage = async (message: string) => {
    if (token) {
      const response = await apiClient.sendAuthenticatedChatMessage(
        { message },
        token
      );
      console.log(response);
    }
  };

  return <button onClick={() => sendMessage("Hello")}>Send</button>;
}
```

### 3. **Checking User State**

```typescript
const { user, isLoading } = useAuth();

if (isLoading) {
  return <LoadingSpinner />;
}

if (!user) {
  return <LoginPrompt />;
}

return <UserDashboard user={user} />;
```

## API Endpoints

### Register
```bash
POST http://localhost:8000/api/v1/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123",
  "username": "username",
  "full_name": "John Doe"  # Optional
}
```

### Login
```bash
POST http://localhost:8000/api/v1/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123"
}
```

### Get Current User
```bash
GET http://localhost:8000/api/v1/auth/me
Authorization: Bearer YOUR_TOKEN
```

### Logout
```bash
POST http://localhost:8000/api/v1/auth/logout
Authorization: Bearer YOUR_TOKEN
```

## Testing

### 1. **Test Registration**
```bash
# Start backend
cd backend
uvicorn app.main:app --reload

# Start frontend
cd frontend
npm run dev

# Visit http://localhost:3000/login
# Click "Sign up" and create an account
```

### 2. **Test Login**
```bash
# Visit http://localhost:3000/login
# Enter credentials and login
# Should redirect to home page with username in navbar
```

### 3. **Test Token Persistence**
```bash
# Login to the app
# Refresh the page
# Should remain logged in
```

### 4. **Test Logout**
```bash
# Click on username dropdown in navbar
# Click "Logout"
# Should return to login page
```

## Environment Variables

Create `.env.development` in frontend folder:
```env
VITE_API_URL=http://localhost:8000
```

Create `.env` in backend folder:
```env
SECRET_KEY=your-secret-key-here-change-in-production
DATABASE_URL=postgresql://user:password@localhost/financial_copilot
```

## Adding Protected Routes

### Example: Protected Dashboard
```typescript
// In App.tsx
import { ProtectedRoute } from "@/components/ProtectedRoute";
import Dashboard from "./pages/Dashboard";

<Routes>
  <Route path="/" element={<Index />} />
  <Route path="/login" element={<Login />} />
  <Route 
    path="/dashboard" 
    element={
      <ProtectedRoute>
        <Dashboard />
      </ProtectedRoute>
    } 
  />
</Routes>
```

## Security Best Practices

✅ **Currently Implemented:**
- JWT tokens with expiration (7 days)
- Password hashing with bcrypt
- Token stored in localStorage
- Automatic token validation on app load

⚠️ **Additional Recommendations:**
1. Use HTTPS in production
2. Implement refresh tokens
3. Add rate limiting on auth endpoints
4. Implement password reset flow
5. Add email verification
6. Consider httpOnly cookies for tokens

## Troubleshooting

### Token Not Persisting
- Check localStorage in browser DevTools
- Ensure token is being saved after login/register

### CORS Errors
- Check backend CORS settings in `main.py`
- Ensure frontend URL is in `ALLOWED_ORIGINS`

### "User not authenticated" Error
- Token might be expired
- Clear localStorage and login again
- Check backend logs for JWT validation errors

### Registration/Login Not Working
- Check Network tab in DevTools
- Verify backend is running on port 8000
- Check backend logs for errors
- Verify database is connected

## Next Steps

1. ✅ Test registration and login flows
2. Add forgot password functionality
3. Add email verification
4. Implement refresh tokens
5. Add user profile page
6. Add OAuth integration (Google, Facebook)
7. Add 2FA support

## Questions?

Check the following files for implementation details:
- Auth logic: `/frontend/src/contexts/AuthContext.tsx`
- API calls: `/frontend/src/services/api.ts`
- Login UI: `/frontend/src/pages/Login.tsx`
- Backend auth: `/backend/app/api/routes/auth.py`
