import React from 'react';
import { Button } from '../ui/button';
import { Input } from '../ui/input';

interface RegisterFormProps {
  email: string;
  password: string;
  confirmPassword: string;
  error?: string | null;
  loading: boolean;
  onEmailChange: (value: string) => void;
  onPasswordChange: (value: string) => void;
  onConfirmPasswordChange: (value: string) => void;
  onSubmit: () => void;
}

export const RegisterForm: React.FC<RegisterFormProps> = ({
  email,
  password,
  confirmPassword,
  error,
  loading,
  onEmailChange,
  onPasswordChange,
  onConfirmPasswordChange,
  onSubmit,
}) => {
  const [successMessage, setSuccessMessage] = React.useState<string | null>(null);
  const [showPassword, setShowPassword] = React.useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = React.useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setSuccessMessage(null); // Clear success message when submitting again
    onSubmit();
  };

  // Clear error and success when user starts typing
  const handleInputChange = (callback: (value: string) => void) => (e: React.ChangeEvent<HTMLInputElement>) => {
    callback(e.target.value);
    if (error || successMessage) {
      setSuccessMessage(null);
    }
  };

  return (
    <div>
      <div className="text-center mb-6">
        <h2 className="text-xl font-bold text-gray-900">Create a new account</h2>
      </div>

      {error && (
        <div className="mb-4 p-3 bg-[#FFD8DF] text-[#FF5C6C] rounded-xl text-sm">
          {typeof error === 'string' ? error : JSON.stringify(error)}
        </div>
      )}

      {successMessage && (
        <div className="mb-4 p-3 bg-[#F0FFDF] text-[#A8DF8E] text-sm rounded-xl">
          {successMessage}
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
              onChange={handleInputChange(onEmailChange)}
              className="w-full p-3 rounded-xl border-gray-300 focus:border-[#A8DF8E] focus:ring-[#A8DF8E] sm:text-sm text-gray-900"
              placeholder="Enter your email"
            />
          </div>
        </div>

        <div>
          <label htmlFor="password" className="block text-sm font-medium text-gray-700 mb-2">
            Password
          </label>
          <div className="mt-1 relative">
            <Input
              id="password"
              name="password"
              type={showPassword ? "text" : "password"}
              autoComplete="new-password"
              required
              value={password}
              onChange={handleInputChange(onPasswordChange)}
              className="w-full p-3 pr-10 rounded-xl border-gray-300 focus:border-[#A8DF8E] focus:ring-[#A8DF8E] sm:text-sm text-gray-900"
              placeholder="Enter your password"
            />
            <button
              type="button"
              onClick={() => setShowPassword(!showPassword)}
              className="absolute inset-y-0 right-0 pr-3 flex items-center text-gray-400 hover:text-gray-500"
            >
              {showPassword ? 'Hide' : 'Show'}
            </button>
          </div>
        </div>

        <div>
          <label htmlFor="confirmPassword" className="block text-sm font-medium text-gray-700 mb-2">
            Confirm Password
          </label>
          <div className="mt-1 relative">
            <Input
              id="confirmPassword"
              name="confirmPassword"
              type={showConfirmPassword ? "text" : "password"}
              autoComplete="new-password"
              required
              value={confirmPassword}
              onChange={handleInputChange(onConfirmPasswordChange)}
              className="w-full p-3 pr-10 rounded-xl border-gray-300 focus:border-[#A8DF8E] focus:ring-[#A8DF8E] sm:text-sm text-gray-900"
              placeholder="Confirm your password"
            />
            <button
              type="button"
              onClick={() => setShowConfirmPassword(!showConfirmPassword)}
              className="absolute inset-y-0 right-0 pr-3 flex items-center text-gray-400 hover:text-gray-500"
            >
              {showConfirmPassword ? 'Hide' : 'Show'}
            </button>
          </div>
        </div>

        <div>
          <Button
            type="submit"
            disabled={loading}
            className="w-full bg-[#A8DF8E] hover:bg-[#97ce7e] text-white rounded-xl shadow-sm hover:scale-[1.02] transition-transform disabled:opacity-50"
          >
            {loading ? 'Creating account...' : 'Create Account'}
          </Button>
        </div>
      </form>

      <div className="mt-6 text-center text-sm text-gray-600">
        <p>
          Already have an account?{' '}
          <a href="/login" className="font-medium text-[#A8DF8E] hover:text-[#8bc47a]">
            Sign in here
          </a>
        </p>
      </div>
    </div>
  );
};