type ChatMessageProps = {
  isAI: boolean
  message: string
  timestamp: string
}

export default function ChatMessage({ isAI, message, timestamp }: ChatMessageProps) {
  return (
    <div className={`flex ${isAI ? 'justify-start' : 'justify-end'} mb-4`}>
      <div
        className={`max-w-[70%] rounded-lg p-4 ${
          isAI ? 'bg-white text-gray-900' : 'bg-indigo-600 text-white'
        }`}
      >
        <p className="text-sm">{message}</p>
        <p className={`text-xs mt-2 ${isAI ? 'text-gray-500' : 'text-indigo-200'}`}>
          {timestamp}
        </p>
      </div>
    </div>
  )
}
