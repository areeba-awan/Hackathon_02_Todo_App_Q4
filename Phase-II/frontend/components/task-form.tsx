'use client';

import { useState } from 'react';
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

export default function TaskForm({ task, onSave, onCancel }: TaskFormProps) {
  const [formData, setFormData] = useState<FormData>({
    title: task?.title || '',
    description: task?.description || '',
    dueDate: task?.dueDate ? new Date(task.dueDate).toISOString().split('T')[0] : '',
  });
  const [error, setError] = useState<string | null>(null);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!formData.title.trim()) {
      setError('Title is required');
      return;
    }
    
    const newTask: Task = {
      id: task?.id || Date.now().toString(),
      title: formData.title,
      description: formData.description,
      completed: task?.completed || false,
      dueDate: formData.dueDate ? new Date(formData.dueDate) : undefined,
      createdAt: task?.createdAt || new Date(),
      updatedAt: new Date(),
      userId: task?.userId || '',
    };
    
    onSave(newTask);
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
          className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition-all duration-300 transform hover:scale-105 dark:focus:ring-offset-gray-800"
        >
          {task ? 'Update Task' : 'Create Task'}
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