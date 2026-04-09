import React, { useEffect, useRef, useState } from 'react'

interface Props {
  label: string
  value: string | number
  sub?: string
  children?: React.ReactNode
}

export function MetricCard({ label, value, sub, children }: Props) {
  return (
    <div style={{
      background: 'var(--bg-surface-2)',
      border: '1px solid var(--border-base)',
      borderRadius: 8,
      padding: '12px 16px',
      display: 'flex',
      flexDirection: 'column',
      gap: 4,
    }}>
      <div style={{
        fontFamily: 'var(--font-display)',
        fontSize: 9,
        fontWeight: 700,
        letterSpacing: '0.12em',
        textTransform: 'uppercase',
        color: 'var(--text-dim)',
      }}>{label}</div>

      <div style={{
        fontFamily: 'var(--font-display)',
        fontWeight: 700,
        fontSize: 28,
        color: 'var(--text-primary)',
        lineHeight: 1,
      }}>{value}</div>

      {sub && (
        <div style={{
          fontFamily: 'var(--font-body)',
          fontSize: 11,
          color: 'var(--text-secondary)',
        }}>{sub}</div>
      )}

      {children}
    </div>
  )
}
