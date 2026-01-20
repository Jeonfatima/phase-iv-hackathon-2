'use client';

import React from 'react';
import Link from 'next/link';
import { RegisterForm } from '@/components/auth/register-form';
import { useAuthState } from '@/hooks/use-auth';
import { useRouter } from 'next/navigation';

export default function RegisterPage() {
  const { handleRegister, registerForm, setRegisterForm, isAuthenticated } = useAuthState();
  const router = useRouter();

  // Redirect to dashboard if already authenticated
  React.useEffect(() => {
    if (isAuthenticated) {
      router.push('/dashboard');
    }
  }, [isAuthenticated, router]);

  const updateForm = (field: string, value: string | boolean) => {
    setRegisterForm(prev => ({
      ...prev,
      [field]: value,
    }));
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-indigo-900/40 to-slate-900">
      {/* Top Header */}
      <header className="sticky top-0 z-10 bg-slate-900/80 backdrop-blur-xl border-b border-slate-700/50 px-6 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center">
            <h1 className="text-2xl font-bold bg-gradient-to-r from-indigo-400 to-purple-400 bg-clip-text text-transparent">
              Todo App Diary
            </h1>
          </div>
          <nav className="flex items-center space-x-6">
            <a href="#features" className="text-slate-300 hover:text-white transition-colors">Features</a>
            <a href="#about" className="text-slate-300 hover:text-white transition-colors">About</a>
            <Link href="/login" className="text-slate-300 hover:text-white transition-colors">Login</Link>
            <Link href="/register" className="text-indigo-400 font-medium">Sign Up</Link>
          </nav>
        </div>
      </header>

      {/* Hero Section */}
      <section className="min-h-screen flex items-center justify-center px-4 py-12">
        <div className="text-center max-w-4xl mx-auto w-full">
          <h1 className="text-4xl sm:text-5xl md:text-6xl lg:text-7xl font-extrabold tracking-tight bg-gradient-to-r from-indigo-400 to-purple-400 bg-clip-text text-transparent mb-4 sm:mb-6">
            Welcome to Todo App Diary
          </h1>
          <p className="text-lg sm:text-xl md:text-2xl text-slate-300 font-medium mb-8 sm:mb-12 max-w-xl sm:max-w-2xl mx-auto">
            Organize tasks, automate productivity, and chat with AI — all in one place.
          </p>

          <div className="flex flex-col sm:flex-row gap-4 justify-center mb-10 sm:mb-16">
            <Link
              href="/register"
              className="px-6 sm:px-8 py-3 sm:py-4 bg-gradient-to-r from-indigo-600 to-purple-600 text-white font-semibold rounded-xl shadow-lg hover:shadow-xl transform hover:scale-105 transition-all duration-300 text-sm sm:text-base"
            >
              Get Started
            </Link>
            <Link
              href="/login"
              className="px-6 sm:px-8 py-3 sm:py-4 bg-slate-800/50 text-white font-semibold rounded-xl border border-slate-600 hover:border-slate-500 transition-all duration-300 text-sm sm:text-base"
            >
              Login
            </Link>
          </div>

          {/* Register Form Card */}
          <div className="bg-black/30 backdrop-blur-xl rounded-2xl sm:rounded-3xl shadow-2xl border border-slate-700/50 p-6 sm:p-8 w-full max-w-sm sm:max-w-md mx-auto">
            <div className="text-center mb-6 sm:mb-8">
              <h2 className="text-2xl sm:text-3xl font-bold text-white mb-2">Create Account</h2>
              <p className="text-slate-400 text-sm sm:text-base">Join us today to boost your productivity</p>
            </div>

            <RegisterForm
              email={registerForm.email}
              password={registerForm.password}
              confirmPassword={registerForm.confirmPassword}
              error={registerForm.error}
              loading={registerForm.loading}
              onEmailChange={(value) => updateForm('email', value)}
              onPasswordChange={(value) => updateForm('password', value)}
              onConfirmPasswordChange={(value) => updateForm('confirmPassword', value)}
              onSubmit={handleRegister}
            />

            <div className="mt-6 text-center">
              <p className="text-slate-400 text-sm">
                Already have an account?{' '}
                <Link href="/login" className="text-indigo-400 hover:text-indigo-300 font-medium">
                  Sign in
                </Link>
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="py-12 sm:py-20 px-4">
        <div className="max-w-4xl sm:max-w-5xl md:max-w-6xl mx-auto">
          <h2 className="text-3xl sm:text-4xl font-bold text-center text-white mb-10 sm:mb-16">Powerful Features</h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 sm:gap-8">
            <div className="bg-slate-800/40 backdrop-blur-sm rounded-xl p-5 sm:p-6 border border-slate-700/50 hover:border-indigo-500/50 transition-all duration-300 hover:shadow-xl group">
              <div className="w-10 sm:w-12 h-10 sm:h-12 bg-gradient-to-r from-indigo-500 to-purple-500 rounded-lg flex items-center justify-center mb-3 sm:mb-4 group-hover:scale-110 transition-transform">
                <svg className="w-5 sm:w-6 h-5 sm:h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01" />
                </svg>
              </div>
              <h3 className="font-bold text-lg sm:text-xl text-white mb-2">Add Tasks</h3>
              <p className="text-slate-400 text-sm sm:text-base">Quickly create and organize your tasks with our intuitive interface.</p>
            </div>

            <div className="bg-slate-800/40 backdrop-blur-sm rounded-xl p-5 sm:p-6 border border-slate-700/50 hover:border-indigo-500/50 transition-all duration-300 hover:shadow-xl group">
              <div className="w-10 sm:w-12 h-10 sm:h-12 bg-gradient-to-r from-emerald-500 to-teal-500 rounded-lg flex items-center justify-center mb-3 sm:mb-4 group-hover:scale-110 transition-transform">
                <svg className="w-5 sm:w-6 h-5 sm:h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                </svg>
              </div>
              <h3 className="font-bold text-lg sm:text-xl text-white mb-2">Edit Tasks</h3>
              <p className="text-slate-400 text-sm sm:text-base">Modify your tasks anytime with real-time editing capabilities.</p>
            </div>

            <div className="bg-slate-800/40 backdrop-blur-sm rounded-xl p-5 sm:p-6 border border-slate-700/50 hover:border-indigo-500/50 transition-all duration-300 hover:shadow-xl group">
              <div className="w-10 sm:w-12 h-10 sm:h-12 bg-gradient-to-r from-rose-500 to-pink-500 rounded-lg flex items-center justify-center mb-3 sm:mb-4 group-hover:scale-110 transition-transform">
                <svg className="w-5 sm:w-6 h-5 sm:h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                </svg>
              </div>
              <h3 className="font-bold text-lg sm:text-xl text-white mb-2">Delete Tasks</h3>
              <p className="text-slate-400 text-sm sm:text-base">Remove completed tasks with one simple click.</p>
            </div>

            <div className="bg-slate-800/40 backdrop-blur-sm rounded-xl p-5 sm:p-6 border border-slate-700/50 hover:border-indigo-500/50 transition-all duration-300 hover:shadow-xl group">
              <div className="w-10 sm:w-12 h-10 sm:h-12 bg-gradient-to-r from-violet-500 to-purple-500 rounded-lg flex items-center justify-center mb-3 sm:mb-4 group-hover:scale-110 transition-transform">
                <svg className="w-5 sm:w-6 h-5 sm:h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
                </svg>
              </div>
              <h3 className="font-bold text-lg sm:text-xl text-white mb-2">AI Chatbot Assistant</h3>
              <p className="text-slate-400 text-sm sm:text-base">Get intelligent help with your tasks through our AI assistant.</p>
            </div>

            <div className="bg-slate-800/40 backdrop-blur-sm rounded-xl p-5 sm:p-6 border border-slate-700/50 hover:border-indigo-500/50 transition-all duration-300 hover:shadow-xl group">
              <div className="w-10 sm:w-12 h-10 sm:h-12 bg-gradient-to-r from-blue-500 to-indigo-500 rounded-lg flex items-center justify-center mb-3 sm:mb-4 group-hover:scale-110 transition-transform">
                <svg className="w-5 sm:w-6 h-5 sm:h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
              </div>
              <h3 className="font-bold text-lg sm:text-xl text-white mb-2">Smart Insights</h3>
              <p className="text-slate-400 text-sm sm:text-base">Receive productivity insights and recommendations.</p>
            </div>

            <div className="bg-slate-800/40 backdrop-blur-sm rounded-xl p-5 sm:p-6 border border-slate-700/50 hover:border-indigo-500/50 transition-all duration-300 hover:shadow-xl group">
              <div className="w-10 sm:w-12 h-10 sm:h-12 bg-gradient-to-r from-cyan-500 to-blue-500 rounded-lg flex items-center justify-center mb-3 sm:mb-4 group-hover:scale-110 transition-transform">
                <svg className="w-5 sm:w-6 h-5 sm:h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <h3 className="font-bold text-lg sm:text-xl text-white mb-2">Real-time Sync</h3>
              <p className="text-slate-400 text-sm sm:text-base">Access your tasks from anywhere, always up-to-date.</p>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-slate-900/80 backdrop-blur-lg border-t border-slate-700/50 py-6 px-4">
        <div className="max-w-4xl sm:max-w-5xl md:max-w-6xl mx-auto">
          <div className="flex flex-col sm:flex-row items-center justify-between gap-4 text-xs sm:text-sm">
            <div className="text-slate-400">
              © {new Date().getFullYear()} Todo App Diary. All rights reserved. Made by Fatima Salman (Roll# 464666)
            </div>
            <div className="flex flex-wrap justify-center gap-4 sm:gap-6">
              <a href="#" className="text-slate-400 hover:text-white transition-colors">Privacy</a>
              <a href="#" className="text-slate-400 hover:text-white transition-colors">Terms</a>
              <a href="#" className="text-slate-400 hover:text-white transition-colors">Contact</a>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}