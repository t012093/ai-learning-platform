'use client'

import { MotionDiv, MotionH1, MotionP } from '@/components/animations/MotionDiv'
import { 
  BookOpenIcon, 
  AcademicCapIcon, 
  ClockIcon, 
  CheckCircleIcon,
  ArrowPathIcon,
  BoltIcon,
  PuzzlePieceIcon
} from '@heroicons/react/24/outline'

type Section = {
  id: number
  title: string
  description: string
  duration: string
  completed: boolean
  contents: {
    type: 'video' | 'article' | 'exercise'
    title: string
    description: string
    url?: string
    duration?: string
  }[]
}

const sections: Section[] = [
  {
    id: 1,
    title: '基礎理解',
    description: 'モダンなWeb開発の基礎概念を学びます',
    duration: '1週間',
    completed: false,
    contents: [
      {
        type: 'video',
        title: 'Webアプリケーションの概要',
        description: 'フロントエンド、バックエンド、データベースの基本的な関係について学びます',
        url: 'https://youtube.com/...',
        duration: '45分'
      },
      {
        type: 'article',
        title: 'モダンWeb開発入門',
        description: '現代のWeb開発で使用される主要な技術スタックについて解説します',
        url: 'https://example.com/article'
      },
      {
        type: 'exercise',
        title: '基礎知識の確認',
        description: '学んだ内容の理解度をチェックする簡単な演習に取り組みます'
      }
    ]
  },
  {
    id: 2,
    title: 'フロントエンド開発',
    description: 'React.jsを使用したUIの実装',
    duration: '2週間',
    completed: false,
    contents: [
      {
        type: 'video',
        title: 'React基礎講座',
        description: 'コンポーネント、props、stateなどReactの基本概念を学びます',
        url: 'https://youtube.com/...',
        duration: '60分'
      },
      {
        type: 'exercise',
        title: 'ToDoアプリの作成',
        description: '学んだ内容を活かして実際にアプリケーションを作成します'
      }
    ]
  }
]

export default function CurriculumPage() {
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
          Webアプリケーション開発コース
        </MotionH1>
        <MotionP
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.2 }}
          className="mt-4 text-lg text-gray-600"
        >
          AIが分析したあなたの学習スタイルに合わせて最適化されたカリキュラムです
        </MotionP>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* メインコンテンツ：カリキュラム */}
        <div className="lg:col-span-2 space-y-6">
          {sections.map((section) => (
            <MotionDiv
              key={section.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5 }}
              className="bg-white rounded-lg shadow-lg p-6"
            >
              <div className="flex items-start justify-between">
                <div>
                  <h3 className="text-lg font-semibold text-gray-900 flex items-center">
                    {section.completed && (
                      <CheckCircleIcon className="h-6 w-6 text-green-500 mr-2" />
                    )}
                    {section.title}
                  </h3>
                  <p className="mt-2 text-gray-600">{section.description}</p>
                  <div className="mt-2 flex items-center text-sm text-gray-500">
                    <ClockIcon className="h-5 w-5 mr-1" />
                    {section.duration}
                  </div>
                </div>
              </div>

              <div className="mt-4 space-y-4">
                {section.contents.map((content, index) => (
                  <div
                    key={index}
                    className="border rounded-lg p-4 hover:bg-gray-50 transition-colors"
                  >
                    <div className="flex items-start">
                      {content.type === 'video' && (
                        <AcademicCapIcon className="h-6 w-6 text-indigo-600 mt-1" />
                      )}
                      {content.type === 'article' && (
                        <BookOpenIcon className="h-6 w-6 text-indigo-600 mt-1" />
                      )}
                      {content.type === 'exercise' && (
                        <PuzzlePieceIcon className="h-6 w-6 text-indigo-600 mt-1" />
                      )}
                      <div className="ml-3">
                        <h4 className="text-base font-medium text-gray-900">{content.title}</h4>
                        <p className="mt-1 text-sm text-gray-500">{content.description}</p>
                        {content.duration && (
                          <div className="mt-2 flex items-center text-sm text-gray-500">
                            <ClockIcon className="h-4 w-4 mr-1" />
                            {content.duration}
                          </div>
                        )}
                        {content.url && (
                          <a
                            href={content.url}
                            className="mt-2 inline-flex items-center text-sm font-medium text-indigo-600 hover:text-indigo-500"
                            target="_blank"
                            rel="noopener noreferrer"
                          >
                            コンテンツを開く
                            <ArrowPathIcon className="ml-1 h-4 w-4" />
                          </a>
                        )}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </MotionDiv>
          ))}
        </div>

        {/* サイドバー：学習進捗とAIによる改善提案 */}
        <div className="space-y-6">
          {/* 進捗状況 */}
          <div className="bg-white rounded-lg shadow-lg p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">学習の進捗</h3>
            <div className="space-y-4">
              <div>
                <div className="flex justify-between text-sm text-gray-600 mb-1">
                  <span>基礎理解</span>
                  <span>0/3</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div className="bg-indigo-600 h-2 rounded-full w-0"></div>
                </div>
              </div>
              <div>
                <div className="flex justify-between text-sm text-gray-600 mb-1">
                  <span>フロントエンド開発</span>
                  <span>0/2</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div className="bg-indigo-600 h-2 rounded-full w-0"></div>
                </div>
              </div>
            </div>
          </div>

          {/* AIによる改善提案 */}
          <div className="bg-white rounded-lg shadow-lg p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
              <BoltIcon className="h-5 w-5 text-indigo-600 mr-2" />
              AIからの提案
            </h3>
            <div className="space-y-4">
              <div className="border-l-4 border-indigo-500 pl-4 py-2">
                <p className="text-sm text-gray-600">
                  基礎理解を深めるために、まずは概念の全体像をつかむことをおすすめします。動画教材から始めるのが効果的でしょう。
                </p>
              </div>
              <button className="w-full bg-indigo-600 text-white px-4 py-2 rounded-lg hover:bg-indigo-500 transition-colors">
                カリキュラムを更新する
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
