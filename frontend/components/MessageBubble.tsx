import React from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

interface MessageBubbleProps {
  role: 'user' | 'assistant';
  content: string;
  timestamp?: Date;
}

const MessageBubble = ({ role, content, timestamp }: MessageBubbleProps) => {
  const isUser = role === 'user';

  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-4`}>
      <div
        className={`max-w-[85%] rounded-2xl p-4 ${
          isUser
            ? 'bg-gradient-to-r from-indigo-600 to-purple-600 text-white rounded-br-none shadow-sm'
            : 'bg-white border border-slate-200 text-slate-800 rounded-bl-none shadow-sm'
        }`}
      >
        <div className={`prose prose-sm max-w-none ${
          isUser ? 'text-white' : 'text-slate-800'
        }`}>
          {isUser ? (
            <p className="mb-0">{content}</p>
          ) : (
            <ReactMarkdown
              remarkPlugins={[remarkGfm]}
              components={{
                p: ({node, ...props}) => <p className="mb-2 last:mb-0" {...props} />,
                ul: ({node, ...props}) => <ul className="mb-2 ml-5 list-disc" {...props} />,
                ol: ({node, ...props}) => <ol className="mb-2 ml-5 list-decimal" {...props} />,
                li: ({node, ...props}) => <li className="mb-1" {...props} />,
                strong: ({node, ...props}) => <strong className="font-semibold" {...props} />,
                em: ({node, ...props}) => <em className="italic" {...props} />,
                code: ({node, ...props}) => <code className="bg-slate-100 text-slate-800 px-1 py-0.5 rounded text-sm font-mono" {...props} />,
                pre: ({node, ...props}) => <pre className="bg-slate-100 p-3 rounded-lg overflow-x-auto text-sm" {...props} />,
              }}
            >
              {content}
            </ReactMarkdown>
          )}
        </div>
        {timestamp && (
          <div
            className={`text-xs mt-2 ${
              isUser ? 'text-indigo-200' : 'text-slate-500'
            }`}
          >
            {timestamp.toLocaleTimeString([], {
              hour: '2-digit',
              minute: '2-digit',
            })}
          </div>
        )}
      </div>
    </div>
  );
};

export default MessageBubble;