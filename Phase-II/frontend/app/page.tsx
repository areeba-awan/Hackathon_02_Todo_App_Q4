'use client';

import Link from 'next/link';
import { useEffect } from 'react';
import { useTheme } from '@/lib/theme-provider';

export default function HomePage() {
  const { theme, toggleTheme } = useTheme();

  useEffect(() => {
    // Auth check can be added here when auth context is ready
  }, []);

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-100 via-purple-50 to-pink-100 dark:from-gray-800 dark:via-gray-900 dark:to-black">
      {/* Header */}
      <header className="border-b border-gray-200 bg-white dark:border-gray-700 dark:bg-gray-900 shadow-lg">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            <div className="flex items-center space-x-2">
              <div className="w-8 h-8 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-lg flex items-center justify-center transform hover:rotate-12 transition-transform duration-300">
                <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                </svg>
              </div>
              <span className="text-xl font-bold bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent dark:from-indigo-400 dark:to-purple-400">Todo App</span>
            </div>
            <nav className="flex items-center space-x-4">
              <button
                onClick={toggleTheme}
                className="p-2 rounded-lg bg-gradient-to-r from-indigo-100 to-purple-100 hover:from-indigo-200 hover:to-purple-200 dark:from-gray-700 dark:to-gray-600 dark:hover:from-gray-600 dark:hover:to-gray-500 transition-all duration-300 transform hover:scale-110"
                aria-label="Toggle theme"
              >
                {theme === 'light' ? '🌙' : '🌞'}
              </button>
              <Link
                href="/login"
                className="text-sm font-medium text-gray-700 hover:text-indigo-600 transition-colors duration-300 dark:text-gray-300 dark:hover:text-indigo-400"
              >
                Sign In
              </Link>
              <Link
                href="/register"
                className="text-sm font-medium text-white bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700 px-4 py-2 rounded-lg transition-all duration-300 transform hover:scale-105 shadow-lg hover:shadow-xl"
              >
                Get Started
              </Link>
            </nav>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16 sm:py-24">
        <div className="text-center">
          <h1 className="text-4xl sm:text-5xl lg:text-6xl font-extrabold tracking-tight animate-pulse">
            <span className="bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 bg-clip-text text-transparent dark:from-green-600 dark:via-green-500 dark:to-green-400">Organize Your Life,</span>
            <br />
            <span className="bg-gradient-to-r from-pink-600 via-purple-600 to-indigo-600 bg-clip-text text-transparent dark:from-green-500 dark:via-green-400 dark:to-green-600">One Task at a Time</span>
          </h1>
          <p className="mt-6 text-lg sm:text-xl text-gray-600 dark:text-gray-300 max-w-2xl mx-auto">
            A simple, elegant way to manage your tasks. Stay productive,
            achieve your goals, and never forget what matters most.
          </p>

          {/* CTA Buttons */}
          <div className="mt-10 flex flex-col sm:flex-row gap-4 justify-center">
            <Link
              href="/register"
              className="inline-flex items-center justify-center px-8 py-3 text-base font-medium text-white bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700 rounded-lg shadow-lg hover:shadow-xl transition-all duration-300 transform hover:-translate-y-1 hover:scale-105"
            >
              Create Free Account
              <svg className="ml-2 w-5 h-5 animate-bounce" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
              </svg>
            </Link>
            <Link
              href="/login"
              className="inline-flex items-center justify-center px-8 py-3 text-base font-medium text-gray-700 bg-white hover:bg-gray-50 border border-gray-300 rounded-lg shadow-sm transition-all duration-300 transform hover:-translate-y-1 dark:bg-gray-700 dark:text-gray-200 dark:border-gray-600 dark:hover:bg-gray-600"
            >
              Sign In to Existing Account
            </Link>
          </div>
        </div>

        {/* Features Section */}
        <div className="mt-24 grid grid-cols-1 gap-8 sm:grid-cols-2 lg:grid-cols-3">
          {/* Feature 1 */}
          <div className="bg-white rounded-xl p-6 shadow-lg border border-gray-100 hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-2 dark:bg-gray-800 dark:border-gray-700">
            <div className="w-12 h-12 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-lg flex items-center justify-center mb-4 transform hover:rotate-12 transition-transform duration-300">
              <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
              </svg>
            </div>
            <h3 className="text-lg font-semibold bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent">Quick Task Creation</h3>
            <p className="mt-2 text-gray-600 dark:text-gray-300">
              Add tasks in seconds with our intuitive interface. Capture ideas before they slip away.
            </p>
          </div>

          {/* Feature 2 */}
          <div className="bg-white rounded-xl p-6 shadow-lg border border-gray-100 hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-2 dark:bg-gray-800 dark:border-gray-700">
            <div className="w-12 h-12 bg-gradient-to-br from-purple-500 to-pink-600 rounded-lg flex items-center justify-center mb-4 transform hover:rotate-12 transition-transform duration-300">
              <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <h3 className="text-lg font-semibold bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent">Track Progress</h3>
            <p className="mt-2 text-gray-600 dark:text-gray-300">
              Mark tasks as complete and watch your productivity grow. Visual feedback keeps you motivated.
            </p>
          </div>

          {/* Feature 3 */}
          <div className="bg-white rounded-xl p-6 shadow-lg border border-gray-100 hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-2 dark:bg-gray-800 dark:border-gray-700">
            <div className="w-12 h-12 bg-gradient-to-br from-green-500 to-teal-600 rounded-lg flex items-center justify-center mb-4 transform hover:rotate-12 transition-transform duration-300">
              <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
              </svg>
            </div>
            <h3 className="text-lg font-semibold bg-gradient-to-r from-green-600 to-teal-600 bg-clip-text text-transparent">Secure & Private</h3>
            <p className="mt-2 text-gray-600 dark:text-gray-300">
              Your tasks are yours alone. Secure authentication ensures your data stays private.
            </p>
          </div>
        </div>

        {/* How It Works */}
        <div className="mt-24">
          <div className="text-center mb-12">
            <h2 className="text-2xl sm:text-3xl font-bold bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 bg-clip-text text-transparent">How It Works</h2>
            <p className="mt-4 text-gray-600 dark:text-gray-300">Get started in three simple steps</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {/* Step 1 */}
            <div className="relative">
              <div className="text-center">
                <div className="w-16 h-16 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-full flex items-center justify-center mx-auto transform hover:scale-110 transition-transform duration-300 shadow-lg">
                  <span className="text-2xl font-bold text-white">1</span>
                </div>
                <h3 className="mt-4 text-lg font-semibold text-gray-900 dark:text-white">Create Account</h3>
                <p className="mt-2 text-gray-600 dark:text-gray-300">
                  Sign up for free in less than a minute
                </p>
              </div>
            </div>

            {/* Step 2 */}
            <div className="relative">
              <div className="hidden md:block absolute top-8 left-0 right-0">
                <div className="border-t-2 border-dashed border-gray-300 dark:border-gray-600"></div>
              </div>
              <div className="text-center">
                <div className="w-16 h-16 bg-gradient-to-br from-purple-500 to-pink-600 rounded-full flex items-center justify-center mx-auto transform hover:scale-110 transition-transform duration-300 shadow-lg">
                  <span className="text-2xl font-bold text-white">2</span>
                </div>
                <h3 className="mt-4 text-lg font-semibold text-gray-900 dark:text-white">Add Your Tasks</h3>
                <p className="mt-2 text-gray-600 dark:text-gray-300">
                  Create and organize your todo list
                </p>
              </div>
            </div>

            {/* Step 3 */}
            <div className="relative">
              <div className="hidden md:block absolute top-8 left-0 right-0">
                <div className="border-t-2 border-dashed border-gray-300 dark:border-gray-600"></div>
              </div>
              <div className="text-center">
                <div className="w-16 h-16 bg-gradient-to-br from-pink-500 to-rose-600 rounded-full flex items-center justify-center mx-auto transform hover:scale-110 transition-transform duration-300 shadow-lg">
                  <span className="text-2xl font-bold text-white">3</span>
                </div>
                <h3 className="mt-4 text-lg font-semibold text-gray-900 dark:text-white">Start Achieving</h3>
                <p className="mt-2 text-gray-600 dark:text-gray-300">
                  Complete tasks and boost productivity
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* Final CTA */}
        <div className="mt-24 bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 rounded-2xl p-8 sm:p-12 text-center shadow-xl transform hover:scale-105 transition-transform duration-300">
          <h2 className="text-2xl sm:text-3xl font-bold text-white">
            Ready to Get More Done?
          </h2>
          <p className="mt-4 text-indigo-100 max-w-xl mx-auto">
            Join thousands of users who organize their daily tasks with our simple yet powerful todo app.
          </p>
          <div className="mt-8">
            <Link
              href="/register"
              className="inline-flex items-center justify-center px-8 py-3 text-base font-medium text-indigo-600 bg-white hover:bg-gray-50 rounded-lg shadow-lg transition-all transform hover:-translate-y-1 hover:scale-105"
            >
              Get Started for Free
            </Link>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="border-t border-gray-200 bg-white mt-24 dark:border-gray-700 dark:bg-gray-900 shadow-lg">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="flex flex-col md:flex-row justify-between items-center">
            <div className="flex items-center space-x-2 mb-4 md:mb-0">
              <div className="w-6 h-6 bg-gradient-to-br from-indigo-500 to-purple-600 rounded flex items-center justify-center">
                <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                </svg>
              </div>
              <span className="text-sm font-semibold bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent dark:from-indigo-400 dark:to-purple-400">Todo App</span>
            </div>
            <p className="text-sm text-gray-500 dark:text-gray-400">
              © 2026 Todo App. Built with Next.js & Better Auth.
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
}