import React, { useEffect, useRef, useState } from 'react'

interface Props {
  memories: any[]
}

function useAnimatedCount(target: number) {
  const [display, setDisplay] = useState(target)
  const prev = useRef(target)
  useEffect(() => {
    if (prev.current === target) return
    const start = prev.current
    const diff = target - start
    const duration = 400
    const startTime = Date.now()
    function tick() {
      const elapsed = Date.now() - startTime
      const progress = Math.min(elapsed / duration, 1)
      setDisplay(Math.round(start + diff * progress))
      if (progress < 1) requestAnimationFrame(tick)
    }
    requestAnimationFrame(tick)
    prev.current = target
  }, [target])
  return display
}

export function MemoryStatsBar({ memories }: Props) {
  const total = useAnimatedCount(memories.length)

  const episodic = memories.filter((m) => (m.type ?? m.memory_type ?? '').toLowerCase() === 'episodic').length
  const semantic  = memories.filter((m) => (m.type ?? m.memory_type ?? '').toLowerCase() === 'semantic').length
  const kg        = memories.filter((m) => ['kg_node', 'kg'].includes((m.type ?? m.memory_type ?? '').toLowerCase())).length

  const hot  = memories.filter((m) => (m.tier ?? '').toLowerCase() === 'hot').length
  const warm = memories.filter((m) => (m.tier ?? '').toLowerCase() === 'warm').length
  const cold = memories.length - hot - warm

  const hotW  = memories.length > 0 ? (hot  / memories.length) * 100 : 0
  const warmW = memories.length > 0 ? (warm / memories.length) * 100 : 0
  const coldW = memories.length > 0 ? (cold / memories.length) * 100 : 0

  return (
    <div style={{
      borderTop: '1px solid var(--border-dim)',
      background: 'var(--bg-surface)',
      padding: '10px 12px',
      flexShrink: 0,
    }}>
      <div style={{ fontFamily: 'var(--font-mono)', fontSize: 11, color: 'var(--text-secondary)', marginBottom: 8 }}>
        ⬡ {total} total {total === 1 ? 'memory' : 'memories'}
      </div>

      {/* Stacked tier bar */}
      <div style={{ height: 8, borderRadius: 4, overflow: 'hidden', display: 'flex', marginBottom: 8 }}>
        <div style={{ width: `${hotW}%`, background: 'var(--tier-hot)', transition: 'width 0.4s ease' }} />
        <div style={{ width: `${warmW}%`, background: 'var(--tier-warm)', transition: 'width 0.4s ease' }} />
        <div style={{ width: `${coldW}%`, background: 'var(--tier-cold)', transition: 'width 0.4s ease' }} />
      </div>
      <div style={{ display: 'flex', gap: 10, marginBottom: 8 }}>
        {[['HOT', hot, 'var(--tier-hot)'], ['WARM', warm, 'var(--tier-warm)'], ['COLD', cold, 'var(--tier-cold)']].map(([label, count, color]) => (
          <span key={label as string} style={{ fontFamily: 'var(--font-mono)', fontSize: 9, color: color as string }}>
            {label} {count}
          </span>
        ))}
      </div>

      {/* Type row */}
      <div style={{ display: 'flex', gap: 12 }}>
        {[
          ['■', 'EPISODIC', episodic, 'var(--accent-purple)'],
          ['■', 'SEMANTIC', semantic, 'var(--accent-teal)'],
          ['■', 'KG', kg, 'var(--accent-orange)'],
        ].map(([icon, label, count, color]) => (
          <span key={label as string} style={{ fontFamily: 'var(--font-display)', fontSize: 11, color: 'var(--text-secondary)' }}>
            <span style={{ color: color as string }}>{icon}</span> {label} {count}
          </span>
        ))}
      </div>
    </div>
  )
}
