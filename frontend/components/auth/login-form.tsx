import React from 'react';
import { Button } from '../ui/button';
import { Input } from '../ui/input';

interface LoginFormProps {
  email: string;
  password: string;
  error?: string | null;
  loading: boolean;
  onEmailChange: (value: string) => void;
  onPasswordChange: (value: string) => void;
  onSubmit: () => void;
}

export const LoginForm: React.FC<LoginFormProps> = ({
  email,
  password,
  error,
  loading,
  onEmailChange,
  onPasswordChange,
  onSubmit,
}) => {
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit();
  };

  return (
    <div>
      <div className="text-center mb-6">
        <h2 className="text-xl font-bold text-gray-900">Sign in to your account</h2>
      </div>

      {error && (
        <div className="mb-4 p-3 bg-[#FFD8DF] text-[#FF5C6C] rounded-xl text-sm">
          {typeof error === 'string' ? error : JSON.stringify(error)}
        </div>
      )}

      <form className="space-y-6" onSubmit={handleSubmit}>
        <div>
          <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-2">
            Email address
          </label>
          <div className="mt-1">
            <Input
              id="email"
              name="email"
              type="email"
              autoComplete="email"
              required
              value={email}
              onChange={(e) => onEmailChange(e.target.value)}
              className="w-full p-3 rounded-xl border-gray-300 focus:border-[#A8DF8E] focus:ring-[#A8DF8E] sm:text-sm text-gray-900"
            />
          </div>
        </div>

        <div>
          <label htmlFor="password" className="block text-sm font-medium text-gray-700 mb-2">
            Password
          </label>
          <div className="mt-1">
            <Input
              id="password"
              name="password"
              type="password"
              autoComplete="current-password"
              required
              value={password}
              onChange={(e) => onPasswordChange(e.target.value)}
              className="w-full p-3 rounded-xl border-gray-300 focus:border-[#A8DF8E] focus:ring-[#A8DF8E] sm:text-sm text-gray-900"
            />
          </div>
        </div>

        <div>
          <Button
            type="submit"
            disabled={loading}
            className="w-full bg-[#A8DF8E] hover:bg-[#97ce7e] text-white rounded-xl shadow-sm hover:scale-[1.02] transition-transform disabled:opacity-50"
          >
            {loading ? 'Signing in...' : 'Sign in'}
          </Button>
        </div>
      </form>

      <div className="mt-6 text-center text-sm text-gray-600">
        <p>
          Don't have an account?{' '}
          <a href="/register" className="font-medium text-[#A8DF8E] hover:text-[#8bc47a]">
            Register here
          </a>
        </p>
      </div>
    </div>
  );
};