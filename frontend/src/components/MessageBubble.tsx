import React from 'react';
import { Message } from '../types';

interface MessageBubbleProps {
  message: Message;
}

const MessageBubble: React.FC<MessageBubbleProps> = ({ message }) => {
  const isUser = message.role === 'user';

  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'}`}>
      <div
        className={`max-w-[70%] rounded-lg px-4 py-3 ${
          isUser
            ? 'bg-blue-600 text-white'
            : 'bg-white border border-gray-200 text-gray-800'
        }`}
      >
        {/* Message Content */}
        <div className="text-sm whitespace-pre-wrap">{message.content}</div>

        {/* Metadata */}
        {message.metadata && (
          <div className="mt-2 pt-2 border-t border-gray-200 text-xs opacity-75">
            {message.metadata.sources && message.metadata.sources.length > 0 && (
              <div>
                Sources: {message.metadata.sources.join(', ')}
              </div>
            )}
          </div>
        )}

        {/* Timestamp */}
        {message.timestamp && (
          <div className="text-xs mt-1 opacity-60">
            {new Date(message.timestamp).toLocaleTimeString()}
          </div>
        )}
      </div>
    </div>
  );
};

export default MessageBubble;
