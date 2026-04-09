import React from 'react'
import { useUIStore } from '../../store'

const TYPES = [
  { id: 'episodic', label: 'EPISODIC', color: 'var(--accent-purple)' },
  { id: 'semantic', label: 'SEMANTIC', color: 'var(--accent-teal)' },
  { id: 'kg_node',  label: 'KG',       color: 'var(--accent-orange)' },
]

export function TypeFilterPills() {
  const { memoryFilter, toggleFilter } = useUIStore()
  const allActive = memoryFilter.size === 0

  return (
    <div style={{ display: 'flex', gap: 6, alignItems: 'center', flexWrap: 'wrap' }}>
      <button
        onClick={() => { TYPES.forEach((t) => { if (memoryFilter.has(t.id)) toggleFilter(t.id) }) }}
        style={{
          fontFamily: 'var(--font-mono)',
          fontSize: 10,
          fontWeight: 500,
          border: '1px solid var(--border-base)',
          borderRadius: 3,
          background: allActive ? 'rgba(255,255,255,0.08)' : 'transparent',
          color: allActive ? 'var(--text-primary)' : 'var(--text-dim)',
          padding: '2px 8px',
          cursor: 'pointer',
        }}
      >ALL</button>
      {TYPES.map((t) => {
        const active = memoryFilter.has(t.id)
        return (
          <button
            key={t.id}
            onClick={() => toggleFilter(t.id)}
            style={{
              fontFamily: 'var(--font-mono)',
              fontSize: 10,
              fontWeight: 500,
              border: `1px solid ${t.color}`,
              borderRadius: 3,
              background: active ? `${t.color}33` : 'transparent',
              color: active ? t.color : 'var(--text-dim)',
              padding: '2px 8px',
              cursor: 'pointer',
            }}
          >
            {t.label}
          </button>
        )
      })}
    </div>
  )
}
