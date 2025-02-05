'use client'

import { MotionDiv, MotionH1, MotionP } from '@/components/animations/MotionDiv'
import Link from 'next/link'
import {
  BeakerIcon,
  UserGroupIcon,
  AcademicCapIcon,
  SparklesIcon,
  RocketLaunchIcon,
  ChartBarIcon,
} from '@heroicons/react/24/outline'

const features = [
  {
    name: 'AIによるパーソナライズ学習',
    description: 'あなたの学習スタイルを分析し、最適な学習プランを提案します。',
    icon: SparklesIcon,
  },
  {
    name: 'コミュニティとの連携',
    description: '同じ目標を持つ仲間と繋がり、モチベーションを高めます。',
    icon: UserGroupIcon,
  },
  {
    name: '進捗の可視化',
    description: '学習の進捗をグラフやチャートで分かりやすく表示します。',
    icon: ChartBarIcon,
  },
  {
    name: 'カスタマイズ可能なカリキュラム',
    description: 'あなたのペースとニーズに合わせてカリキュラムを調整できます。',
    icon: AcademicCapIcon,
  },
  {
    name: 'リアルタイムフィードバック',
    description: 'AIが学習状況を分析し、改善点を提案します。',
    icon: BeakerIcon,
  },
  {
    name: '目標達成のサポート',
    description: '明確な目標設定と達成までのロードマップを提供します。',
    icon: RocketLaunchIcon,
  },
]

export default function Home() {
  return (
    <div className="space-y-24">
      {/* ヒーローセクション */}
      <div className="relative isolate overflow-hidden">
        <div className="mx-auto max-w-7xl px-6 py-24 sm:py-32 lg:px-8">
          <div className="mx-auto max-w-2xl lg:mx-0 lg:max-w-xl">
            <div className="flex">
              <div className="relative rounded-full px-3 py-1 text-sm leading-6 text-gray-600 ring-1 ring-gray-900/10 hover:ring-gray-900/20">
                AIによる新しい学習体験を始めましょう{' '}
                <Link href="/assessment" className="font-semibold text-indigo-600">
                  <span className="absolute inset-0" aria-hidden="true" />
                  診断を開始 <span aria-hidden="true">&rarr;</span>
                </Link>
              </div>
            </div>
            <MotionH1
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5 }}
              className="mt-10 text-4xl font-bold tracking-tight text-gray-900 sm:text-6xl"
            >
              AIが導く、あなただけの学習体験
            </MotionH1>
            <MotionP
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: 0.2 }}
              className="mt-6 text-lg leading-8 text-gray-600"
            >
              最新のAI技術があなたの学習スタイルを分析し、パーソナライズされた学習プランを提案。
              効率的な学習で、目標達成までの道のりをサポートします。
            </MotionP>
            <div className="mt-10 flex items-center gap-x-6">
              <Link
                href="/assessment"
                className="rounded-md bg-indigo-600 px-3.5 py-2.5 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
              >
                無料で診断を始める
              </Link>
              <Link href="/community" className="text-sm font-semibold leading-6 text-gray-900">
                コミュニティを見る <span aria-hidden="true">→</span>
              </Link>
            </div>
          </div>
        </div>
        <div
          className="absolute left-1/2 top-0 -z-10 -translate-x-1/2 blur-3xl xl:-top-6"
          aria-hidden="true"
        >
          <div
            className="aspect-[1155/678] w-[72.1875rem] bg-gradient-to-tr from-[#ff80b5] to-[#9089fc] opacity-30"
            style={{
              clipPath:
                'polygon(74.1% 44.1%, 100% 61.6%, 97.5% 26.9%, 85.5% 0.1%, 80.7% 2%, 72.5% 32.5%, 60.2% 62.4%, 52.4% 68.1%, 47.5% 58.3%, 45.2% 34.5%, 27.5% 76.7%, 0.1% 64.9%, 17.9% 100%, 27.6% 76.8%, 76.1% 97.7%, 74.1% 44.1%)',
            }}
          />
        </div>
      </div>

      {/* 特徴セクション */}
      <div className="mx-auto max-w-7xl px-6 lg:px-8">
        <div className="mx-auto max-w-2xl lg:text-center">
          <h2 className="text-base font-semibold leading-7 text-indigo-600">
            より効果的な学習を
          </h2>
          <p className="mt-2 text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl">
            AIがあなたの学習をサポート
          </p>
          <p className="mt-6 text-lg leading-8 text-gray-600">
            最新のAI技術を活用し、一人ひとりに最適化された学習環境を提供します。
            あなたの目標達成をサポートする様々な機能をご用意しています。
          </p>
        </div>
        <div className="mx-auto mt-16 max-w-2xl sm:mt-20 lg:mt-24 lg:max-w-none">
          <dl className="grid max-w-xl grid-cols-1 gap-x-8 gap-y-16 lg:max-w-none lg:grid-cols-3">
            {features.map((feature) => (
              <MotionDiv
                key={feature.name}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5 }}
                viewport={{ once: true }}
                className="flex flex-col"
              >
                <dt className="flex items-center gap-x-3 text-base font-semibold leading-7 text-gray-900">
                  <feature.icon
                    className="h-5 w-5 flex-none text-indigo-600"
                    aria-hidden="true"
                  />
                  {feature.name}
                </dt>
                <dd className="mt-4 flex flex-auto flex-col text-base leading-7 text-gray-600">
                  <p className="flex-auto">{feature.description}</p>
                </dd>
              </MotionDiv>
            ))}
          </dl>
        </div>
      </div>

      {/* CTAセクション */}
      <div className="relative isolate overflow-hidden bg-gray-900">
        <div className="px-6 py-24 sm:px-6 sm:py-32 lg:px-8">
          <div className="mx-auto max-w-2xl text-center">
            <h2 className="text-3xl font-bold tracking-tight text-white sm:text-4xl">
              あなたの学習をAIが最適化
              <br />
              今すぐ始めましょう
            </h2>
            <p className="mx-auto mt-6 max-w-xl text-lg leading-8 text-gray-300">
              たった30問の質問であなたに最適な学習プランを作成。
              効率的な学習で、目標達成までの道のりをサポートします。
            </p>
            <div className="mt-10 flex items-center justify-center gap-x-6">
              <Link
                href="/assessment"
                className="rounded-md bg-white px-3.5 py-2.5 text-sm font-semibold text-gray-900 shadow-sm hover:bg-gray-100 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-white"
              >
                無料で診断を始める
              </Link>
              <Link href="/learning" className="text-sm font-semibold leading-6 text-white">
                学習方法を見る <span aria-hidden="true">→</span>
              </Link>
            </div>
          </div>
        </div>
        <div
          className="absolute -top-24 right-0 -z-10 transform-gpu blur-3xl"
          aria-hidden="true"
        >
          <div
            className="aspect-[1404/767] w-[87.75rem] bg-gradient-to-r from-[#80caff] to-[#4f46e5] opacity-25"
            style={{
              clipPath:
                'polygon(73.6% 51.7%, 91.7% 11.8%, 100% 46.4%, 97.4% 82.2%, 92.5% 84.9%, 75.7% 64%, 55.3% 47.5%, 46.5% 49.4%, 45% 62.9%, 50.3% 87.2%, 21.3% 64.1%, 0.1% 100%, 5.4% 51.1%, 21.4% 63.9%, 58.9% 0.2%, 73.6% 51.7%)',
            }}
          />
        </div>
      </div>
    </div>
  )
}
