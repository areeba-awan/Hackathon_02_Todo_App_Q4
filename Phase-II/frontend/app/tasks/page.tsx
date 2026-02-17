'use client';

import ProtectedRoute from '@/components/protected-route';
import MainLayout from '@/components/main-layout';
import TaskList from '@/components/task-list';
import { useAuth } from '@/lib/auth-provider';
import Link from 'next/link';

export default function TasksPage() {
  const { user } = useAuth();

  return (
    <ProtectedRoute>
      <MainLayout>
        <div className="lg:flex lg:items-center lg:justify-between mb-6">
          <div className="min-w-0 flex-1">
            <h2 className="text-2xl font-bold leading-7 bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 bg-clip-text text-transparent sm:truncate sm:text-2xl sm:tracking-tight">
              Your Tasks
            </h2>
          </div>
          <div className="mt-5 flex lg:mt-0 lg:ml-4">
            <span className="hidden sm:block ml-3">
              <Link
                href="/tasks/new"
                className="inline-flex items-center rounded-md border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 shadow-sm hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 dark:bg-gray-700 dark:border-gray-600 dark:text-gray-300 dark:hover:bg-gray-600 dark:focus:ring-offset-gray-800 transition-all duration-300 transform hover:scale-105"
              >
                <svg
                  className="-ml-1 mr-2 h-5 w-5 text-gray-500 dark:text-gray-400"
                  xmlns="http://www.w3.org/2000/svg"
                  viewBox="0 0 20 20"
                  fill="currentColor"
                  aria-hidden="true"
                >
                  <path
                    fillRule="evenodd"
                    d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z"
                    clipRule="evenodd"
                  />
                </svg>
                New Task
              </Link>
            </span>
          </div>
        </div>

        {user ? (
          <div className="bg-white shadow-xl overflow-hidden sm:rounded-lg dark:bg-gray-800">
            <ul className="divide-y divide-gray-200 dark:divide-gray-700">
              <TaskList userId={user.id} />
            </ul>
          </div>
        ) : (
          <div className="text-center py-12">
            <svg className="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
            </svg>
            <h3 className="mt-2 text-sm font-medium bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent">No user session</h3>
            <p className="mt-1 text-sm text-gray-500 dark:text-gray-300">Please sign in to view your tasks.</p>
          </div>
        )}
      </MainLayout>
    </ProtectedRoute>
  );
}