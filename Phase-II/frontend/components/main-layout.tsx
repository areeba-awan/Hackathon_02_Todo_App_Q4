'use client';

import { useAuth } from '@/lib/auth-provider';
import { useTheme } from '@/lib/theme-provider';
import Link from 'next/link';
import { useState } from 'react';

export default function MainLayout({ children }: { children: React.ReactNode }) {
  const { user, logout } = useAuth();
  const { theme, toggleTheme } = useTheme();
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  const handleLogout = () => {
    logout();
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-50 via-purple-50 to-pink-50 dark:bg-gray-900">
      {/* Modern Gradient Navbar */}
      <nav className="relative bg-gradient-to-r from-violet-600 via-fuchsia-600 to-rose-600 shadow-2xl">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-20">
            {/* Logo Section */}
            <div className="flex items-center space-x-4">
              <Link href="/" className="group">
                <div className="w-12 h-12 bg-white/20 backdrop-blur-sm rounded-2xl flex items-center justify-center transform group-hover:rotate-12 group-hover:scale-110 transition-all duration-300 shadow-xl border border-white/30">
                  <svg className="w-7 h-7 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M5 13l4 4L19 7" />
                  </svg>
                </div>
              </Link>
              <div>
                <Link href="/" className="text-2xl font-bold text-white drop-shadow-lg">
                  Todo App
                </Link>
                <p className="text-xs text-white/70 -mt-1">Organize Your Life</p>
              </div>
            </div>

            {/* Desktop Navigation */}
            <div className="hidden md:flex items-center space-x-2">
              <Link
                href="/dashboard"
                className="group flex items-center px-4 py-2.5 rounded-xl text-sm font-medium text-white/90 hover:text-white hover:bg-white/20 backdrop-blur-sm transition-all duration-300"
              >
                <svg className="w-5 h-5 mr-2 group-hover:scale-110 transition-transform duration-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
                </svg>
                Dashboard
              </Link>
              <Link
                href="/tasks"
                className="group flex items-center px-4 py-2.5 rounded-xl text-sm font-medium text-white/90 hover:text-white hover:bg-white/20 backdrop-blur-sm transition-all duration-300"
              >
                <svg className="w-5 h-5 mr-2 group-hover:scale-110 transition-transform duration-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                </svg>
                Tasks
              </Link>
              <Link
                href="/tasks/new"
                className="group flex items-center px-4 py-2.5 rounded-xl text-sm font-medium text-white/90 hover:text-white hover:bg-white/20 backdrop-blur-sm transition-all duration-300"
              >
                <svg className="w-5 h-5 mr-2 group-hover:scale-110 transition-transform duration-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
                </svg>
                New Task
              </Link>
            </div>

            {/* Right Side Actions */}
            <div className="flex items-center space-x-3">
              {/* Theme Toggle */}
              <button
                onClick={toggleTheme}
                className="p-2.5 rounded-xl bg-white/20 backdrop-blur-sm hover:bg-white/30 transition-all duration-300 transform hover:scale-110 border border-white/30"
                aria-label="Toggle theme"
              >
                <span className="text-xl">{theme === 'light' ? '🌙' : '☀️'}</span>
              </button>

              {user ? (
                <>
                  <div className="hidden lg:flex items-center px-4 py-2 rounded-xl bg-white/10 backdrop-blur-sm border border-white/20">
                    <div className="w-8 h-8 bg-gradient-to-br from-amber-400 to-orange-500 rounded-full flex items-center justify-center text-white font-bold text-sm mr-3">
                      {user.name?.charAt(0) || user.email.charAt(0)}
                    </div>
                    <span className="text-sm font-medium text-white">{user.name || user.email}</span>
                  </div>
                  <button
                    onClick={handleLogout}
                    className="group flex items-center px-4 py-2.5 border border-white/40 text-sm font-medium rounded-xl text-white bg-white/10 backdrop-blur-sm hover:bg-white/20 focus:outline-none focus:ring-2 focus:ring-white transition-all duration-300 transform hover:scale-105"
                  >
                    <svg className="w-5 h-5 mr-2 group-hover:translate-x-1 transition-transform duration-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                    </svg>
                    Logout
                  </button>
                </>
              ) : (
                <Link
                  href="/login"
                  className="group flex items-center px-5 py-2.5 border border-transparent text-sm font-medium rounded-xl text-violet-600 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-white transition-all duration-300 transform hover:scale-105 shadow-lg"
                >
                  Sign in
                  <svg className="w-4 h-4 ml-2 group-hover:translate-x-1 transition-transform duration-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                  </svg>
                </Link>
              )}
            </div>
          </div>
        </div>

        {/* Bottom gradient line */}
        <div className="absolute bottom-0 left-0 right-0 h-1 bg-gradient-to-r from-transparent via-white/50 to-transparent"></div>
      </nav>

      {/* Mobile menu button */}
      <div className="md:hidden">
        <button
          onClick={() => setIsMenuOpen(!isMenuOpen)}
          className="inline-flex items-center justify-center p-2 rounded-md text-gray-400 hover:text-gray-500 hover:bg-gray-100 dark:hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-indigo-500"
        >
          <span className="sr-only">Open main menu</span>
          {/* Mobile menu icon */}
          <svg
            className={`${isMenuOpen ? 'hidden' : 'block'} h-6 w-6`}
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
            aria-hidden="true"
          >
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
          </svg>
          {/* Close menu icon */}
          <svg
            className={`${isMenuOpen ? 'block' : 'hidden'} h-6 w-6`}
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
            aria-hidden="true"
          >
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>

      {/* Mobile menu */}
      {isMenuOpen && (
        <div className="md:hidden">
          <div className="pt-2 pb-3 space-y-1">
            <Link
              href="/dashboard"
              className="block pl-3 pr-4 py-2 border-l-4 border-transparent text-base font-medium text-gray-600 hover:text-gray-800 hover:bg-gray-50 hover:border-gray-300 dark:text-gray-300 dark:hover:text-gray-200 dark:hover:bg-gray-700"
            >
              Dashboard
            </Link>
            <Link
              href="/tasks"
              className="block pl-3 pr-4 py-2 border-l-4 border-transparent text-base font-medium text-gray-600 hover:text-gray-800 hover:bg-gray-50 hover:border-gray-300 dark:text-gray-300 dark:hover:text-gray-200 dark:hover:bg-gray-700"
            >
              Tasks
            </Link>
          </div>
          <div className="pt-4 pb-3 border-t border-gray-200 dark:border-gray-700">
            <div className="flex items-center px-4">
              <div className="flex-shrink-0">
                <div className="bg-gray-200 border-2 border-dashed rounded-xl w-10 h-10 dark:bg-gray-700" />
              </div>
              <div className="ml-3">
                <div className="text-base font-medium text-gray-800 dark:text-gray-200">
                  {user?.name || user?.email}
                </div>
              </div>
            </div>
            <div className="mt-3 space-y-1">
              <button
                onClick={handleLogout}
                className="block w-full text-left pl-5 pr-4 py-2 text-base font-medium text-gray-500 hover:text-gray-800 hover:bg-gray-100 dark:text-gray-400 dark:hover:text-gray-200 dark:hover:bg-gray-700"
              >
                Logout
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Main content */}
      <main>
        <div className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
          {children}
        </div>
      </main>

      {/* Ultra Modern Detailed Footer */}
      <footer className="relative bg-gradient-to-br from-gray-900 via-purple-900 to-gray-900 text-white mt-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-12">
            {/* Brand Section */}
            <div className="lg:col-span-1">
              <div className="flex items-center space-x-3 mb-6">
                <div className="w-12 h-12 bg-gradient-to-br from-violet-500 to-fuchsia-600 rounded-2xl flex items-center justify-center shadow-xl transform hover:rotate-12 transition-transform duration-300">
                  <svg className="w-7 h-7 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M5 13l4 4L19 7" />
                  </svg>
                </div>
                <span className="text-2xl font-bold">Todo App</span>
              </div>
              <p className="text-gray-300 mb-6 leading-relaxed">
                Organize your life, one task at a time. The simplest and most elegant way to manage your daily tasks and boost productivity.
              </p>
              
              {/* Social Media Links */}
              <div className="flex space-x-3">
                <a href="#" className="group w-11 h-11 bg-white/10 backdrop-blur-sm rounded-xl flex items-center justify-center hover:bg-gradient-to-br hover:from-violet-500 hover:to-fuchsia-600 transition-all duration-300 transform hover:scale-110 hover:-translate-y-1">
                  <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24"><path d="M24 4.557c-.883.392-1.832.656-2.828.775 1.017-.609 1.798-1.574 2.165-2.724-.951.564-2.005.974-3.127 1.195-.897-.957-2.178-1.555-3.594-1.555-3.179 0-5.515 2.966-4.797 6.045-4.091-.205-7.719-2.165-10.148-5.144-1.29 2.213-.669 5.108 1.523 6.574-.806-.026-1.566-.247-2.229-.616-.054 2.281 1.581 4.415 3.949 4.89-.693.188-1.452.232-2.224.084.626 1.956 2.444 3.379 4.6 3.419-2.07 1.623-4.678 2.348-7.29 2.04 2.179 1.397 4.768 2.212 7.548 2.212 9.142 0 14.307-7.721 13.995-14.646.962-.695 1.797-1.562 2.457-2.549z"/></svg>
                </a>
                <a href="#" className="group w-11 h-11 bg-white/10 backdrop-blur-sm rounded-xl flex items-center justify-center hover:bg-gradient-to-br hover:from-violet-500 hover:to-fuchsia-600 transition-all duration-300 transform hover:scale-110 hover:-translate-y-1">
                  <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24"><path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.163 6.162 6.163 6.162-2.759 6.162-6.163c0-3.403-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.79-4-4 0-2.209 1.791-4 4-4s4 1.791 4 4c0 2.21-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 1.439-.645 1.439-1.44s-.644-1.44-1.439-1.44z"/></svg>
                </a>
                <a href="#" className="group w-11 h-11 bg-white/10 backdrop-blur-sm rounded-xl flex items-center justify-center hover:bg-gradient-to-br hover:from-violet-500 hover:to-fuchsia-600 transition-all duration-300 transform hover:scale-110 hover:-translate-y-1">
                  <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24"><path d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.239 5-5v-14c0-2.761-2.238-5-5-5zm-11 19h-3v-11h3v11zm-1.5-12.268c-.966 0-1.75-.79-1.75-1.764s.784-1.764 1.75-1.764 1.75.79 1.75 1.764-.783 1.764-1.75 1.764zm13.5 12.268h-3v-5.604c0-3.368-4-3.113-4 0v5.604h-3v-11h3v1.765c1.396-2.586 7-2.777 7 2.476v6.759z"/></svg>
                </a>
                <a href="#" className="group w-11 h-11 bg-white/10 backdrop-blur-sm rounded-xl flex items-center justify-center hover:bg-gradient-to-br hover:from-violet-500 hover:to-fuchsia-600 transition-all duration-300 transform hover:scale-110 hover:-translate-y-1">
                  <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24"><path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/></svg>
                </a>
              </div>
            </div>

            {/* Quick Links */}
            <div>
              <h3 className="text-lg font-bold mb-6 flex items-center">
                <span className="w-1 h-6 bg-gradient-to-b from-violet-400 to-fuchsia-400 rounded-full mr-3"></span>
                <span className="bg-gradient-to-r from-violet-300 to-fuchsia-300 bg-clip-text text-transparent">Quick Links</span>
              </h3>
              <ul className="space-y-3">
                <li>
                  <Link href="/dashboard" className="group flex items-center text-gray-300 hover:text-white transition-all duration-300">
                    <svg className="w-4 h-4 mr-2 text-violet-400 group-hover:text-violet-300 group-hover:translate-x-1 transition-all duration-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                    </svg>
                    Dashboard
                  </Link>
                </li>
                <li>
                  <Link href="/tasks" className="group flex items-center text-gray-300 hover:text-white transition-all duration-300">
                    <svg className="w-4 h-4 mr-2 text-fuchsia-400 group-hover:text-fuchsia-300 group-hover:translate-x-1 transition-all duration-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                    </svg>
                    All Tasks
                  </Link>
                </li>
                <li>
                  <Link href="/tasks/new" className="group flex items-center text-gray-300 hover:text-white transition-all duration-300">
                    <svg className="w-4 h-4 mr-2 text-rose-400 group-hover:text-rose-300 group-hover:translate-x-1 transition-all duration-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                    </svg>
                    Create Task
                  </Link>
                </li>
                <li>
                  <Link href="/login" className="group flex items-center text-gray-300 hover:text-white transition-all duration-300">
                    <svg className="w-4 h-4 mr-2 text-amber-400 group-hover:text-amber-300 group-hover:translate-x-1 transition-all duration-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                    </svg>
                    Sign In
                  </Link>
                </li>
                <li>
                  <Link href="/register" className="group flex items-center text-gray-300 hover:text-white transition-all duration-300">
                    <svg className="w-4 h-4 mr-2 text-emerald-400 group-hover:text-emerald-300 group-hover:translate-x-1 transition-all duration-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                    </svg>
                    Register
                  </Link>
                </li>
              </ul>
            </div>

            {/* Features */}
            <div>
              <h3 className="text-lg font-bold mb-6 flex items-center">
                <span className="w-1 h-6 bg-gradient-to-b from-fuchsia-400 to-rose-400 rounded-full mr-3"></span>
                <span className="bg-gradient-to-r from-fuchsia-300 to-rose-300 bg-clip-text text-transparent">Features</span>
              </h3>
              <ul className="space-y-3">
                <li className="group flex items-start">
                  <svg className="w-5 h-5 mr-2 text-green-400 mt-0.5 group-hover:scale-110 transition-transform duration-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                  </svg>
                  <span className="text-gray-300 group-hover:text-white transition-colors duration-300">Task Management</span>
                </li>
                <li className="group flex items-start">
                  <svg className="w-5 h-5 mr-2 text-green-400 mt-0.5 group-hover:scale-110 transition-transform duration-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                  </svg>
                  <span className="text-gray-300 group-hover:text-white transition-colors duration-300">Due Date Tracking</span>
                </li>
                <li className="group flex items-start">
                  <svg className="w-5 h-5 mr-2 text-green-400 mt-0.5 group-hover:scale-110 transition-transform duration-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                  </svg>
                  <span className="text-gray-300 group-hover:text-white transition-colors duration-300">Dark Mode</span>
                </li>
                <li className="group flex items-start">
                  <svg className="w-5 h-5 mr-2 text-green-400 mt-0.5 group-hover:scale-110 transition-transform duration-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                  </svg>
                  <span className="text-gray-300 group-hover:text-white transition-colors duration-300">Secure Authentication</span>
                </li>
                <li className="group flex items-start">
                  <svg className="w-5 h-5 mr-2 text-green-400 mt-0.5 group-hover:scale-110 transition-transform duration-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                  </svg>
                  <span className="text-gray-300 group-hover:text-white transition-colors duration-300">Responsive Design</span>
                </li>
              </ul>
            </div>

            {/* Contact & Info */}
            <div>
              <h3 className="text-lg font-bold mb-6 flex items-center">
                <span className="w-1 h-6 bg-gradient-to-b from-rose-400 to-amber-400 rounded-full mr-3"></span>
                <span className="bg-gradient-to-r from-rose-300 to-amber-300 bg-clip-text text-transparent">Contact Us</span>
              </h3>
              <ul className="space-y-4">
                <li className="group flex items-center space-x-3">
                  <div className="w-10 h-10 bg-gradient-to-br from-violet-500 to-fuchsia-600 rounded-xl flex items-center justify-center group-hover:scale-110 transition-transform duration-300">
                    <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                    </svg>
                  </div>
                  <span className="text-gray-300 group-hover:text-white transition-colors duration-300">support@todoapp.com</span>
                </li>
                <li className="group flex items-center space-x-3">
                  <div className="w-10 h-10 bg-gradient-to-br from-fuchsia-500 to-rose-600 rounded-xl flex items-center justify-center group-hover:scale-110 transition-transform duration-300">
                    <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
                    </svg>
                  </div>
                  <span className="text-gray-300 group-hover:text-white transition-colors duration-300">+1 (555) 123-4567</span>
                </li>
                <li className="group flex items-center space-x-3">
                  <div className="w-10 h-10 bg-gradient-to-br from-rose-500 to-amber-600 rounded-xl flex items-center justify-center group-hover:scale-110 transition-transform duration-300">
                    <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                    </svg>
                  </div>
                  <span className="text-gray-300 group-hover:text-white transition-colors duration-300">123 Task Street, NY</span>
                </li>
              </ul>

              {/* Newsletter */}
              <div className="mt-6">
                <p className="text-sm text-gray-400 mb-3">Subscribe to our newsletter</p>
                <div className="flex">
                  <input
                    type="email"
                    placeholder="Your email"
                    className="flex-1 px-4 py-2.5 bg-white/10 backdrop-blur-sm border border-white/20 rounded-l-xl text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-violet-500"
                  />
                  <button className="px-4 py-2.5 bg-gradient-to-r from-violet-600 to-fuchsia-600 rounded-r-xl hover:from-violet-700 hover:to-fuchsia-700 transition-all duration-300 transform hover:scale-105">
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14 5l7 7m0 0l-7 7m7-7H3" />
                    </svg>
                  </button>
                </div>
              </div>
            </div>
          </div>

          {/* Bottom Bar */}
          <div className="border-t border-white/10 mt-12 pt-8">
            <div className="flex flex-col lg:flex-row justify-between items-center space-y-4 lg:space-y-0">
              <p className="text-gray-400 text-sm">
                © {new Date().getFullYear()} Todo App. Built with <span className="text-red-400">❤️</span> using Next.js & Better Auth.
              </p>
              <div className="flex flex-wrap justify-center space-x-6">
                <Link href="#" className="text-gray-400 hover:text-white text-sm transition-all duration-300 hover:underline">Privacy Policy</Link>
                <Link href="#" className="text-gray-400 hover:text-white text-sm transition-all duration-300 hover:underline">Terms of Service</Link>
                <Link href="#" className="text-gray-400 hover:text-white text-sm transition-all duration-300 hover:underline">Cookie Policy</Link>
                <Link href="#" className="text-gray-400 hover:text-white text-sm transition-all duration-300 hover:underline">Help Center</Link>
              </div>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}