'use client';

import React from 'react';
import { TaskList } from '@/components/tasks/task-list';
import { TaskForm } from '@/components/tasks/task-form';
import { useTasks } from '@/hooks/use-tasks';
import { useAuth } from '@/providers/auth-provider';
import { Button } from '@/components/ui/button';
import { useRouter } from 'next/navigation';

export default function DashboardPage() {
  const { tasks: filteredTasks, createTask, loading, error, setFilter, filter } = useTasks();
  const { logout } = useAuth();
  const router = useRouter();

  const handleCreateTask = async (title: string, description: string) => {
    await createTask(title, description);
  };

  const handleSignOut = async () => {
    await logout();
    router.push('/login');
  };

  return (
    <>
      {/* Header */}
      <div className="bg-[#A8DF8E] text-white p-6 rounded-t-2xl rounded-b-lg">
        <div className="flex justify-between items-center max-w-4xl mx-auto">
          <h1 className="text-2xl font-bold">Todo App Diary</h1>
          <Button
            variant="secondary"
            size="sm"
            className="bg-white text-[#A8DF8E] hover:bg-gray-100 rounded-xl"
            onClick={handleSignOut}
          >
            Sign Out
          </Button>
        </div>
      </div>

      {/* Main Content */}
      <div className="p-6 bg-[#FFF0F5] min-h-screen">
        <div className="max-w-4xl mx-auto">
          {error && (
            <div className="mb-4 p-4 bg-[#FFD8DF] text-[#FF5C6C] rounded-xl">
              {typeof error === 'string' ? error : JSON.stringify(error)}
            </div>
          )}

          <TaskForm onSubmit={handleCreateTask} loading={loading} />

          <div className="mt-8">
            <div className="flex space-x-4 mb-6 justify-center">
              <button
                onClick={() => setFilter('all')}
                className={`px-4 py-2 rounded-xl text-sm font-medium transition-colors ${
                  filter === 'all'
                    ? 'bg-[#FFAAB8] text-white shadow-md'
                    : 'bg-white text-gray-700 border border-gray-200 hover:bg-gray-50'
                }`}
              >
                All
              </button>
              <button
                onClick={() => setFilter('active')}
                className={`px-4 py-2 rounded-xl text-sm font-medium transition-colors ${
                  filter === 'active'
                    ? 'bg-[#FFAAB8] text-white shadow-md'
                    : 'bg-white text-gray-700 border border-gray-200 hover:bg-gray-50'
                }`}
              >
                Active
              </button>
              <button
                onClick={() => setFilter('completed')}
                className={`px-4 py-2 rounded-xl text-sm font-medium transition-colors ${
                  filter === 'completed'
                    ? 'bg-[#FFAAB8] text-white shadow-md'
                    : 'bg-white text-gray-700 border border-gray-200 hover:bg-gray-50'
                }`}
              >
                Completed
              </button>
            </div>

            {loading ? (
              <div className="flex justify-center items-center h-32">
                <div className="animate-spin rounded-full h-10 w-10 border-t-2 border-b-2 border-[#A8DF8E]"></div>
              </div>
            ) : (
              <TaskList tasks={filteredTasks} />
            )}
          </div>
        </div>

        {/* Footer */}
        <footer className="mt-12 text-center text-gray-500 text-sm">
          Made by Fatima Salman 464666
        </footer>
      </div>
    </>
  );
}