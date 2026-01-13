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
    <div className={`border border-gray-200 rounded-xl p-4 shadow-lg transition-all duration-300 hover:shadow-xl hover:scale-[1.02] ${
      task.completed
        ? 'bg-[#F0FFDF] border-[#A8DF8E]'
        : 'bg-white border-gray-200'
    }`}>
      {isEditing ? (
        <div className="space-y-3">
          <input
            type="text"
            value={editTitle}
            onChange={(e) => setEditTitle(e.target.value)}
            className="w-full p-3 border border-gray-300 rounded-xl text-lg font-medium text-gray-900 focus:border-[#A8DF8E] focus:outline-none transition-colors"
            autoFocus
          />
          <textarea
            value={editDescription}
            onChange={(e) => setEditDescription(e.target.value)}
            className="w-full p-3 border border-gray-300 rounded-xl text-gray-900 focus:border-[#A8DF8E] focus:outline-none transition-colors resize-none"
            rows={3}
          />
          <div className="flex space-x-2">
            <Button
              size="sm"
              className="bg-[#A8DF8E] hover:bg-[#97ce7e] text-white rounded-xl shadow-sm hover:scale-105 transition-transform"
              onClick={handleSave}
            >
              Save
            </Button>
            <Button
              variant="outline"
              size="sm"
              className="border-gray-300 hover:bg-gray-50 rounded-xl hover:scale-105 transition-transform"
              onClick={handleCancel}
            >
              Cancel
            </Button>
          </div>
        </div>
      ) : (
        <div>
          <div className="flex items-start">
            <input
              type="checkbox"
              checked={task.completed}
              onChange={handleToggleCompletion}
              className="mt-1 h-5 w-5 text-[#A8DF8E] rounded focus:ring-[#A8DF8E]"
            />
            <div className="ml-3 flex-1">
              <h3
                className={`text-lg font-medium ${
                  task.completed ? 'line-through text-gray-600' : 'text-gray-900'
                }`}
              >
                {task.title}
              </h3>
              {task.description && (
                <p
                  className={`mt-1 text-sm ${
                    task.completed ? 'line-through text-gray-500' : 'text-gray-600'
                  }`}
                >
                  {task.description}
                </p>
              )}
              <div className="mt-2 text-xs text-gray-500">
                Created: {new Date(task.created_at).toLocaleDateString()}
              </div>
            </div>
          </div>
          <div className="mt-3 flex justify-end space-x-2">
            <Button
              variant="outline"
              size="sm"
              className="border-gray-300 hover:bg-gray-50 rounded-xl hover:scale-105 transition-transform"
              onClick={handleEdit}
            >
              Edit
            </Button>
            <Button
              variant="danger"
              size="sm"
              className={`bg-[#FFD8DF] hover:bg-[#FFB3BA] text-[#FF5C6C] rounded-xl shadow-sm hover:scale-105 transition-transform ${
                isDeleting ? 'opacity-75 cursor-not-allowed' : ''
              }`}
              onClick={handleDelete}
              disabled={isDeleting}
            >
              {isDeleting ? 'Deleting...' : 'Delete'}
            </Button>
          </div>
        </div>
      )}
    </div>
  );
};