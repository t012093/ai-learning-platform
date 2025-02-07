'use client'

import dynamic from 'next/dynamic'
import { HTMLMotionProps } from 'framer-motion'

type BaseMotionProps = {
  children: React.ReactNode
}

type MotionDivProps = BaseMotionProps & Omit<HTMLMotionProps<'div'>, 'children'>
type MotionH1Props = BaseMotionProps & Omit<HTMLMotionProps<'h1'>, 'children'>
type MotionPProps = BaseMotionProps & Omit<HTMLMotionProps<'p'>, 'children'>

const MotionDivBase = dynamic(
  () => import('framer-motion').then((mod) => {
    const { motion } = mod
    return ({ children, ...props }: MotionDivProps) => (
      <motion.div {...props}>{children}</motion.div>
    )
  }),
  { ssr: true }
)

const MotionH1Base = dynamic(
  () => import('framer-motion').then((mod) => {
    const { motion } = mod
    return ({ children, ...props }: MotionH1Props) => (
      <motion.h1 {...props}>{children}</motion.h1>
    )
  }),
  { ssr: true }
)

const MotionPBase = dynamic(
  () => import('framer-motion').then((mod) => {
    const { motion } = mod
    return ({ children, ...props }: MotionPProps) => (
      <motion.p {...props}>{children}</motion.p>
    )
  }),
  { ssr: true }
)

export const MotionDiv = MotionDivBase
export const MotionH1 = MotionH1Base
export const MotionP = MotionPBase
