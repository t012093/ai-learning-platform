'use client'

import { MotionH1, MotionP, MotionDiv } from '@/components/animations/MotionDiv'
import { 
  UserGroupIcon, 
  CalendarIcon, 
  MapPinIcon, 
  ChatBubbleLeftRightIcon,
  ArrowRightIcon
} from '@heroicons/react/24/outline'

type Event = {
  id: number
  title: string
  type: 'online' | 'offline'
  date: string
  description: string
  participants: number
  maxParticipants: number
}

const upcomingEvents: Event[] = [
  {
    id: 1,
    title: 'プログラミング勉強会',
    type: 'online',
    date: '2024/03/15 19:00',
    description: 'オンラインでのプログラミング勉強会です。初心者歓迎！',
    participants: 15,
    maxParticipants: 20
  },
  {
    id: 2,
    title: '渋谷もくもく会',
    type: 'offline',
    date: '2024/03/20 14:00',
    description: '渋谷のコワーキングスペースで開催する勉強会です。',
    participants: 8,
    maxParticipants: 12
  }
]

export default function CommunityPage() {
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
          学習コミュニティ
        </MotionH1>
        <MotionP
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.2 }}
          className="mt-4 text-lg text-gray-600"
        >
          仲間と一緒に学び、成長しましょう
        </MotionP>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* メインコンテンツ */}
        <div className="lg:col-span-2 space-y-6">
          {/* イベント一覧 */}
          <div className="bg-white rounded-lg shadow-lg p-6">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">近日開催予定のイベント</h2>
            <div className="space-y-4">
              {upcomingEvents.map((event) => (
                <MotionDiv
                  key={event.id}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  className="border rounded-lg p-4"
                >
                  <div className="flex items-start justify-between">
                    <div>
                      <h3 className="font-semibold text-gray-900">{event.title}</h3>
                      <p className="text-gray-600 text-sm mt-1">{event.description}</p>
                      <div className="flex items-center mt-2 text-sm text-gray-500">
                        <CalendarIcon className="h-4 w-4 mr-1" />
                        {event.date}
                        <span className="mx-2">•</span>
                        {event.type === 'online' ? (
                          <UserGroupIcon className="h-4 w-4 mr-1" />
                        ) : (
                          <MapPinIcon className="h-4 w-4 mr-1" />
                        )}
                        {event.type === 'online' ? 'オンライン' : 'オフライン'}
                      </div>
                    </div>
                    <button className="bg-indigo-600 text-white px-4 py-2 rounded-lg hover:bg-indigo-500 transition-colors text-sm">
                      参加する
                    </button>
                  </div>
                  <div className="mt-3 bg-gray-50 rounded-lg p-2">
                    <div className="text-sm text-gray-600">
                      参加者: {event.participants}/{event.maxParticipants}
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2 mt-1">
                      <div
                        className="bg-indigo-600 h-2 rounded-full"
                        style={{
                          width: `${(event.participants / event.maxParticipants) * 100}%`,
                        }}
                      ></div>
                    </div>
                  </div>
                </MotionDiv>
              ))}
            </div>
          </div>

          {/* ディスカッションボード */}
          <div className="bg-white rounded-lg shadow-lg p-6">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">ディスカッション</h2>
            <div className="space-y-4">
              <div className="border rounded-lg p-4">
                <h3 className="font-semibold text-gray-900">React学習のおすすめ教材</h3>
                <p className="text-gray-600 text-sm mt-1">
                  Reactの学習を始めたいのですが、おすすめの教材やロードマップがありましたら教えてください。
                </p>
                <div className="flex items-center mt-2 text-sm text-gray-500">
                  <ChatBubbleLeftRightIcon className="h-4 w-4 mr-1" />
                  12件の返信
                </div>
              </div>
              <div className="border rounded-lg p-4">
                <h3 className="font-semibold text-gray-900">学習時間の確保について</h3>
                <p className="text-gray-600 text-sm mt-1">
                  仕事と学習の両立について、みなさんどのように時間を確保していますか？
                </p>
                <div className="flex items-center mt-2 text-sm text-gray-500">
                  <ChatBubbleLeftRightIcon className="h-4 w-4 mr-1" />
                  8件の返信
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* サイドバー */}
        <div className="space-y-6">
          {/* 学習仲間を探す */}
          <div className="bg-white rounded-lg shadow-lg p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">学習仲間を探す</h3>
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="font-semibold text-gray-900">Webフロントエンド</p>
                  <p className="text-sm text-gray-600">15人が学習中</p>
                </div>
                <ArrowRightIcon className="h-5 w-5 text-gray-400" />
              </div>
              <div className="flex items-center justify-between">
                <div>
                  <p className="font-semibold text-gray-900">バックエンド開発</p>
                  <p className="text-sm text-gray-600">12人が学習中</p>
                </div>
                <ArrowRightIcon className="h-5 w-5 text-gray-400" />
              </div>
            </div>
          </div>

          {/* ローカルコミュニティ */}
          <div className="bg-white rounded-lg shadow-lg p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">近くのコミュニティ</h3>
            <div className="space-y-4">
              <div className="border rounded-lg p-4">
                <h4 className="font-semibold text-gray-900">渋谷エンジニアコミュニティ</h4>
                <p className="text-sm text-gray-600 mt-1">
                  毎週水曜日に渋谷で勉強会を開催しています。
                </p>
                <button className="mt-2 text-indigo-600 text-sm font-semibold">
                  詳細を見る
                </button>
              </div>
              <div className="border rounded-lg p-4">
                <h4 className="font-semibold text-gray-900">新宿Tech Meetup</h4>
                <p className="text-sm text-gray-600 mt-1">
                  月1回のペースで技術勉強会を開催しています。
                </p>
                <button className="mt-2 text-indigo-600 text-sm font-semibold">
                  詳細を見る
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
