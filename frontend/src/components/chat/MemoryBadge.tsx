import React, { useState } from 'react'

interface Props {
  cubeId: string
  type?: string
  content?: string
  tier?: string
  score?: number
  accessCount?: number
}

function getBadgeStyle(type: string) {
  if (type === 'episodic') return {
    bg: 'rgba(168,85,247,0.15)',
    border: 'rgba(168,85,247,0.4)',
    prefix: '▌',
  }
  if (type === 'semantic') return {
    bg: 'rgba(20,184,166,0.15)',
    border: 'rgba(20,184,166,0.4)',
    prefix: '●',
  }
  return {
    bg: 'rgba(251,146,60,0.15)',
    border: 'rgba(251,146,60,0.4)',
    prefix: '◆',
  }
}

export function MemoryBadge({ cubeId, type = 'episodic', content, tier, score, accessCount }: Props) {
  const [showTooltip, setShowTooltip] = useState(false)
  const style = getBadgeStyle(type.toLowerCase())
  const label = content ? content.slice(0, 24) + (content.length > 24 ? '…' : '') : cubeId.slice(0, 8)

  return (
    <span
      style={{ position: 'relative', display: 'inline-block' }}
      onMouseEnter={() => setShowTooltip(true)}
      onMouseLeave={() => setShowTooltip(false)}
    >
      <span style={{
        display: 'inline-flex',
        alignItems: 'center',
        gap: 4,
        background: style.bg,
        border: `1px solid ${style.border}`,
        borderRadius: 4,
        padding: '3px 8px',
        fontFamily: 'var(--font-body)',
        fontSize: 11,
        color: 'var(--text-secondary)',
        cursor: 'default',
      }}>
        <span>{style.prefix}</span>
        {label}
      </span>

      {showTooltip && (
        <div style={{
          position: 'absolute',
          bottom: '100%',
          left: 0,
          marginBottom: 4,
          background: 'var(--bg-surface-3)',
          border: '1px solid var(--border-base)',
          borderRadius: 4,
          padding: '6px 10px',
          fontFamily: 'var(--font-mono)',
          fontSize: 10,
          color: 'var(--text-secondary)',
          whiteSpace: 'nowrap',
          zIndex: 100,
          lineHeight: 1.6,
          minWidth: 180,
        }}>
          <div>id: {cubeId}</div>
          <div>type: {type}</div>
          <div>tier: {tier ?? '—'}</div>
          <div>score: {score != null ? score.toFixed(2) : '—'}</div>
          <div>access: {accessCount ?? 0}</div>
        </div>
      )}
    </span>
  )
}
