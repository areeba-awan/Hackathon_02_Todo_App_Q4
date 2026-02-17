'use client';

import ProtectedRoute from '@/components/protected-route';
import MainLayout from '@/components/main-layout';
import { useAuth } from '@/lib/auth-provider';
import Link from 'next/link';

export default function DashboardPage() {
  const { user } = useAuth();

  return (
    <ProtectedRoute>
      <MainLayout>
        <div className="bg-white overflow-hidden shadow-xl rounded-lg dark:bg-gray-800">
          <div className="px-4 py-5 sm:p-6">
            <h1 className="text-2xl font-bold bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 bg-clip-text text-transparent mb-4">
              Welcome, {user?.name || user?.email}!
            </h1>
            <p className="text-gray-600 mb-6 dark:text-gray-300">
              This is your personalized dashboard. Here you can manage your tasks and account settings.
            </p>

            <div className="grid grid-cols-1 gap-5 sm:grid-cols-2">
              <div className="bg-gradient-to-br from-blue-50 to-indigo-50 overflow-hidden shadow-lg rounded-lg dark:bg-blue-900/20 transform hover:scale-105 transition-all duration-300">
                <div className="px-4 py-5 sm:p-6">
                  <div className="flex items-center">
                    <div className="flex-shrink-0 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-md p-3">
                      <svg className="h-6 w-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                      </svg>
                    </div>
                    <div className="ml-5 w-0 flex-1">
                      <dl>
                        <dt className="text-sm font-medium text-blue-800 dark:text-blue-300 truncate">Your Tasks</dt>
                        <dd className="flex items-baseline">
                          <div className="text-2xl font-semibold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">0</div>
                        </dd>
                      </dl>
                    </div>
                  </div>
                </div>
              </div>

              <div className="bg-gradient-to-br from-green-50 to-emerald-50 overflow-hidden shadow-lg rounded-lg dark:bg-green-900/20 transform hover:scale-105 transition-all duration-300">
                <div className="px-4 py-5 sm:p-6">
                  <div className="flex items-center">
                    <div className="flex-shrink-0 bg-gradient-to-br from-green-500 to-emerald-600 rounded-md p-3">
                      <svg className="h-6 w-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                      </svg>
                    </div>
                    <div className="ml-5 w-0 flex-1">
                      <dl>
                        <dt className="text-sm font-medium text-green-800 dark:text-green-300 truncate">Completed Tasks</dt>
                        <dd className="flex items-baseline">
                          <div className="text-2xl font-semibold bg-gradient-to-r from-green-600 to-emerald-600 bg-clip-text text-transparent">0</div>
                        </dd>
                      </dl>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <div className="mt-8">
              <Link
                href="/tasks"
                className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition-all duration-300 transform hover:scale-105 dark:focus:ring-offset-gray-800"
              >
                View Tasks
              </Link>
            </div>
          </div>
        </div>
      </MainLayout>
    </ProtectedRoute>
  );
}