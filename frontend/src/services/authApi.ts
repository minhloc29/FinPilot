import { request } from "./client";

export interface User {
  id: number
  email: string
  username: string
  full_name?: string
  is_active: boolean
  is_superuser: boolean
}

export interface AuthResponse {
  user: User
  access_token: string
  token_type: string
}

export interface RegisterRequest {
  email: string
  password: string
  username: string
  full_name?: string
  phone_number?: string
}

export async function register(data: RegisterRequest) {
  return request<AuthResponse>("/api/v1/auth/register", {
    method: "POST",
    body: JSON.stringify(data)
  })
}

export async function login(email: string, password: string) {
  return request<AuthResponse>("/api/v1/auth/login", {
    method: "POST",
    body: JSON.stringify({ email, password })
  })
}

export async function getCurrentUser(token: string) {
  return request<User>("/api/v1/auth/me", {
    headers: {
      Authorization: `Bearer ${token}`
    }
  })
}

export async function logout(token: string) {
  return request<{ message: string }>("/api/v1/auth/logout", {
    method: "POST",
    headers: {
      Authorization: `Bearer ${token}`
    }
  })
}