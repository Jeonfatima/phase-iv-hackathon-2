'use client';

import React, { createContext, useContext, useEffect, useState, ReactNode } from 'react';
import { authClient } from '@/lib/auth';
import { User } from '@/lib/types';

interface AuthContextType {
  user: User | null;
  isLoading: boolean;
  isAuthenticated: boolean;
  token: string | null;
  login: (email: string, password: string) => Promise<any>;
  register: (email: string, password: string) => Promise<any>;
  logout: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const login = async (email: string, password: string) => {
    setIsLoading(true);
    const result = await authClient.signIn.credentials({ email, password });
    if (result.user && result.token) {
      setUser({ id: Number(result.user.id), email: result.user.email });
      setToken(result.token); // store JWT token
      // Also store in localStorage immediately
      localStorage.setItem('auth-token', result.token);
    }
    setIsLoading(false);
    return result;
  };

  const register = async (email: string, password: string) => {
    setIsLoading(true);
    const result = await authClient.signUp({ email, password });
    setIsLoading(false);
    return result;
  };

  const logout = async () => {
    setIsLoading(true);
    await authClient.signOut();
    setUser(null);
    setToken(null);
    // Also remove from localStorage
    localStorage.removeItem('auth-token');
    localStorage.removeItem('user');
    setIsLoading(false);
  };

  // Optional: persist token in localStorage
  useEffect(() => {
    const savedToken = localStorage.getItem('auth-token');
    const savedUser = localStorage.getItem('user');
    if (savedToken && savedUser) {
      setToken(savedToken);
      setUser(JSON.parse(savedUser));
    }
  }, []);

  useEffect(() => {
    if (token && user) {
      localStorage.setItem('auth-token', token);
      localStorage.setItem('user', JSON.stringify(user));
    } else {
      localStorage.removeItem('auth-token');
      localStorage.removeItem('user');
    }
  }, [token, user]);

  return (
    <AuthContext.Provider
      value={{
        user,
        isLoading,
        isAuthenticated: !!user,
        token,
        login,
        register,
        logout,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) throw new Error('useAuth must be used within an AuthProvider');
  return context;
}
