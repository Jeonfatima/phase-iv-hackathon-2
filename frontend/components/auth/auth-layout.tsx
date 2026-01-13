import React from 'react';
import Link from 'next/link';

interface AuthLayoutProps {
  children: React.ReactNode;
}

export const AuthLayout: React.FC<AuthLayoutProps> = ({ children }) => {
  return (
    <>
      {/* Header */}
      <div className="bg-[#A8DF8E] text-white p-6 rounded-t-2xl rounded-b-lg">
        <div className="text-center">
          <h2 className="text-2xl font-bold">Todo App Diary</h2>
          <p className="mt-1 text-sm opacity-90">
            Sign in to your account or create a new one
          </p>
        </div>
      </div>

      {/* Main Content */}
      <div className="p-6 bg-[#FFF0F5] min-h-screen">
        <div className="max-w-md mx-auto mt-8">
          <div className="bg-white py-8 px-6 shadow-md rounded-xl border border-gray-100">
            {children}
            <div className="mt-6 text-center">
              <Link
                href="/login"
                className="text-sm font-medium text-[#A8DF8E] hover:text-[#8bc47a]"
              >
                Login
              </Link>
              <span className="mx-2 text-gray-400">|</span>
              <Link
                href="/register"
                className="text-sm font-medium text-[#A8DF8E] hover:text-[#8bc47a]"
              >
                Register
              </Link>
            </div>
          </div>
        </div>
      </div>
    </>
  );
};