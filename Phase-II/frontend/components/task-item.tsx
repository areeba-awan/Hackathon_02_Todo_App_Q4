import { useState } from 'react';
import { Task } from '@/types/task';
import { useAuth } from '@/lib/auth-provider';
import Link from 'next/link';

interface TaskItemProps {
  task: Task;
  onUpdate: () => void;
}

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export default function TaskItem({ task, onUpdate }: TaskItemProps) {
  const { token } = useAuth();
  const [loading, setLoading] = useState(false);

  const handleToggle = async () => {
    setLoading(true);
    try {
      const response = await fetch(`${API_URL}/api/tasks/${task.id}/complete`, {
        method: 'PATCH',
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error?.message || 'Failed to update task');
      }

      onUpdate();
    } catch (err: any) {
      console.error('Failed to toggle task:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async () => {
    if (!confirm('Are you sure you want to delete this task?')) return;

    setLoading(true);
    try {
      const response = await fetch(`${API_URL}/api/tasks/${task.id}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error?.message || 'Failed to delete task');
      }

      onUpdate();
    } catch (err: any) {
      console.error('Failed to delete task:', err);
    } finally {
      setLoading(false);
    }
  };

  const formatDate = (date: Date) => {
    return new Intl.DateTimeFormat('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
    }).format(date);
  };

  return (
    <li className="py-4 hover:bg-gradient-to-r hover:from-indigo-50 hover:to-purple-50 dark:hover:from-gray-700 dark:hover:to-gray-600 transition-all duration-300">
      <div className="flex items-center">
        <input
          id={`task-${task.id}`}
          name={`task-${task.id}`}
          type="checkbox"
          checked={task.completed}
          onChange={handleToggle}
          disabled={loading}
          className="h-4 w-4 text-indigo-600 border-gray-300 rounded focus:ring-indigo-500 dark:border-gray-600 transition-all duration-300 disabled:opacity-50"
        />
        <label htmlFor={`task-${task.id}`} className="ml-3 block">
          <div className="flex justify-between">
            <p className={`text-sm font-medium ${task.completed ? 'line-through text-gray-500 dark:text-gray-400' : 'bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent'}`}>
              {task.title}
            </p>
          </div>
          {task.description && (
            <p className={`mt-1 text-sm ${task.completed ? 'text-gray-500 dark:text-gray-400' : 'text-gray-700 dark:text-gray-300'}`}>
              {task.description}
            </p>
          )}
        </label>
        <div className="ml-auto flex space-x-2">
          <Link
            href={`/tasks/${task.id}/edit`}
            className="inline-flex items-center px-2.5 py-0.5 border border-transparent text-xs font-medium rounded text-indigo-700 bg-gradient-to-r from-indigo-100 to-purple-100 hover:from-indigo-200 hover:to-purple-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 dark:text-indigo-300 dark:from-indigo-900/30 dark:to-purple-900/30 dark:hover:from-indigo-900/50 dark:hover:to-purple-900/50 dark:focus:ring-offset-gray-800 transition-all duration-300 transform hover:scale-105"
          >
            Edit
          </Link>
          <button
            onClick={handleDelete}
            disabled={loading}
            className="inline-flex items-center px-2.5 py-0.5 border border-transparent text-xs font-medium rounded text-red-700 bg-gradient-to-r from-red-100 to-rose-100 hover:from-red-200 hover:to-rose-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 disabled:opacity-50 dark:text-red-300 dark:from-red-900/30 dark:to-rose-900/30 dark:hover:from-red-900/50 dark:hover:to-rose-900/50 dark:focus:ring-offset-gray-800 transition-all duration-300 transform hover:scale-105"
          >
            Delete
          </button>
        </div>
      </div>
    </li>
  );
}