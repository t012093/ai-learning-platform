'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { MotionH1, MotionP } from '@/components/animations/MotionDiv'
import ChatInterface from '@/components/chat/ChatInterface'
import AnalyzingPopup from '@/components/assessment/AnalyzingPopup'

export default function AssessmentPage() {
  const router = useRouter()
  const [showAnalyzing, setShowAnalyzing] = useState(false)
  const [hasStarted, setHasStarted] = useState(false)
  const [progress, setProgress] = useState({
    career: 0,
    learning: 0,
    lifestyle: 0
  })

  const updateProgress = (questionCount: number) => {
    // 30問を3カテゴリに分けて進捗を更新
    if (questionCount <= 10) {
      setProgress(prev => ({ ...prev, career: questionCount }))
    } else if (questionCount <= 20) {
      setProgress(prev => ({ ...prev, learning: questionCount - 10 }))
    } else {
      setProgress(prev => ({ ...prev, lifestyle: questionCount - 20 }))
    }
  }

  const handleStartAssessment = () => {
    setHasStarted(true)
  }

  const handleChatComplete = () => {
    setShowAnalyzing(true)
    // 分析中のアニメーションを3秒間表示した後、パーソナライズ情報ページに遷移
    setTimeout(() => {
      router.push('/personalized')
    }, 3000)
  }

  return (
    <div className="space-y-8">
      <div className="text-center space-y-4">
        <MotionH1
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl"
        >
          パーソナライズドアセスメント
        </MotionH1>
        <MotionP
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.2 }}
          className="mt-4 text-lg text-gray-600"
        >
          AIとの対話を通じて、あなたに最適な学習プランを作成します
        </MotionP>
        {!hasStarted && (
          <button
            onClick={handleStartAssessment}
            className="mt-6 inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
          >
            パーソナライズ診断を開始する
          </button>
        )}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* チャットインターフェース */}
        <div className="lg:col-span-2">
          {hasStarted && (
            <ChatInterface
              onComplete={handleChatComplete}
              onProgressUpdate={updateProgress}
            />
          )}
        </div>

        {/* サイドバー：アセスメント進捗 */}
        <div className="space-y-6">
          <div className="bg-white p-6 rounded-lg shadow-lg">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">アセスメントの進捗</h3>
            <div className="space-y-4">
              <div>
                <div className="flex justify-between text-sm text-gray-600 mb-1">
                  <span>キャリア・目標</span>
                  <span>{progress.career}/10</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div
                    className="bg-indigo-600 h-2 rounded-full transition-all duration-500"
                    style={{ width: `${(progress.career / 10) * 100}%` }}
                  />
                </div>
              </div>
              <div>
                <div className="flex justify-between text-sm text-gray-600 mb-1">
                  <span>学習スタイル</span>
                  <span>{progress.learning}/10</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div
                    className="bg-indigo-600 h-2 rounded-full transition-all duration-500"
                    style={{ width: `${(progress.learning / 10) * 100}%` }}
                  />
                </div>
              </div>
              <div>
                <div className="flex justify-between text-sm text-gray-600 mb-1">
                  <span>生活習慣・環境</span>
                  <span>{progress.lifestyle}/10</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div
                    className="bg-indigo-600 h-2 rounded-full transition-all duration-500"
                    style={{ width: `${(progress.lifestyle / 10) * 100}%` }}
                  />
                </div>
              </div>
            </div>
          </div>

          <div className="bg-white p-6 rounded-lg shadow-lg">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">これまでの回答から</h3>
            <ul className="space-y-3 text-sm text-gray-600">
              <li className="flex items-start">
                <span className="inline-block w-2 h-2 bg-indigo-600 rounded-full mt-1.5 mr-2"></span>
                学習意欲が高く、実践的なスキル習得に興味があります
              </li>
              <li className="flex items-start">
                <span className="inline-block w-2 h-2 bg-indigo-600 rounded-full mt-1.5 mr-2"></span>
                オンラインでの学習を希望しています
              </li>
              <li className="flex items-start">
                <span className="inline-block w-2 h-2 bg-indigo-600 rounded-full mt-1.5 mr-2"></span>
                週10時間程度の学習時間を確保できそうです
              </li>
            </ul>
          </div>
        </div>
      </div>

      <AnalyzingPopup
        isOpen={showAnalyzing}
        onAnalysisComplete={() => router.push('/personalized')}
      />
    </div>
  )
}
