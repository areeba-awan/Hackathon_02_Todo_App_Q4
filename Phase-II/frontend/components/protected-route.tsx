'use client';

import { useAuth } from '@/lib/auth-provider';
import { useRouter } from 'next/navigation';
import { useEffect, ReactNode } from 'react';

interface ProtectedRouteProps {
  children: ReactNode;
}

export default function ProtectedRoute({ children }: ProtectedRouteProps) {
  const { isAuthenticated, user } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!isAuthenticated) {
      router.push('/login');
    }
  }, [isAuthenticated, router]);

  // If not authenticated, return nothing while redirecting
  if (!isAuthenticated) {
    return null;
  }

  // If authenticated, render the children
  return <>{children}</>;
}