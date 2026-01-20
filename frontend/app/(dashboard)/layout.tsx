'use client';

import React from 'react';
import { useAuth } from '@/providers/auth-provider';
import { useRouter } from 'next/navigation';
import { useEffect } from 'react';

export default function AppLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const { isAuthenticated, isLoading } = useAuth();
  const router = useRouter();

  // Redirect to login if not authenticated
  useEffect(() => {
    if (!isLoading && !isAuthenticated) {
      router.push('/login');
    }
  }, [isAuthenticated, isLoading, router]);

  // Show loading state while checking auth
  if (isLoading) {
    return (
      <div className="min-h-screen bg-slate-900 flex items-center justify-center">
        <div className="text-center">
          <div className="inline-block animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-indigo-600"></div>
          <p className="mt-2 text-slate-400">Loading...</p>
        </div>
      </div>
    );
  }

  // If not authenticated and not loading, redirect is handled by useEffect
  if (!isAuthenticated && !isLoading) {
    return null; // This will be handled by the redirect in useEffect
  }

  return (
    <div className="w-screen h-screen overflow-hidden bg-slate-900">
      {children}
    </div>
  );
}