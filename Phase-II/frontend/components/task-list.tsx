'use client';

import { useState, useEffect } from 'react';
import TaskItem from './task-item';
import { Task } from '@/types/task';

interface TaskListProps {
  userId: string;
}

export default function TaskList({ userId }: TaskListProps) {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchTasks();
  }, [userId]);

  const fetchTasks = async () => {
    try {
      setLoading(true);
      // This would normally call the API to fetch tasks
      // For now, we'll use mock data
      const mockTasks: Task[] = [
        {
          id: '1',
          title: 'Sample Task',
          description: 'This is a sample task to demonstrate the UI',
          completed: false,
          dueDate: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000), // 7 days from now
          createdAt: new Date(),
          updatedAt: new Date(),
          userId: userId,
        },
        {
          id: '2',
          title: 'Another Sample Task',
          description: 'This is another sample task',
          completed: true,
          dueDate: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000), // 2 days ago
          createdAt: new Date(Date.now() - 3 * 24 * 60 * 60 * 1000),
          updatedAt: new Date(Date.now() - 1 * 24 * 60 * 60 * 1000),
          userId: userId,
        },
      ];
      setTasks(mockTasks);
    } catch (err: any) {
      setError(err.message || 'Failed to fetch tasks');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-indigo-500"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="rounded-md bg-gradient-to-r from-red-50 to-pink-50 p-4 dark:bg-red-900/20">
        <div className="text-sm text-red-700 dark:text-red-300">Error: {error}</div>
      </div>
    );
  }

  if (tasks.length === 0) {
    return (
      <div className="text-center py-12">
        <svg className="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
        </svg>
        <h3 className="mt-2 text-sm font-medium bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent">No tasks</h3>
        <p className="mt-1 text-sm text-gray-500 dark:text-gray-300">Get started by creating a new task.</p>
        <div className="mt-6">
          <a
            href="/tasks/new"
            className="inline-flex items-center px-4 py-2 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition-all duration-300 transform hover:scale-105 dark:focus:ring-offset-gray-800"
          >
            Create new task
          </a>
        </div>
      </div>
    );
  }

  return (
    <ul className="divide-y divide-gray-200">
      {tasks.map((task) => (
        <TaskItem key={task.id} task={task} onUpdate={fetchTasks} />
      ))}
    </ul>
  );
}