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
      

      {error && (
        <div className="mb-6 p-4 bg-red-900/30 text-red-300 rounded-xl text-sm border border-red-700/50">
          {typeof error === 'string' ? error : JSON.stringify(error)}
        </div>
      )}

      <form className="space-y-5" onSubmit={handleSubmit}>
        <div>
          <label htmlFor="email" className="block text-sm font-medium text-slate-300 mb-2">
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
              className="w-full px-4 py-3 rounded-lg border-slate-600/50 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/20 focus:outline-none transition-colors text-slate-100 bg-slate-800/50"
              placeholder="Enter your email"
            />
          </div>
        </div>

        <div>
          <label htmlFor="password" className="block text-sm font-medium text-slate-300 mb-2">
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
              className="w-full px-4 py-3 rounded-lg border-slate-600/50 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/20 focus:outline-none transition-colors text-slate-100 bg-slate-800/50"
              placeholder="Enter your password"
            />
          </div>
        </div>

        <div className="flex items-center justify-between text-sm">
          <label className="flex items-center text-slate-400">
            <input
              type="checkbox"
              className="rounded border-slate-600 bg-slate-700 text-indigo-500 focus:ring-indigo-500 mr-2"
            />
            Remember me
          </label>
          <a href="#" className="font-medium text-indigo-400 hover:text-indigo-300">
            Forgot password?
          </a>
        </div>

        <div>
          <Button
            type="submit"
            disabled={loading}
            className="w-full bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700 text-white rounded-lg shadow-lg hover:shadow-xl hover:scale-[1.02] transition-all duration-300 disabled:opacity-50 h-12 font-semibold"
          >
            {loading ? (
              <div className="flex items-center justify-center">
                <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin mr-2"></div>
                Signing in...
              </div>
            ) : (
              'Sign in'
            )}
          </Button>
        </div>
      </form>

      <div className="mt-8 text-center text-sm text-slate-400">
        <p>
          Don't have an account?{' '}
          <a href="/register" className="font-semibold text-indigo-400 hover:text-indigo-300 transition-colors">
            Register here
          </a>
        </p>
      </div>
    </div>
  );
};