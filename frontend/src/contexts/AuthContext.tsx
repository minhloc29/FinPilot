import { createContext, useContext, useState, useEffect, ReactNode } from "react";
import { apiClient, User } from "@/services/api";

interface AuthContextType {
  user: User | null;
  token: string | null;
  login: (email: string, password: string) => Promise<void>;
  register: (data: RegisterData) => Promise<void>;
  logout: () => void;
  isLoading: boolean;
}

interface RegisterData {
  email: string;
  password: string;
  username: string;
  full_name?: string;
  phone_number?: string;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  // Load token and user from localStorage on mount
  useEffect(() => {
    const loadUser = async () => {
      const storedToken = localStorage.getItem("access_token");
      if (storedToken) {
        try {
          const userData = await apiClient.getCurrentUser(storedToken);
          setUser(userData);
          setToken(storedToken);
        } catch (error) {
          // Token might be expired or invalid
          localStorage.removeItem("access_token");
          console.error("Failed to load user:", error);
        }
      }
      setIsLoading(false);
    };

    loadUser();
  }, []);

  const login = async (email: string, password: string) => {
    try {
      const response = await apiClient.login(email, password);
      setUser(response.user);
      setToken(response.access_token);
      localStorage.setItem("access_token", response.access_token);
    } catch (error) {
      throw error;
    }
  };

  const register = async (data: RegisterData) => {
    try {
      const response = await apiClient.register(data);
      setUser(response.user);
      setToken(response.access_token);
      localStorage.setItem("access_token", response.access_token);
    } catch (error) {
      throw error;
    }
  };

  const logout = () => {
    if (token) {
      apiClient.logout(token).catch(console.error);
    }
    setUser(null);
    setToken(null);
    localStorage.removeItem("access_token");
  };

  return (
    <AuthContext.Provider value={{ user, token, login, register, logout, isLoading }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
}
