import React from 'react';

export const EmptyState: React.FC = () => {
  return (
    <div className="text-center py-16 px-4">
      <div className="inline-flex items-center justify-center p-4 bg-gray-100 rounded-full mb-4">
        <svg
          className="h-12 w-12 text-[#A8DF8E]"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
          aria-hidden="true"
        >
          <path
            vectorEffect="non-scaling-stroke"
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"
          />
        </svg>
      </div>
      <h3 className="mt-2 text-lg font-medium text-gray-900">No tasks yet</h3>
      <p className="mt-2 text-gray-600 max-w-md mx-auto">
        Get started by creating your first task in the form above.
      </p>
    </div>
  );
};