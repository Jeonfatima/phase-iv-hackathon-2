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
    <form onSubmit={handleSubmit} className="space-y-4 bg-white p-6 rounded-2xl shadow-md border border-gray-100">
      <div>
        <label htmlFor="title" className="block text-sm font-medium text-gray-700 mb-2">
          Task Title
        </label>
        <Input
          id="title"
          type="text"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          placeholder="What needs to be done?"
          className="w-full p-3 rounded-xl border-gray-300 focus:border-[#A8DF8E] focus:ring-[#A8DF8E] text-gray-900"
          required
        />
      </div>

      <div>
        <label htmlFor="description" className="block text-sm font-medium text-gray-700 mb-2">
          Description (Optional)
        </label>
        <textarea
          id="description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          placeholder="Add details..."
          className="block w-full rounded-xl border-gray-300 focus:border-[#A8DF8E] focus:ring-[#A8DF8E] sm:text-sm p-3 border border-gray-300 text-gray-900 resize-none"
          rows={2}
        />
      </div>

      <div>
        <Button
          type="submit"
          disabled={loading || !title.trim()}
          className={`w-full bg-[#A8DF8E] hover:bg-[#97ce7e] text-white rounded-xl shadow-sm hover:scale-[1.02] transition-transform ${
            (loading || !title.trim()) ? 'opacity-75 cursor-not-allowed' : ''
          }`}
        >
          {loading ? 'Adding task...' : 'Add Task'}
        </Button>
      </div>
    </form>
  );
};