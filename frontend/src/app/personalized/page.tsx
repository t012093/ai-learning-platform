'use client'

import { MotionDiv, MotionH1, MotionP } from '@/components/animations/MotionDiv'
import {
  SparklesIcon,
  MoonIcon,
  CalendarIcon,
  LightBulbIcon,
  ChartBarIcon,
  ClockIcon,
  UserIcon,
  AcademicCapIcon
} from '@heroicons/react/24/outline'
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  LineChart,
  Line
} from 'recharts'

const sleepData = [
  { hour: '22', quality: 85 },
  { hour: '23', quality: 90 },
  { hour: '0', quality: 95 },
  { hour: '1', quality: 88 },
  { hour: '2', quality: 80 },
  { hour: '3', quality: 75 },
  { hour: '4', quality: 70 },
  { hour: '5', quality: 75 },
  { hour: '6', quality: 85 },
  { hour: '7', quality: 90 },
]

const weeklySchedule = [
  { day: '月', hours: 3 },
  { day: '火', hours: 2 },
  { day: '水', hours: 4 },
  { day: '木', hours: 2 },
  { day: '金', hours: 3 },
  { day: '土', hours: 5 },
  { day: '日', hours: 4 },
]

const learningStyle = {
  visualLearning: 80,
  auditoryLearning: 60,
  kinestheticLearning: 40,
}

export default function PersonalizedPage() {
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
          パーソナライズ分析結果
        </MotionH1>
        <MotionP
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.2 }}
          className="mt-4 text-lg text-gray-600"
        >
          AIによって分析された、あなたに最適な学習スタイルとスケジュール
        </MotionP>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* 学習スタイル分析 */}
        <MotionDiv
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="bg-white rounded-lg shadow-lg p-6"
        >
          <h2 className="text-xl font-semibold text-gray-900 mb-4 flex items-center">
            <SparklesIcon className="h-6 w-6 text-indigo-600 mr-2" />
            学習スタイル分析
          </h2>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart
                data={[
                  { type: '視覚的学習', value: learningStyle.visualLearning },
                  { type: '聴覚的学習', value: learningStyle.auditoryLearning },
                  { type: '体験的学習', value: learningStyle.kinestheticLearning },
                ]}
                margin={{ top: 20, right: 30, left: 20, bottom: 5 }}
              >
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="type" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="value" fill="#4f46e5" />
              </BarChart>
            </ResponsiveContainer>
          </div>
          <div className="mt-4 space-y-2">
            <p className="text-sm text-gray-600">
              • あなたは視覚的な学習が最も効果的です
            </p>
            <p className="text-sm text-gray-600">
              • 図表やダイアグラムを活用した学習をおすすめします
            </p>
          </div>
        </MotionDiv>

        {/* 睡眠パターンと最適学習時間 */}
        <MotionDiv
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.2 }}
          className="bg-white rounded-lg shadow-lg p-6"
        >
          <h2 className="text-xl font-semibold text-gray-900 mb-4 flex items-center">
            <MoonIcon className="h-6 w-6 text-indigo-600 mr-2" />
            睡眠パターンと最適学習時間
          </h2>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart
                data={sleepData}
                margin={{ top: 20, right: 30, left: 20, bottom: 5 }}
              >
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="hour" />
                <YAxis />
                <Tooltip />
                <Line type="monotone" dataKey="quality" stroke="#4f46e5" />
              </LineChart>
            </ResponsiveContainer>
          </div>
          <div className="mt-4 space-y-2">
            <p className="text-sm text-gray-600">
              • 最適な睡眠時間: 23:00 - 7:00
            </p>
            <p className="text-sm text-gray-600">
              • 推奨学習時間帯: 9:00 - 11:00, 15:00 - 17:00
            </p>
          </div>
        </MotionDiv>

        {/* 週間推奨スケジュール */}
        <MotionDiv
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.4 }}
          className="bg-white rounded-lg shadow-lg p-6"
        >
          <h2 className="text-xl font-semibold text-gray-900 mb-4 flex items-center">
            <CalendarIcon className="h-6 w-6 text-indigo-600 mr-2" />
            週間推奨スケジュール
          </h2>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart
                data={weeklySchedule}
                margin={{ top: 20, right: 30, left: 20, bottom: 5 }}
              >
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="day" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="hours" fill="#4f46e5" />
              </BarChart>
            </ResponsiveContainer>
          </div>
          <div className="mt-4 space-y-2">
            <p className="text-sm text-gray-600">
              • 週23時間の学習時間を推奨
            </p>
            <p className="text-sm text-gray-600">
              • 土曜日は集中的な学習に適しています
            </p>
          </div>
        </MotionDiv>

        {/* 性格タイプと学習アプローチ */}
        <MotionDiv
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.6 }}
          className="bg-white rounded-lg shadow-lg p-6"
        >
          <h2 className="text-xl font-semibold text-gray-900 mb-4 flex items-center">
            <UserIcon className="h-6 w-6 text-indigo-600 mr-2" />
            性格タイプと学習アプローチ
          </h2>
          <div className="space-y-4">
            <div className="border rounded-lg p-4">
              <h3 className="font-semibold text-gray-900 flex items-center">
                <LightBulbIcon className="h-5 w-5 text-indigo-600 mr-2" />
                論理的思考型
              </h3>
              <p className="mt-2 text-sm text-gray-600">
                体系的なアプローチを好み、概念の理解を重視します。理論から実践へと段階的に学習を進めることで最も効果的に知識を吸収できます。
              </p>
            </div>

            <div className="border rounded-lg p-4">
              <h3 className="font-semibold text-gray-900 flex items-center">
                <ChartBarIcon className="h-5 w-5 text-indigo-600 mr-2" />
                目標指向型
              </h3>
              <p className="mt-2 text-sm text-gray-600">
                明確な目標設定と進捗管理が効果的です。小さな目標を達成していくことでモチベーションを維持できます。
              </p>
            </div>

            <div className="border rounded-lg p-4">
              <h3 className="font-semibold text-gray-900 flex items-center">
                <ClockIcon className="h-5 w-5 text-indigo-600 mr-2" />
                集中力パターン
              </h3>
              <p className="mt-2 text-sm text-gray-600">
                45分の集中学習と15分の休憩を組み合わせたポモドーロテクニックが効果的です。
              </p>
            </div>

            <div className="border rounded-lg p-4">
              <h3 className="font-semibold text-gray-900 flex items-center">
                <AcademicCapIcon className="h-5 w-5 text-indigo-600 mr-2" />
                推奨学習方法
              </h3>
              <p className="mt-2 text-sm text-gray-600">
                • プロジェクトベースの学習
                • 概念マップの作成
                • 定期的な振り返りと復習
              </p>
            </div>
          </div>
        </MotionDiv>
      </div>
    </div>
  )
}
