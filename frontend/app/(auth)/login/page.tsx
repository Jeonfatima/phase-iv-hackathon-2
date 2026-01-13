'use client';

import React from 'react';
import { LoginForm } from '@/components/auth/login-form';
import { useAuthState } from '@/hooks/use-auth';
import { useRouter } from 'next/navigation';

export default function LoginPage() {
  const { handleLogin, loginForm, setLoginForm, isAuthenticated } = useAuthState();
  const router = useRouter();

  // Redirect to dashboard if already authenticated
  React.useEffect(() => {
    if (isAuthenticated) {
      router.push('/dashboard');
    }
  }, [isAuthenticated, router]);

  const updateForm = (field: string, value: string | boolean) => {
    setLoginForm(prev => ({
      ...prev,
      [field]: value,
    }));
  };

  return (
    <div>
      <LoginForm
        email={loginForm.email}
        password={loginForm.password}
        error={loginForm.error}
        loading={loginForm.loading}
        onEmailChange={(value) => updateForm('email', value)}
        onPasswordChange={(value) => updateForm('password', value)}
        onSubmit={handleLogin}
      />
    </div>
  );
}