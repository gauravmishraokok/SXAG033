import React, { useState, useEffect, useRef } from 'react'
import { useCourtQueue } from '../../hooks/useCourtQueue'
import { useCourtStore } from '../../store'
import { ContradictionCard } from './ContradictionCard'
import { CourtHistory, CourtHistoryEntry } from './CourtHistory'
import { useQueryClient } from '@tanstack/react-query'

export function CourtPanel() {
  const { data, refetch } = useCourtQueue()
  const { pendingCount, hasAlert } = useCourtStore()
  const [history, setHistory] = useState<CourtHistoryEntry[]>([])
  const panelRef = useRef<HTMLDivElement>(null)
  const qc = useQueryClient()

  const items: any[] = Array.isArray(data) ? data : (data?.items ?? [])

  // Court alert animation on panel border
  useEffect(() => {
    if (!hasAlert || !panelRef.current) return
    panelRef.current.style.animation = 'court-alert 0.5s ease 4'
    const t = setTimeout(() => {
      if (panelRef.current) panelRef.current.style.animation = ''
    }, 2000)
    return () => clearTimeout(t)
  }, [hasAlert])

  function handleResolved(item: any) {
    const id = item.id ?? item.quarantine_id ?? ''
    const label = (item.incoming_memory?.content ?? item.incoming?.content ?? id).slice(0, 24)
    const time = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    setHistory((prev) => [{ id, label, time, resolution: 'accept' as const }, ...prev].slice(0, 5))
    refetch()
    qc.invalidateQueries({ queryKey: ['court-queue'] })
  }

  const isEmpty = pendingCount === 0

  return (
    <div ref={panelRef} style={{ border: '1px solid transparent', borderRadius: 0, height: '100%', display: 'flex', flexDirection: 'column' }}>
      {/* Header */}
      <div className="panel-header">
        <span style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
          <span>⚖ Memory Court</span>
        </span>
        {isEmpty ? (
          <span style={{ display: 'flex', alignItems: 'center', gap: 5, fontFamily: 'var(--font-mono)', fontSize: 10, color: 'var(--accent-green)' }}>
            <span style={{ width: 6, height: 6, borderRadius: '50%', background: 'var(--accent-green)', display: 'inline-block' }} />
            ALL CLEAR
          </span>
        ) : (
          <span style={{ display: 'flex', alignItems: 'center', gap: 5, fontFamily: 'var(--font-mono)', fontSize: 10, color: 'var(--accent-amber)', animation: 'pulse-glow 0.8s infinite' }}>
            ⚠ {pendingCount} PENDING
          </span>
        )}
      </div>

      {/* Queue */}
      <div style={{ flex: 1, overflow: 'auto' }}>
        {isEmpty && (
          <div style={{
            padding: 24,
            textAlign: 'center',
            fontFamily: 'var(--font-mono)',
            fontSize: 11,
            color: 'var(--text-ghost)',
          }}>
            No contradictions detected
          </div>
        )}

        {items.map((item: any) => (
          <ContradictionCard
            key={item.id ?? item.quarantine_id}
            item={item}
            onResolved={() => handleResolved(item)}
          />
        ))}
      </div>

      <CourtHistory entries={history} />
    </div>
  )
}
