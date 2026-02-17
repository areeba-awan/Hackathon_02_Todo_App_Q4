'use client';

import ProtectedRoute from '@/components/protected-route';
import MainLayout from '@/components/main-layout';
import TaskForm from '@/components/task-form';
import { Task } from '@/types/task';
import { useRouter } from 'next/navigation';

export default function NewTaskPage() {
  const router = useRouter();

  const handleSave = (task: Task) => {
    // Task has been saved to backend, redirect to tasks page
    router.push('/tasks');
  };

  const handleCancel = () => {
    router.push('/tasks');
  };

  return (
    <ProtectedRoute>
      <MainLayout>
        <div className="bg-white shadow-xl sm:rounded-lg p-6 dark:bg-gray-800">
          <h1 className="text-2xl font-bold bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 bg-clip-text text-transparent mb-6">Create New Task</h1>
          <TaskForm onSave={handleSave} onCancel={handleCancel} />
        </div>
      </MainLayout>
    </ProtectedRoute>
  );
}