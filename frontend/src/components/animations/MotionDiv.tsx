'use client'

import { motion, HTMLMotionProps } from 'framer-motion'

type BaseMotionProps = {
  children: React.ReactNode
}

type MotionDivProps = BaseMotionProps & Omit<HTMLMotionProps<'div'>, 'children'>
type MotionH1Props = BaseMotionProps & Omit<HTMLMotionProps<'h1'>, 'children'>
type MotionPProps = BaseMotionProps & Omit<HTMLMotionProps<'p'>, 'children'>

export function MotionDiv({ children, ...props }: MotionDivProps) {
  return <motion.div {...props}>{children}</motion.div>
}

export function MotionH1({ children, ...props }: MotionH1Props) {
  return <motion.h1 {...props}>{children}</motion.h1>
}

export function MotionP({ children, ...props }: MotionPProps) {
  return <motion.p {...props}>{children}</motion.p>
}
