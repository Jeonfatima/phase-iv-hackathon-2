'use client';

import React, { useState, useEffect } from 'react';
import { TaskList } from '@/components/tasks/task-list';
import { TaskForm } from '@/components/tasks/task-form';
import { useTasks } from '@/hooks/use-tasks';
import { useAuth } from '@/providers/auth-provider';
import { useRouter } from 'next/navigation';
import ChatBotButton from '@/components/ChatBotButton';
import ChatPanel from '@/components/ChatPanel';
import useChat from '@/hooks/useChat';

export default function DashboardPage() {
  const { tasks: filteredTasks, createTask, loading, error, setFilter, filter } = useTasks();
  const { logout, user } = useAuth();
  const router = useRouter();
  const [isChatOpen, setIsChatOpen] = useState(false);
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);

  // Only initialize chat functionality when user is authenticated
  const userId = user?.id?.toString() || '';
  const isAuthenticated = !!user;

  // Initialize chat hook only when user is authenticated
  const chatHook = useChat(userId);
  const { messages, sendMessage, isLoading: isChatLoading, error: chatError } = chatHook;

  const handleCreateTask = async (title: string, description: string) => {
    await createTask(title, description);
  };

  const handleSignOut = async () => {
    await logout();
    router.push('/login');
  };

  const toggleChat = () => {
    setIsChatOpen(!isChatOpen);
  };

  const toggleSidebar = () => {
    setSidebarCollapsed(!sidebarCollapsed);
  };

  const handleSendChatMessage = (message: string) => {
    if (userId) {
      sendMessage(message);
    } else {
      console.error('Cannot send message: user not authenticated');
    }
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
  };

  // Handle responsive sidebar behavior
  useEffect(() => {
    const handleResize = () => {
      if (window.innerWidth < 768) {
        setSidebarCollapsed(true);
      } else {
        setSidebarCollapsed(false);
      }
    };

    handleResize();
    window.addEventListener('resize', handleResize);

    return () => {
      window.removeEventListener('resize', handleResize);
    };
  }, []);

  return (
    <div className="flex h-screen bg-slate-900 overflow-hidden">
      {/* Sidebar */}
      <div className={`bg-slate-900 border-r border-slate-700/50 flex flex-col transition-all duration-300 ${sidebarCollapsed ? 'w-20' : 'w-64'}`}>
        <div className="p-4 border-b border-slate-700/50">
          {!sidebarCollapsed && (
            <h1 className="text-2xl font-bold bg-gradient-to-r from-indigo-400 to-purple-400 bg-clip-text text-transparent">
              Todo App Diary
            </h1>
          )}
          {sidebarCollapsed && (
            <div className="text-center">
              <div className="text-xl font-bold bg-gradient-to-r from-indigo-400 to-purple-400 bg-clip-text text-transparent">T</div>
            </div>
          )}
        </div>

        <nav className="flex-1 p-4">
          <ul className="space-y-2">
            <li>
              <a href="#" className={`flex items-center ${sidebarCollapsed ? 'justify-center' : 'px-3 py-2'} text-indigo-400 bg-indigo-900/30 rounded-lg font-medium border border-indigo-500/30 ${sidebarCollapsed ? 'p-3' : ''}`}>
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                </svg>
                {!sidebarCollapsed && <span className="ml-3">My Tasks</span>}
              </a>
            </li>
            <li>
              <a href="#" className={`flex items-center ${sidebarCollapsed ? 'justify-center' : 'px-3 py-2'} text-slate-300 hover:bg-slate-800/50 rounded-lg hover:border-l-2 hover:border-indigo-500/50 transition-all ${sidebarCollapsed ? 'p-3' : ''}`}>
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                {!sidebarCollapsed && <span className="ml-3">Scheduled</span>}
              </a>
            </li>
            <li>
              <a href="#" className={`flex items-center ${sidebarCollapsed ? 'justify-center' : 'px-3 py-2'} text-slate-300 hover:bg-slate-800/50 rounded-lg hover:border-l-2 hover:border-indigo-500/50 transition-all ${sidebarCollapsed ? 'p-3' : ''}`}>
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                {!sidebarCollapsed && <span className="ml-3">Completed</span>}
              </a>
            </li>
            <li>
              <a href="#" className={`flex items-center ${sidebarCollapsed ? 'justify-center' : 'px-3 py-2'} text-slate-300 hover:bg-slate-800/50 rounded-lg hover:border-l-2 hover:border-indigo-500/50 transition-all ${sidebarCollapsed ? 'p-3' : ''}`}>
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" />
                </svg>
                {!sidebarCollapsed && <span className="ml-3">Labels</span>}
              </a>
            </li>
          </ul>
        </nav>

        <div className="p-4 border-t border-slate-700/50">
          {!sidebarCollapsed ? (
            <div className="flex items-center justify-between">
              <div className="flex items-center">
                <div className="w-8 h-8 bg-gradient-to-r from-indigo-500 to-purple-500 rounded-full flex items-center justify-center text-white text-sm font-semibold">
                  {user?.email?.charAt(0)?.toUpperCase() || 'U'}
                </div>
                <div className="ml-3">
                  <p className="text-sm font-medium text-slate-200">{user?.email?.split('@')[0]}</p>
                  <p className="text-xs text-slate-400">Online</p>
                </div>
              </div>
              <button
                onClick={handleSignOut}
                className="p-2 text-slate-400 hover:text-slate-200 hover:bg-slate-800/50 rounded-lg transition-colors"
              >
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                </svg>
              </button>
            </div>
          ) : (
            <div className="flex flex-col items-center space-y-3">
              <div className="w-8 h-8 bg-gradient-to-r from-indigo-500 to-purple-500 rounded-full flex items-center justify-center text-white text-sm font-semibold">
                {user?.email?.charAt(0)?.toUpperCase() || 'U'}
              </div>
              <button
                onClick={handleSignOut}
                className="p-2 text-slate-400 hover:text-slate-200 hover:bg-slate-800/50 rounded-lg transition-colors"
              >
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                </svg>
              </button>
            </div>
          )}
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Top Bar */}
        <header className="bg-slate-900/80 backdrop-blur-lg border-b border-slate-700/50 px-4 sm:px-6 py-4 flex items-center">
          <button
            onClick={toggleSidebar}
            className="mr-4 p-2 text-slate-400 hover:text-white hover:bg-slate-800/50 rounded-lg transition-colors lg:hidden"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
            </svg>
          </button>

          <div className="flex-1">
            <h2 className="text-xl sm:text-2xl font-bold text-slate-200">Your Tasks</h2>
            <p className="text-slate-400 mt-1 text-sm sm:text-base">Hey {user?.email?.split('@')[0]}! Ready to be productive? 👋</p>
          </div>

          <div className="hidden md:flex items-center space-x-4">
            <div className="text-sm text-slate-400">
              {new Date().toLocaleDateString('en-US', { weekday: 'long', month: 'long', day: 'numeric' })}
            </div>
          </div>
          <div className="md:hidden text-xs text-slate-400 ml-2">
            {new Date().toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}
          </div>
        </header>

        {/* Content Area */}
        <main className="flex-1 overflow-auto p-4 sm:p-6">
          <div className="max-w-none sm:max-w-6xl mx-auto">
            {error && (
              <div className="mb-6 p-4 bg-red-900/30 text-red-300 rounded-xl text-sm border border-red-700/50">
                {typeof error === 'string' ? error : JSON.stringify(error)}
              </div>
            )}

            <div className="bg-slate-800/40 backdrop-blur-sm rounded-2xl shadow-xl border border-slate-700/50 p-4 sm:p-6 mb-6">
              <TaskForm onSubmit={handleCreateTask} loading={loading} />
            </div>

            <div className="bg-slate-800/40 backdrop-blur-sm rounded-2xl shadow-xl border border-slate-700/50 p-4 sm:p-6">
              <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-6">
                <div className="flex flex-wrap gap-2">
                  <button
                    onClick={() => setFilter('all')}
                    className={`px-3 sm:px-4 py-2 rounded-lg text-xs sm:text-sm font-medium transition-colors ${
                      filter === 'all'
                        ? 'bg-indigo-600 text-white shadow-lg'
                        : 'text-slate-300 hover:bg-slate-700/50'
                    }`}
                  >
                    All ({filteredTasks.length})
                  </button>
                  <button
                    onClick={() => setFilter('active')}
                    className={`px-3 sm:px-4 py-2 rounded-lg text-xs sm:text-sm font-medium transition-colors ${
                      filter === 'active'
                        ? 'bg-indigo-600 text-white shadow-lg'
                        : 'text-slate-300 hover:bg-slate-700/50'
                    }`}
                  >
                    Active ({filteredTasks.filter(t => !t.completed).length})
                  </button>
                  <button
                    onClick={() => setFilter('completed')}
                    className={`px-3 sm:px-4 py-2 rounded-lg text-xs sm:text-sm font-medium transition-colors ${
                      filter === 'completed'
                        ? 'bg-indigo-600 text-white shadow-lg'
                        : 'text-slate-300 hover:bg-slate-700/50'
                    }`}
                  >
                    Completed ({filteredTasks.filter(t => t.completed).length})
                  </button>
                </div>

                <div className="text-xs sm:text-sm text-slate-400">
                  {filteredTasks.length} tasks
                </div>
              </div>

              {loading ? (
                <div className="flex justify-center items-center h-32">
                  <div className="animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-indigo-500"></div>
                </div>
              ) : (
                <TaskList tasks={filteredTasks} />
              )}
            </div>
          </div>
        </main>

        {/* Footer */}
        <footer className="bg-slate-900/80 backdrop-blur-lg border-t border-slate-700/50 px-4 sm:px-6 py-4">
          <div className="flex flex-col sm:flex-row items-center justify-between text-xs sm:text-sm text-slate-400 gap-2">
            <span>Made by Fatima Salman</span>
            <span>© {new Date().getFullYear()} Todo App Diary. All rights reserved.</span>
          </div>
        </footer>
      </div>

      {/* Chatbot Components */}
      <ChatBotButton onClick={toggleChat} />
      <ChatPanel
        isOpen={isChatOpen}
        onClose={toggleChat}
        messages={messages}
        onSendMessage={handleSendChatMessage}
        isLoading={isChatLoading}
      />
    </div>
  );
}