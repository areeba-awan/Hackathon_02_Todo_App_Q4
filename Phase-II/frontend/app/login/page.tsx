'use client';

import AuthLayout from '@/components/auth-layout';
import LoginForm from '@/components/login-form';
import Link from 'next/link';

export default function LoginPage() {
  return (
    <AuthLayout>
      <div>
        <h2 className="mt-6 text-center text-3xl font-extrabold bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 bg-clip-text text-transparent">
          Sign in to your account
        </h2>
        <p className="mt-2 text-center text-sm text-gray-600 dark:text-gray-300">
          Or{' '}
          <Link
            href="/register"
            className="font-medium bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent hover:from-indigo-700 hover:to-purple-700"
          >
            create a new account
          </Link>
        </p>
      </div>
      <LoginForm />
    </AuthLayout>
  );
}