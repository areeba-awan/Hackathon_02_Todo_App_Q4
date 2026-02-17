'use client';

import ProtectedRoute from '@/components/protected-route';
import MainLayout from '@/components/main-layout';
import TaskForm from '@/components/task-form';
import { Task } from '@/types/task';
import { useRouter } from 'next/navigation';

export default function EditTaskPage() {
  const router = useRouter();

  // Mock task data - in a real app, this would come from props or API
  const mockTask: Task = {
    id: '1',
    title: 'Sample Task',
    description: 'This is a sample task to demonstrate the UI',
    completed: false,
    dueDate: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000), // 7 days from now
    createdAt: new Date(),
    updatedAt: new Date(),
    userId: 'user-123',
  };

  const handleSave = (task: Task) => {
    // In a real app, this would save to the backend
    // For now, we'll just navigate back to the tasks page
    router.push('/tasks');
  };

  const handleCancel = () => {
    router.push('/tasks');
  };

  return (
    <ProtectedRoute>
      <MainLayout>
        <div className="bg-white shadow-xl sm:rounded-lg p-6 dark:bg-gray-800">
          <h1 className="text-2xl font-bold bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 bg-clip-text text-transparent mb-6">Edit Task</h1>
          <TaskForm task={mockTask} onSave={handleSave} onCancel={handleCancel} />
        </div>
      </MainLayout>
    </ProtectedRoute>
  );
}