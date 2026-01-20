import React from 'react';
import { Task } from '@/lib/types';
import { useTasks } from '@/hooks/use-tasks';
import { Button } from '../ui/button';

interface TaskCardProps {
  task: Task;
}

export const TaskCard: React.FC<TaskCardProps> = ({ task }) => {
  const { toggleTaskCompletion, deleteTask, updateTask } = useTasks();
  const [isEditing, setIsEditing] = React.useState(false);
  const [editTitle, setEditTitle] = React.useState(task.title);
  const [editDescription, setEditDescription] = React.useState(task.description || '');
  const [isDeleting, setIsDeleting] = React.useState(false);

  const handleToggleCompletion = () => {
    toggleTaskCompletion(task.id);
  };

  const handleDelete = async () => {
    setIsDeleting(true);
    try {
      await deleteTask(task.id);
    } finally {
      setIsDeleting(false);
    }
  };

  const handleEdit = () => {
    setIsEditing(true);
    setEditTitle(task.title);
    setEditDescription(task.description || '');
  };

  const handleSave = () => {
    updateTask(task.id, {
      title: editTitle,
      description: editDescription || undefined,
    });
    setIsEditing(false);
  };

  const handleCancel = () => {
    setIsEditing(false);
    setEditTitle(task.title);
    setEditDescription(task.description || '');
  };

  return (
    <div className={`bg-white border border-slate-200 rounded-xl p-5 shadow-sm hover:shadow-md transition-all duration-200 hover:-translate-y-0.5 group ${
      task.completed
        ? 'bg-slate-50 border-slate-200'
        : 'hover:border-indigo-200'
    }`}>
      {isEditing ? (
        <div className="space-y-4">
          <input
            type="text"
            value={editTitle}
            onChange={(e) => setEditTitle(e.target.value)}
            className="w-full px-3 py-2 border border-slate-300 rounded-lg text-base font-medium text-slate-900 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 focus:outline-none transition-colors"
            autoFocus
          />
          <textarea
            value={editDescription}
            onChange={(e) => setEditDescription(e.target.value)}
            className="w-full px-3 py-2 border border-slate-300 rounded-lg text-slate-900 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 focus:outline-none transition-colors resize-none"
            rows={2}
          />
          <div className="flex space-x-2">
            <Button
              size="sm"
              className="bg-indigo-600 hover:bg-indigo-700 text-white rounded-lg shadow-sm hover:scale-105 transition-transform text-sm px-3 py-1.5"
              onClick={handleSave}
            >
              Save
            </Button>
            <Button
              variant="outline"
              size="sm"
              className="border-slate-300 hover:bg-slate-50 rounded-lg hover:scale-105 transition-transform text-sm px-3 py-1.5"
              onClick={handleCancel}
            >
              Cancel
            </Button>
          </div>
        </div>
      ) : (
        <div>
          <div className="flex items-start gap-3">
            <button
              onClick={handleToggleCompletion}
              className={`flex-shrink-0 w-5 h-5 rounded border-2 mt-0.5 flex items-center justify-center transition-colors ${
                task.completed
                  ? 'bg-indigo-600 border-indigo-600 text-white'
                  : 'border-slate-300 hover:border-indigo-400'
              }`}
            >
              {task.completed && (
                <svg className="w-3 h-3" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                </svg>
              )}
            </button>
            <div className="flex-1 min-w-0">
              <h3
                className={`text-base font-medium ${
                  task.completed ? 'line-through text-slate-500' : 'text-slate-900'
                }`}
              >
                {task.title}
              </h3>
              {task.description && (
                <p
                  className={`mt-1 text-sm ${
                    task.completed ? 'line-through text-slate-400' : 'text-slate-600'
                  }`}
                >
                  {task.description}
                </p>
              )}
              <div className="mt-2 flex items-center text-xs text-slate-500">
                <span>Created: {new Date(task.created_at).toLocaleDateString()}</span>
                {task.completed && (
                  <span className="ml-2 inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                    Completed
                  </span>
                )}
              </div>
            </div>
          </div>

          {/* Action buttons - hidden by default, shown on hover */}
          <div className="mt-3 flex justify-end space-x-1 opacity-0 group-hover:opacity-100 transition-opacity">
            <button
              onClick={handleEdit}
              className="p-1.5 text-slate-400 hover:text-slate-600 hover:bg-slate-100 rounded-md transition-colors"
            >
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
              </svg>
            </button>
            <button
              onClick={handleDelete}
              disabled={isDeleting}
              className={`p-1.5 text-slate-400 hover:text-red-600 hover:bg-red-50 rounded-md transition-colors ${
                isDeleting ? 'opacity-50 cursor-not-allowed' : ''
              }`}
            >
              {isDeleting ? (
                <svg className="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
              ) : (
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                </svg>
              )}
            </button>
          </div>
        </div>
      )}
    </div>
  );
};