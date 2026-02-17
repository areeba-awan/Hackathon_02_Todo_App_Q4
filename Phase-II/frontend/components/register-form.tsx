'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/lib/auth-provider';

interface FormData {
  email: string;
  password: string;
  name: string;
}

export default function RegisterForm() {
  const [formData, setFormData] = useState<FormData>({ email: '', password: '', name: '' });
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  
  const router = useRouter();
  const { register } = useAuth();

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setLoading(true);

    try {
      await register(formData.email, formData.password, formData.name);
      // Redirect happens in the register function
    } catch (err: any) {
      setError(err.message || 'Registration failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      {error && (
        <div className="rounded-md bg-red-50 p-4 dark:bg-red-900/20">
          <div className="text-sm text-red-700 dark:text-red-300">{error}</div>
        </div>
      )}

      <div>
        <label htmlFor="name" className="block text-sm font-medium text-gray-700 dark:text-gray-300">
          Full Name
        </label>
        <div className="mt-1">
          <input
            id="name"
            name="name"
            type="text"
            autoComplete="name"
            required
            value={formData.name}
            onChange={handleChange}
            className="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm dark:bg-gray-700 dark:border-gray-600 dark:text-white dark:placeholder-gray-400"
          />
        </div>
      </div>

      <div>
        <label htmlFor="email" className="block text-sm font-medium text-gray-700 dark:text-gray-300">
          Email address
        </label>
        <div className="mt-1">
          <input
            id="email"
            name="email"
            type="email"
            autoComplete="email"
            required
            value={formData.email}
            onChange={handleChange}
            className="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm dark:bg-gray-700 dark:border-gray-600 dark:text-white dark:placeholder-gray-400"
          />
        </div>
      </div>

      <div>
        <label htmlFor="password" className="block text-sm font-medium text-gray-700 dark:text-gray-300">
          Password
        </label>
        <div className="mt-1">
          <input
            id="password"
            name="password"
            type="password"
            autoComplete="new-password"
            required
            value={formData.password}
            onChange={handleChange}
            className="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm dark:bg-gray-700 dark:border-gray-600 dark:text-white dark:placeholder-gray-400"
          />
        </div>
      </div>

      <div>
        <button
          type="submit"
          disabled={loading}
          className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50 dark:focus:ring-offset-gray-800"
        >
          {loading ? 'Creating account...' : 'Create account'}
        </button>
      </div>
    </form>
  );
}