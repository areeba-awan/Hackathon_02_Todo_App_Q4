'use client';

import { useState } from 'react';
import { useAuth } from '@/lib/auth-provider';
import { Task } from '@/types/task';

interface TaskFormProps {
  task?: Task;
  onSave: (task: Task) => void;
  onCancel: () => void;
}

interface FormData {
  title: string;
  description: string;
  dueDate?: string;
}

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export default function TaskForm({ task, onSave, onCancel }: TaskFormProps) {
  const { token } = useAuth();
  const [formData, setFormData] = useState<FormData>({
    title: task?.title || '',
    description: task?.description || '',
    dueDate: task?.dueDate ? new Date(task.dueDate).toISOString().split('T')[0] : '',
  });
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(false);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!formData.title.trim()) {
      setError('Title is required');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      // If task exists, update it; otherwise create a new one
      const url = task
        ? `${API_URL}/api/tasks/${task.id}`
        : `${API_URL}/api/tasks`;

      const response = await fetch(url, {
        method: task ? 'PUT' : 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({
          title: formData.title,
          description: formData.description || null,
          ...(task && { completed: task.completed }),
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error?.message || 'Failed to save task');
      }

      const savedTaskData = await response.json();
      const savedTask: Task = {
        id: savedTaskData.id.toString(),
        title: savedTaskData.title,
        description: savedTaskData.description,
        completed: savedTaskData.completed,
        createdAt: new Date(savedTaskData.created_at),
        updatedAt: new Date(savedTaskData.updated_at),
        userId: savedTaskData.user_id,
      };

      onSave(savedTask);
    } catch (err: any) {
      setError(err.message || 'Failed to save task');
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      {error && (
        <div className="rounded-md bg-gradient-to-r from-red-50 to-pink-50 p-4 dark:bg-red-900/20">
          <div className="text-sm text-red-700 dark:text-red-300">{error}</div>
        </div>
      )}

      <div>
        <label htmlFor="title" className="block text-sm font-medium text-gray-700 dark:text-gray-300">
          Title *
        </label>
        <div className="mt-1">
          <input
            type="text"
            id="title"
            name="title"
            value={formData.title}
            onChange={handleChange}
            required
            className="shadow-sm focus:ring-indigo-500 focus:border-indigo-500 block w-full sm:text-sm border-gray-300 rounded-md p-2 dark:bg-gray-700 dark:border-gray-600 dark:text-white transition-all duration-300"
          />
        </div>
      </div>

      <div>
        <label htmlFor="description" className="block text-sm font-medium text-gray-700 dark:text-gray-300">
          Description
        </label>
        <div className="mt-1">
          <textarea
            id="description"
            name="description"
            rows={3}
            value={formData.description}
            onChange={handleChange}
            className="shadow-sm focus:ring-indigo-500 focus:border-indigo-500 block w-full sm:text-sm border-gray-300 rounded-md p-2 dark:bg-gray-700 dark:border-gray-600 dark:text-white transition-all duration-300"
          />
        </div>
      </div>

      <div>
        <label htmlFor="dueDate" className="block text-sm font-medium text-gray-700 dark:text-gray-300">
          Due Date
        </label>
        <div className="mt-1">
          <input
            type="date"
            id="dueDate"
            name="dueDate"
            value={formData.dueDate}
            onChange={handleChange}
            className="shadow-sm focus:ring-indigo-500 focus:border-indigo-500 block w-full sm:text-sm border-gray-300 rounded-md p-2 dark:bg-gray-700 dark:border-gray-600 dark:text-white transition-all duration-300"
          />
        </div>
      </div>

      <div className="flex space-x-3">
        <button
          type="submit"
          disabled={loading}
          className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition-all duration-300 transform hover:scale-105 disabled:opacity-50 dark:focus:ring-offset-gray-800"
        >
          {loading ? (task ? 'Updating...' : 'Creating...') : (task ? 'Update Task' : 'Create Task')}
        </button>
        <button
          type="button"
          onClick={onCancel}
          className="inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md shadow-sm text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 dark:bg-gray-700 dark:border-gray-600 dark:text-gray-300 dark:hover:bg-gray-600 dark:focus:ring-offset-gray-800 transition-all duration-300"
        >
          Cancel
        </button>
      </div>
    </form>
  );
}