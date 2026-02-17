'use client';

import { useAuth } from '@/lib/auth-provider';
import { useRouter } from 'next/navigation';
import { useEffect, useState, ReactNode } from 'react';

interface ProtectedRouteProps {
  children: ReactNode;
}

export default function ProtectedRoute({ children }: ProtectedRouteProps) {
  const { isAuthenticated, user } = useAuth();
  const router = useRouter();
  const [isChecking, setIsChecking] = useState(true);

  useEffect(() => {
    // Give auth context time to load from localStorage
    const timer = setTimeout(() => {
      if (!isAuthenticated) {
        router.push('/login');
      } else {
        setIsChecking(false);
      }
    }, 500);

    return () => clearTimeout(timer);
  }, [isAuthenticated, router]);

  // Show loading while checking auth
  if (isChecking || !isAuthenticated) {
    return (
      <div className="flex justify-center items-center h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-indigo-500"></div>
      </div>
    );
  }

  // If authenticated, render the children
  return <>{children}</>;
}