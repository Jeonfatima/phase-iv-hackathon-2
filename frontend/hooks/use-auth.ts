import { useState, useEffect } from 'react';
import { useAuth } from '@/providers/auth-provider';
import { LoginFormState, RegisterFormState } from '@/lib/types';

export const useAuthState = () => {
  const { user, isLoading, isAuthenticated, login, register, logout } = useAuth();

  const [loginForm, setLoginForm] = useState<LoginFormState>({
    email: '',
    password: '',
    error: null,
    loading: false,
  });

  const [registerForm, setRegisterForm] = useState<RegisterFormState>({
    email: '',
    password: '',
    confirmPassword: '',
    error: null,
    loading: false,
  });

  const handleLogin = async () => {
    if (!loginForm.email || !loginForm.password) {
      setLoginForm(prev => ({
        ...prev,
        error: 'Email and password are required'
      }));
      return;
    }

    setLoginForm(prev => ({ ...prev, loading: true, error: null }));

    try {
      const result = await login(loginForm.email, loginForm.password);
      if (result.error) {
        setLoginForm(prev => ({
          ...prev,
          error: result.error?.message || 'Login failed',
          loading: false
        }));
      } else {
        setLoginForm(prev => ({ ...prev, loading: false }));
      }
    } catch (error: any) {
      setLoginForm(prev => ({
        ...prev,
        error: error.message || 'Login failed',
        loading: false
      }));
    }
  };

  const handleRegister = async () => {
    if (!registerForm.email || !registerForm.password) {
      setRegisterForm(prev => ({
        ...prev,
        error: 'Email and password are required',
        loading: false
      }));
      return;
    }

    if (registerForm.password !== registerForm.confirmPassword) {
      setRegisterForm(prev => ({
        ...prev,
        error: 'Passwords do not match',
        loading: false
      }));
      return;
    }

    setRegisterForm(prev => ({ ...prev, loading: true, error: null }));

    try {
      const result = await register(registerForm.email, registerForm.password);
      if (result.error) {
        setRegisterForm(prev => ({
          ...prev,
          error: result.error?.message || 'Registration failed',
          loading: false
        }));
      } else {
        setRegisterForm(prev => ({
          ...prev,
          loading: false,
          email: '',
          password: '',
          confirmPassword: '',
          error: null
        }));
        // Show success message - this will be handled in the component
        alert('Registration successful! Now go to login to continue.');
        // Optionally redirect to login page
        // window.location.href = '/login';
      }
    } catch (error: any) {
      setRegisterForm(prev => ({
        ...prev,
        error: error.message || 'Registration failed',
        loading: false
      }));
    }
  };

  return {
    user,
    isLoading,
    isAuthenticated,
    loginForm,
    registerForm,
    setLoginForm,
    setRegisterForm,
    handleLogin,
    handleRegister,
    logout: async () => {
      await logout();
    }
  };
};