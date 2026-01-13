import React from 'react';

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {}

export const Input: React.FC<InputProps> = ({
  className = '',
  ...props
}) => {
  const baseClasses = 'block w-full rounded-xl border-gray-300 shadow-sm focus:border-[#A8DF8E] focus:ring-[#A8DF8E] sm:text-sm border border-gray-300 text-gray-900';
  const classes = `${baseClasses} ${className}`;

  return (
    <input
      className={classes}
      {...props}
    />
  );
};