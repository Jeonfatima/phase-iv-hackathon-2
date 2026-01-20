import React from 'react';
import { Button } from '../ui/button';
import { Input } from '../ui/input';

interface TaskFormProps {
  onSubmit: (title: string, description: string) => void;
  loading: boolean;
}

export const TaskForm: React.FC<TaskFormProps> = ({ onSubmit, loading }) => {
  const [title, setTitle] = React.useState('');
  const [description, setDescription] = React.useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    if (!title.trim()) return;

    onSubmit(title.trim(), description.trim());
    setTitle('');
    setDescription('');
  };

  return (
    <form onSubmit={handleSubmit} className="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
      <div className="space-y-4">
        <div>
          <label htmlFor="title" className="block text-sm font-medium text-slate-700 mb-2">
            Task Title
          </label>
          <Input
            id="title"
            type="text"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            placeholder="What needs to be done?"
            className="w-full px-4 py-3 rounded-lg border-slate-300 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 focus:outline-none transition-colors text-slate-900 bg-slate-50/50"
            required
          />
        </div>

        <div>
          <label htmlFor="description" className="block text-sm font-medium text-slate-700 mb-2">
            Description (Optional)
          </label>
          <textarea
            id="description"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            placeholder="Add details..."
            className="block w-full rounded-lg border-slate-300 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 focus:outline-none transition-colors text-slate-900 bg-slate-50/50 resize-none"
            rows={2}
          />
        </div>

        <div>
          <Button
            type="submit"
            disabled={loading || !title.trim()}
            className={`w-full bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700 text-white rounded-lg shadow-sm hover:shadow-md transition-all ${
              (loading || !title.trim()) ? 'opacity-75 cursor-not-allowed' : ''
            }`}
          >
            {loading ? (
              <div className="flex items-center justify-center">
                <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin mr-2"></div>
                Adding task...
              </div>
            ) : (
              'Add Task'
            )}
          </Button>
        </div>
      </div>
    </form>
  );
};