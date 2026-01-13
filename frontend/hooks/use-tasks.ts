// frontend/hooks/use-tasks.ts

import React, { useEffect, useState } from "react";
import { apiClient, Task } from "@/lib/api";
import { useAuth } from "@/providers/auth-provider";

type Filter = "all" | "active" | "completed";

// Helper function to safely extract error message
const extractErrorMessage = (errorObj: any, defaultMessage: string = "An error occurred"): string => {
  if (!errorObj) return defaultMessage;

  // If it's already a string, return it
  if (typeof errorObj === 'string') return errorObj;

  // If it has a message property, return that
  if (errorObj.message) return errorObj.message;

  // If it has a detail property, return that
  if (errorObj.detail) return errorObj.detail;

  // If it's an array (like validation errors), join the messages
  if (Array.isArray(errorObj)) {
    return errorObj.map(err =>
      typeof err === 'string' ? err :
      err.msg || err.detail || err.message || JSON.stringify(err)
    ).join('; ');
  }

  // Fallback to string conversion
  return String(errorObj);
};

export const useTasks = () => {
  const { token, user } = useAuth();

  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [filter, setFilter] = useState<Filter>("all");

  // Track loading operations to properly manage loading state
  const loadingOperationsCount = React.useRef<number>(0);

  // Manage loading state with a counter to handle multiple simultaneous operations
  const setLoadingState = React.useCallback((isLoading: boolean) => {
    if (isLoading) {
      loadingOperationsCount.current += 1;
      setLoading(true);
    } else if (loadingOperationsCount.current > 0) {
      loadingOperationsCount.current -= 1;
      if (loadingOperationsCount.current === 0) {
        setLoading(false);
      }
    }
  }, []);

  // Track tasks that are currently being deleted to prevent duplicate API calls
  const deletingTaskIds = React.useRef<Set<number>>(new Set());

  useEffect(() => {
    if (token && user?.id) {
      loadTasks();
    }
  }, [token, user]);

  const loadTasks = async () => {
    if (!token || !user?.id) return;

    setLoadingState(true);
    setError(null);

    const res = await apiClient.getTasks(user.id, token);

    if (res.success && Array.isArray(res.data)) {
      const tasksData = [...res.data];
      setTasks(() => tasksData);
    } else {
      setError(extractErrorMessage(res.error, "Failed to load tasks"));
    }

    setLoadingState(false);
  };

  const createTask = async (title: string, description?: string) => {
    if (!token || !user?.id) return;

    setLoadingState(true);
    setError(null);

    const res = await apiClient.createTask(
      user.id,
      { title, description, completed: false },
      token
    );

    if (res.success && res.data) {
      const newTask = res.data;
      setTasks(prev => [...prev, newTask]);
    } else {
      setError(extractErrorMessage(res.error, "Failed to create task"));
    }

    setLoadingState(false);
  };

  const updateTask = async (taskId: number, data: Partial<Task>) => {
    if (!token || !user?.id) return;

    setLoadingState(true);
    setError(null);

    const res = await apiClient.updateTask(user.id, taskId, data, token);

    if (!res.success || !res.data) {
      setError(extractErrorMessage(res.error, "Failed to update task"));
      setLoadingState(false);
      return;
    }

    const updatedTask = res.data;

    setTasks(prev =>
      prev.map(task =>
        task.id === taskId ? updatedTask : task
      )
    );

    setLoadingState(false);
  };

  // Enhanced deleteTask with duplicate prevention and proper state management
  const deleteTask = async (taskId: number) => {
    if (!token || !user?.id) return;

    // Prevent duplicate API calls for the same task
    if (deletingTaskIds.current.has(taskId)) {
      return; // Already deleting this task
    }

    // Add task ID to the set of tasks being deleted
    deletingTaskIds.current.add(taskId);

    try {
      setLoadingState(true);
      setError(null);

      const res = await apiClient.deleteTask(user.id, taskId, token);

      if (res.success) {
        // Remove task from state - this should trigger UI update
        setTasks(prev => prev.filter(task => task.id !== taskId));
      } else {
        setError(extractErrorMessage(res.error, "Failed to delete task"));
      }
    } catch (err) {
      setError(extractErrorMessage(err, "Failed to delete task"));
    } finally {
      // Remove task ID from the set after completion
      deletingTaskIds.current.delete(taskId);
      setLoadingState(false);
    }
  };

  const toggleTaskCompletion = async (taskId: number) => {
    const task = tasks.find(t => t.id === taskId);
    if (!task || !token || !user?.id) return;

    setLoadingState(true);
    setError(null);

    const res = await apiClient.toggleTaskCompletion(user.id, taskId, !task.completed, token);

    if (!res.success || !res.data) {
      setError(extractErrorMessage(res.error, "Failed to toggle task completion"));
      setLoadingState(false);
      return;
    }

    const updatedTask = res.data;

    setTasks(prev =>
      prev.map(task =>
        task.id === taskId ? updatedTask : task
      )
    );

    setLoadingState(false);
  };

  const filteredTasks = tasks.filter(task => {
    if (filter === "active") return !task.completed;
    if (filter === "completed") return task.completed;
    return true;
  });

  return {
    tasks: filteredTasks,
    loading,
    error,
    filter,
    setFilter,
    createTask,
    updateTask,
    deleteTask,
    toggleTaskCompletion,
    reload: loadTasks,
  };
};
