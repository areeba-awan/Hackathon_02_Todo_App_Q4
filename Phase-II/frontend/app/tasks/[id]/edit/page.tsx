'use client';

import { useEffect, useState } from 'react';
import ProtectedRoute from '@/components/protected-route';
import MainLayout from '@/components/main-layout';
import TaskForm from '@/components/task-form';
import { Task } from '@/types/task';
import { useRouter, useParams } from 'next/navigation';
import { useAuth } from '@/lib/auth-provider';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export default function EditTaskPage() {
  const router = useRouter();
  const params = useParams();
  const { token } = useAuth();
  const [task, setTask] = useState<Task | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const taskId = params?.id as string;

  useEffect(() => {
    const fetchTask = async () => {
      try {
        const response = await fetch(`${API_URL}/api/tasks/${taskId}`, {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
        });

        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.error?.message || 'Failed to fetch task');
        }

        const data = await response.json();
        const fetchedTask: Task = {
          id: data.id.toString(),
          title: data.title,
          description: data.description,
          completed: data.completed,
          createdAt: new Date(data.created_at),
          updatedAt: new Date(data.updated_at),
          userId: data.user_id,
        };
        setTask(fetchedTask);
      } catch (err: any) {
        setError(err.message || 'Failed to fetch task');
      } finally {
        setLoading(false);
      }
    };

    if (taskId) {
      fetchTask();
    }
  }, [taskId, token]);

  const handleSave = (updatedTask: Task) => {
    router.push('/tasks');
  };

  const handleCancel = () => {
    router.push('/tasks');
  };

  if (loading) {
    return (
      <ProtectedRoute>
        <MainLayout>
          <div className="flex justify-center items-center h-64">
            <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-indigo-500"></div>
          </div>
        </MainLayout>
      </ProtectedRoute>
    );
  }

  if (error || !task) {
    return (
      <ProtectedRoute>
        <MainLayout>
          <div className="bg-white shadow-xl sm:rounded-lg p-6 dark:bg-gray-800">
            <div className="rounded-md bg-red-50 p-4 dark:bg-red-900/20">
              <div className="text-sm text-red-700 dark:text-red-300">Error: {error || 'Task not found'}</div>
            </div>
          </div>
        </MainLayout>
      </ProtectedRoute>
    );
  }

  return (
    <ProtectedRoute>
      <MainLayout>
        <div className="bg-white shadow-xl sm:rounded-lg p-6 dark:bg-gray-800">
          <h1 className="text-2xl font-bold bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 bg-clip-text text-transparent mb-6">Edit Task</h1>
          <TaskForm task={task} onSave={handleSave} onCancel={handleCancel} />
        </div>
      </MainLayout>
    </ProtectedRoute>
  );
}