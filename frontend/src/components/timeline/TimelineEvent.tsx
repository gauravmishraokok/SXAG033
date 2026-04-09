import React, { useState } from 'react'

interface Event {
  id?: string
  cube_id?: string
  type?: string
  event_type?: string
  content?: string
  label?: string
  timestamp?: string
  created_at?: string
  memory_type?: string
}

interface Props {
  event: Event
  isNew?: boolean
}

function eventColor(type: string) {
  if (type === 'created') return 'var(--accent-green)'
  if (type === 'updated') return 'var(--accent-blue)'
  if (type === 'quarantined') return 'var(--accent-amber)'
  if (type === 'resolved') return 'var(--accent-green)'
  if (type === 'evicted') return 'var(--text-dim)'
  return 'var(--text-secondary)'
}

function eventSize(type: string) {
  if (type === 'quarantined') return 12
  if (type === 'evicted') return 8
  return 10
}

function eventLabel(type: string) {
  const map: Record<string, string> = {
    created: 'created',
    updated: 'updated',
    quarantined: 'quarantined',
    resolved: 'resolved',
    evicted: 'evicted',
  }
  return map[type] ?? type
}

function typeBadgeColor(memType: string) {
  if (memType === 'episodic') return 'var(--accent-purple)'
  if (memType === 'semantic') return 'var(--accent-teal)'
  return 'var(--accent-orange)'
}

export function TimelineEvent({ event, isNew }: Props) {
  const [showTooltip, setShowTooltip] = useState(false)
  const type = (event.event_type ?? event.type ?? 'created').toLowerCase()
  const memType = (event.memory_type ?? 'episodic').toLowerCase()
  const ts = event.timestamp ?? event.created_at ?? ''
  const content = event.content ?? event.label ?? event.cube_id ?? ''
  const id = event.cube_id ?? event.id ?? ''

  const color = eventColor(type)
  const size = eventSize(type)
  const timeStr = ts ? new Date(ts).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) : ''

  return (
    <div
      style={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        flexShrink: 0,
        width: 90,
        position: 'relative',
        animation: isNew ? 'slide-in-right 0.3s ease-out' : undefined,
      }}
      onMouseEnter={() => setShowTooltip(true)}
      onMouseLeave={() => setShowTooltip(false)}
    >
      {/* Dot */}
      <div style={{
        width: size, height: size,
        borderRadius: '50%',
        background: color,
        marginBottom: 6,
        flexShrink: 0,
      }} />

      {/* Labels */}
      <div style={{ fontFamily: 'var(--font-mono)', fontSize: 9, color: 'var(--text-dim)', textAlign: 'center', marginBottom: 3 }}>
        {timeStr}
      </div>
      <div style={{
        fontFamily: 'var(--font-display)',
        fontSize: 9,
        fontWeight: 700,
        letterSpacing: '0.06em',
        color,
        textAlign: 'center',
        textTransform: 'uppercase',
        marginBottom: 3,
      }}>
        {eventLabel(type)}
      </div>
      {memType && (
        <div style={{
          fontFamily: 'var(--font-mono)',
          fontSize: 9,
          color: typeBadgeColor(memType),
          textAlign: 'center',
          marginBottom: 3,
        }}>
          [{memType.toUpperCase().slice(0, 8)}]
        </div>
      )}
      <div style={{
        fontFamily: 'var(--font-mono)',
        fontSize: 9,
        color: 'var(--text-dim)',
        textAlign: 'center',
        maxWidth: 82,
        overflow: 'hidden',
        textOverflow: 'ellipsis',
        whiteSpace: 'nowrap',
      }}>
        {content.slice(0, 14)}{content.length > 14 ? '…' : ''}
      </div>

      {/* Tooltip */}
      {showTooltip && (
        <div style={{
          position: 'absolute',
          bottom: '100%',
          left: '50%',
          transform: 'translateX(-50%)',
          marginBottom: 8,
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
          boxShadow: '0 4px 20px rgba(0,0,0,0.5)',
        }}>
          <div>id: {id.slice(0, 12)}</div>
          <div>event: {type}</div>
          <div>time: {timeStr}</div>
          <div style={{ maxWidth: 200, whiteSpace: 'normal' }}>{content.slice(0, 80)}</div>
        </div>
      )}
    </div>
  )
}
