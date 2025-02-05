'use client'

import { MotionH1, MotionP, MotionDiv } from '@/components/animations/MotionDiv'
import { CheckCircleIcon, PlayCircleIcon, BookOpenIcon, ClockIcon } from '@heroicons/react/24/outline'
import { useRouter } from 'next/navigation'

type LearningModule = {
  id: number
  title: string
  description: string
  completed: boolean
  duration: string
  resources: {
    type: 'video' | 'article'
    title: string
    url: string
  }[]
}

const modules: LearningModule[] = [
  {
    id: 1,
    title: 'プログラミング基礎',
    description: 'プログラミングの基本概念と考え方を学びます',
    completed: true,
    duration: '2週間',
    resources: [
      {
        type: 'video',
        title: 'プログラミング入門講座',
        url: 'https://youtube.com/...'
      },
      {
        type: 'article',
        title: 'プログラミング思考の基礎',
        url: 'https://example.com/article'
      }
    ]
  },
  {
    id: 2,
    title: 'Webアプリケーション開発',
    description: 'モダンなWebアプリケーション開発の手法を学びます',
    completed: false,
    duration: '4週間',
    resources: [
      {
        type: 'video',
        title: 'React入門',
        url: 'https://youtube.com/...'
      },
      {
        type: 'article',
        title: 'フロントエンド開発ベストプラクティス',
        url: 'https://example.com/article'
      }
    ]
  }
]

export default function LearningPage() {
  const router = useRouter()

  const handleStartModule = (moduleId: number) => {
    router.push(`/curriculum/${moduleId}`)
  }

  return (
    <div className="space-y-8">
      {/* ヘッダー */}
      <div className="text-center">
        <MotionH1
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl"
        >
          パーソナライズド学習プログラム
        </MotionH1>
        <MotionP
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.2 }}
          className="mt-4 text-lg text-gray-600"
        >
          あなたの目標と学習スタイルに合わせた最適な学習プランです
        </MotionP>
      </div>

      {/* 学習の進捗状況 */}
      <div className="bg-white rounded-lg shadow-lg p-6">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">学習の進捗状況</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-indigo-50 p-4 rounded-lg">
            <div className="font-semibold text-indigo-800">完了したモジュール</div>
            <div className="text-3xl font-bold text-indigo-600">1/2</div>
          </div>
          <div className="bg-indigo-50 p-4 rounded-lg">
            <div className="font-semibold text-indigo-800">学習時間</div>
            <div className="text-3xl font-bold text-indigo-600">12時間</div>
          </div>
          <div className="bg-indigo-50 p-4 rounded-lg">
            <div className="font-semibold text-indigo-800">次回の目標</div>
            <div className="text-3xl font-bold text-indigo-600">3日後</div>
          </div>
        </div>
      </div>

      {/* 学習モジュール */}
      <div className="space-y-6">
        {modules.map((module) => (
          <MotionDiv
            key={module.id}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            className="bg-white rounded-lg shadow-lg p-6"
          >
            <div className="flex items-start justify-between">
              <div>
                <h3 className="text-lg font-semibold text-gray-900 flex items-center">
                  {module.completed && (
                    <CheckCircleIcon className="h-6 w-6 text-green-500 mr-2" />
                  )}
                  {module.title}
                </h3>
                <p className="mt-2 text-gray-600">{module.description}</p>
                <div className="mt-2 flex items-center text-sm text-gray-500">
                  <ClockIcon className="h-5 w-5 mr-1" />
                  {module.duration}
                </div>
              </div>
              {!module.completed && (
                <button 
                  onClick={() => handleStartModule(module.id)}
                  className="bg-indigo-600 text-white px-4 py-2 rounded-lg hover:bg-indigo-500 transition-colors"
                >
                  開始する
                </button>
              )}
            </div>

            <div className="mt-4 border-t pt-4">
              <h4 className="text-sm font-semibold text-gray-700 mb-2">学習リソース</h4>
              <ul className="space-y-2">
                {module.resources.map((resource, index) => (
                  <li key={index} className="flex items-center text-sm">
                    {resource.type === 'video' ? (
                      <PlayCircleIcon className="h-5 w-5 text-indigo-600 mr-2" />
                    ) : (
                      <BookOpenIcon className="h-5 w-5 text-indigo-600 mr-2" />
                    )}
                    <a
                      href={resource.url}
                      className="text-indigo-600 hover:text-indigo-500"
                      target="_blank"
                      rel="noopener noreferrer"
                    >
                      {resource.title}
                    </a>
                  </li>
                ))}
              </ul>
            </div>
          </MotionDiv>
        ))}
      </div>
    </div>
  )
}
