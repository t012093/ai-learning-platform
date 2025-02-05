'use client'

import { useState, useRef, useEffect } from 'react'
import ChatMessage from './ChatMessage'
import { PaperAirplaneIcon } from '@heroicons/react/24/outline'

type Message = {
  id: number
  isAI: boolean
  message: string
  timestamp: string
}

type Props = {
  onComplete?: () => void
  onProgressUpdate?: (questionCount: number) => void
}

const TOTAL_QUESTIONS = 30

export default function ChatInterface({ onComplete, onProgressUpdate }: Props) {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: 1,
      isAI: true,
      message: 'こんにちは！あなたに最適な学習プランを提案するために、30個の質問をさせていただきます。まず、現在の職業や学習目的について教えていただけますか？',
      timestamp: new Date().toLocaleTimeString(),
    },
  ])
  const [input, setInput] = useState('')
  const [questionCount, setQuestionCount] = useState(0)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const getNextQuestion = (count: number): string => {
    const questions = [
      '週に何時間程度学習に時間を充てられそうですか？',
      '普段はどのような時間帯に学習するのが好ましいですか？',
      'オンラインでの学習とオフラインでの学習、どちらを希望されますか？',
      'これまでの学習経験で、どのような学習方法が最も効果的だと感じましたか？',
      '目標達成までの期間はどのくらいを想定していますか？',
      '学習を続ける上で、モチベーションを維持するために何か工夫していることはありますか？',
      'グループ学習と個人学習、どちらが好みですか？',
      '新しい概念を学ぶ際、どのようなアプローチが最も理解しやすいですか？',
      '学習環境について、どのような場所で学習するのが最も集中できますか？',
      '学習の進捗を確認する方法として、どのような形式が好ましいですか？'
      // 実際の実装では30問分用意
    ]
    return questions[count % questions.length]
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (!input.trim()) return

    const userMessage: Message = {
      id: messages.length + 1,
      isAI: false,
      message: input.trim(),
      timestamp: new Date().toLocaleTimeString(),
    }

    setMessages((prev) => [...prev, userMessage])
    setInput('')

    const newQuestionCount = questionCount + 1
    setQuestionCount(newQuestionCount)
    if (onProgressUpdate) {
      onProgressUpdate(newQuestionCount)
    }

    // AIの応答をシミュレート
    setTimeout(() => {
      let aiResponse = ''
      
      if (newQuestionCount < TOTAL_QUESTIONS) {
        aiResponse = `ありがとうございます。${getNextQuestion(newQuestionCount)}`
      } else {
        aiResponse = 'すべての質問にお答えいただき、ありがとうございました。これまでの情報を基に、あなたに最適な学習プランを作成いたします。'
        if (onComplete) {
          setTimeout(onComplete, 1000)
        }
      }

      const aiMessage: Message = {
        id: messages.length + 2,
        isAI: true,
        message: aiResponse,
        timestamp: new Date().toLocaleTimeString(),
      }
      setMessages((prev) => [...prev, aiMessage])
    }, 1000)
  }

  const progress = (questionCount / TOTAL_QUESTIONS) * 100

  return (
    <div className="flex flex-col h-[600px] bg-gray-50 rounded-lg shadow-lg">
      {/* 進捗バー */}
      <div className="p-4 border-b border-gray-200">
        <div className="flex items-center justify-between text-sm text-gray-600 mb-2">
          <span>アセスメントの進捗</span>
          <span>{questionCount}/{TOTAL_QUESTIONS}問</span>
        </div>
        <div className="w-full bg-gray-200 rounded-full h-2">
          <div
            className="bg-indigo-600 h-2 rounded-full transition-all duration-500"
            style={{ width: `${progress}%` }}
          />
        </div>
      </div>

      {/* チャット履歴 */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((message) => (
          <ChatMessage
            key={message.id}
            isAI={message.isAI}
            message={message.message}
            timestamp={message.timestamp}
          />
        ))}
        <div ref={messagesEndRef} />
      </div>

      {/* 入力フォーム */}
      <div className="border-t border-gray-200 p-4 bg-white rounded-b-lg">
        <form onSubmit={handleSubmit} className="flex space-x-4">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="メッセージを入力..."
            className="flex-1 rounded-lg border border-gray-300 px-4 py-2 focus:outline-none focus:border-indigo-500"
          />
          <button
            type="submit"
            className="bg-indigo-600 text-white px-4 py-2 rounded-lg hover:bg-indigo-500 transition-colors"
          >
            <PaperAirplaneIcon className="h-5 w-5" />
          </button>
        </form>
      </div>
    </div>
  )
}
