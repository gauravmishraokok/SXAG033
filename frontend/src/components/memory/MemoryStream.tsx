import React, { useRef, useState, useEffect } from 'react'
import { useMemories } from '../../hooks/useMemories'
import { useUIStore } from '../../store'
import { MemoryCard } from './MemoryCard'
import { TypeFilterPills } from './TypeFilterPills'
import { MemoryStatsBar } from './MemoryStatsBar'

export function MemoryStream() {
  const { data, isLoading, isError } = useMemories()
  const { memoryFilter } = useUIStore()
  const seenIdsRef = useRef<Set<string>>(new Set())
  const [newIds, setNewIds] = useState<Set<string>>(new Set())

  const raw: any[] = Array.isArray(data) ? data : (data?.memories ?? data?.items ?? [])

  // Detect new memories
  useEffect(() => {
    if (!raw.length) return
    const justNew = new Set<string>()
    raw.forEach((m: any) => {
      const id = m.cube_id ?? m.id ?? ''
      if (id && !seenIdsRef.current.has(id)) {
        justNew.add(id)
        seenIdsRef.current.add(id)
      }
    })
    if (justNew.size > 0) {
      setNewIds(justNew)
      setTimeout(() => setNewIds(new Set()), 1200)
    }
  }, [raw])

  // Filter
  const filtered = memoryFilter.size === 0
    ? raw
    : raw.filter((m: any) => memoryFilter.has((m.type ?? m.memory_type ?? '').toLowerCase()))

  return (
    <>
      {/* Panel header */}
      <div className="panel-header" style={{ flexDirection: 'column', alignItems: 'flex-start', gap: 8 }}>
        <div style={{ display: 'flex', width: '100%', justifyContent: 'space-between', alignItems: 'center' }}>
          <span>Memory Stream</span>
          <span style={{
            display: 'flex', alignItems: 'center', gap: 4,
            fontFamily: 'var(--font-mono)', fontSize: 9,
            color: 'var(--accent-green)',
          }}>
            <span style={{ width: 6, height: 6, borderRadius: '50%', background: 'var(--accent-green)', display: 'inline-block', animation: 'pulse-glow 2s infinite' }} />
            live
          </span>
        </div>
        <TypeFilterPills />
      </div>

      {/* Cards */}
      <div style={{ flex: 1, overflow: 'auto' }}>
        {isLoading && !raw.length && (
          <SkeletonCards />
        )}
        {isError && (
          <ErrorState message="Cannot reach /memories endpoint" />
        )}
        {filtered.length === 0 && !isLoading && !isError && (
          <div style={{ padding: 24, textAlign: 'center', fontFamily: 'var(--font-mono)', fontSize: 11, color: 'var(--text-ghost)' }}>
            No memories yet — start a conversation
          </div>
        )}
        {filtered.map((memory: any) => {
          const id = memory.cube_id ?? memory.id ?? ''
          return (
            <MemoryCard
              key={id}
              memory={memory}
              isNew={newIds.has(id)}
            />
          )
        })}
      </div>

      <MemoryStatsBar memories={raw} />
    </>
  )
}

function SkeletonCards() {
  return (
    <>
      {[1, 2, 3].map((i) => (
        <div key={i} style={{
          margin: '6px 8px',
          padding: 12,
          background: 'var(--bg-surface-2)',
          borderRadius: 4,
          borderLeft: '3px solid var(--border-bright)',
          animation: 'pulse-glow 1.5s infinite',
        }}>
          <div style={{ height: 10, background: 'var(--bg-surface-3)', borderRadius: 2, width: '40%', marginBottom: 8 }} />
          <div style={{ height: 10, background: 'var(--bg-surface-3)', borderRadius: 2, width: '90%', marginBottom: 4 }} />
          <div style={{ height: 10, background: 'var(--bg-surface-3)', borderRadius: 2, width: '70%' }} />
        </div>
      ))}
    </>
  )
}

function ErrorState({ message }: { message: string }) {
  return (
    <div style={{
      margin: 12,
      padding: 12,
      border: '1px solid rgba(255,71,87,0.3)',
      borderRadius: 4,
      background: 'rgba(255,71,87,0.05)',
      fontFamily: 'var(--font-mono)',
      fontSize: 11,
      color: 'var(--accent-red)',
    }}>
      ⚠ {message}
    </div>
  )
}
