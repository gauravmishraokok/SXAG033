import React from 'react'

export interface CourtHistoryEntry {
  id: string
  label: string
  time: string
  resolution: 'accept' | 'reject' | 'merge'
}

interface Props {
  entries: CourtHistoryEntry[]
}

const icons = { accept: '✓', reject: '✗', merge: '⟳' }
const colors = {
  accept: 'var(--accent-green)',
  reject: 'var(--accent-red)',
  merge:  'var(--accent-amber)',
}

export function CourtHistory({ entries }: Props) {
  if (entries.length === 0) return null

  return (
    <div style={{ padding: '12px 14px', borderTop: '1px solid var(--border-dim)' }}>
      <div style={{
        fontFamily: 'var(--font-display)',
        fontSize: 9,
        fontWeight: 700,
        letterSpacing: '0.14em',
        color: 'var(--text-dim)',
        marginBottom: 8,
      }}>
        RESOLVED TODAY ─────────────────────────────
      </div>
      {entries.slice(0, 5).map((e) => (
        <div key={e.id} style={{
          display: 'flex',
          alignItems: 'center',
          gap: 8,
          fontFamily: 'var(--font-mono)',
          fontSize: 11,
          color: 'var(--text-secondary)',
          marginBottom: 4,
        }}>
          <span style={{ color: colors[e.resolution], width: 12 }}>{icons[e.resolution]}</span>
          <span style={{ flex: 1, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>{e.label}</span>
          <span style={{ color: 'var(--text-dim)', flexShrink: 0 }}>{e.time}</span>
          <span style={{ color: colors[e.resolution], flexShrink: 0 }}>{e.resolution}</span>
        </div>
      ))}
    </div>
  )
}
