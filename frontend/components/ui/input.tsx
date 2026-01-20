import React from 'react';

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {}

export const Input: React.FC<InputProps> = ({
  className = '',
  ...props
}) => {
  const baseClasses = 'block w-full rounded-lg border-slate-300 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 focus:outline-none transition-colors text-slate-900 bg-slate-50/50';
  const classes = `${baseClasses} ${className}`;

  return (
    <input
      className={classes}
      {...props}
    />
  );
};