'use client';

import AuthLayout from '@/components/auth-layout';
import RegisterForm from '@/components/register-form';
import Link from 'next/link';

export default function RegisterPage() {
  return (
    <AuthLayout>
      <div>
        <h2 className="mt-6 text-center text-3xl font-extrabold bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 bg-clip-text text-transparent">
          Create a new account
        </h2>
        <p className="mt-2 text-center text-sm text-gray-600 dark:text-gray-300">
          Or{' '}
          <Link
            href="/login"
            className="font-medium bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent hover:from-indigo-700 hover:to-purple-700"
          >
            sign in to your existing account
          </Link>
        </p>
      </div>
      <RegisterForm />
    </AuthLayout>
  );
}