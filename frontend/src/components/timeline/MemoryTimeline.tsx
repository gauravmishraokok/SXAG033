import React, { useEffect, useRef, useState } from 'react'
import { useTimeline } from '../../hooks/useTimeline'
import { TimelineEvent } from './TimelineEvent'

export function MemoryTimeline() {
  const { data, isLoading, isError } = useTimeline()
  const scrollRef = useRef<HTMLDivElement>(null)
  const seenIdsRef = useRef<Set<string>>(new Set())
  const [newIds, setNewIds] = useState<Set<string>>(new Set())

  const events: any[] = Array.isArray(data) ? data : (data?.events ?? data?.items ?? [])
  const sorted = [...events].sort((a, b) => {
    const ta = new Date(a.timestamp ?? a.created_at ?? 0).getTime()
    const tb = new Date(b.timestamp ?? b.created_at ?? 0).getTime()
    return ta - tb
  })

  // Detect new events + auto-scroll
  useEffect(() => {
    if (!sorted.length) return
    const justNew = new Set<string>()
    sorted.forEach((e: any) => {
      const id = e.id ?? e.cube_id ?? ''
      if (id && !seenIdsRef.current.has(id)) {
        justNew.add(id)
        seenIdsRef.current.add(id)
      }
    })
    if (justNew.size > 0) {
      setNewIds(justNew)
      setTimeout(() => setNewIds(new Set()), 1000)
      // Auto-scroll to right
      setTimeout(() => {
        scrollRef.current?.scrollTo({ left: scrollRef.current.scrollWidth, behavior: 'smooth' })
      }, 100)
    }
  }, [events.length])

  if (isError) {
    return (
      <div style={{ padding: 16, fontFamily: 'var(--font-mono)', fontSize: 11, color: 'var(--accent-red)' }}>
        ⚠ Cannot reach /timeline endpoint
      </div>
    )
  }

  return (
    <div style={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
      {/* Timeline axis */}
      <div style={{ padding: '4px 16px', fontFamily: 'var(--font-mono)', fontSize: 9, color: 'var(--text-ghost)', borderBottom: '1px solid var(--border-dim)', flexShrink: 0 }}>
        ← earlier ──────────────────────────────────────────────── now →
      </div>

      <div
        ref={scrollRef}
        style={{
          flex: 1,
          overflowX: 'auto',
          overflowY: 'hidden',
          display: 'flex',
          alignItems: 'flex-start',
          padding: '16px 20px',
          gap: 24,
        }}
      >
        {/* Connector line */}
        {sorted.length > 0 && (
          <div style={{
            position: 'absolute',
            top: 44,
            left: 20,
            right: 20,
            height: 1,
            background: 'var(--border-dim)',
            pointerEvents: 'none',
          }} />
        )}

        {isLoading && sorted.length === 0 && (
          <div style={{ fontFamily: 'var(--font-mono)', fontSize: 11, color: 'var(--text-ghost)', animation: 'pulse-glow 1.5s infinite', alignSelf: 'center' }}>
            Loading timeline...
          </div>
        )}
        {!isLoading && sorted.length === 0 && (
          <div style={{ fontFamily: 'var(--font-mono)', fontSize: 11, color: 'var(--text-ghost)', alignSelf: 'center' }}>
            No timeline events yet
          </div>
        )}

        {sorted.map((event: any) => {
          const id = event.id ?? event.cube_id ?? ''
          return (
            <TimelineEvent
              key={id || Math.random()}
              event={event}
              isNew={newIds.has(id)}
            />
          )
        })}
      </div>
    </div>
  )
}
