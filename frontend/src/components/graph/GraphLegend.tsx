import React from 'react'

export function GraphLegend() {
  return (
    <div style={{
      position: 'absolute',
      bottom: 12,
      right: 12,
      background: 'rgba(17,19,24,0.9)',
      border: '1px solid var(--border-dim)',
      borderRadius: 6,
      padding: '8px 12px',
      fontFamily: 'var(--font-mono)',
      fontSize: 9,
      color: 'var(--text-dim)',
      lineHeight: 1.8,
      backdropFilter: 'blur(4px)',
    }}>
      <div style={{ display: 'flex', gap: 12, flexWrap: 'wrap' }}>
        {[
          ['var(--accent-purple)', 'EPISODIC'],
          ['var(--accent-teal)',   'SEMANTIC'],
          ['var(--accent-orange)', 'KG_NODE'],
        ].map(([color, label]) => (
          <span key={label} style={{ display: 'flex', alignItems: 'center', gap: 4 }}>
            <span style={{ width: 8, height: 8, borderRadius: '50%', background: color, display: 'inline-block' }} />
            {label}
          </span>
        ))}
      </div>
      <div style={{ display: 'flex', gap: 12, marginTop: 4 }}>
        {[
          ['var(--tier-hot)',  'HOT'],
          ['var(--tier-warm)', 'WARM'],
          ['var(--tier-cold)', 'COLD'],
        ].map(([color, label]) => (
          <span key={label} style={{ display: 'flex', alignItems: 'center', gap: 4 }}>
            <span style={{ width: 8, height: 8, borderRadius: '50%', border: `2px solid ${color}`, display: 'inline-block' }} />
            {label}
          </span>
        ))}
      </div>
      <div style={{ display: 'flex', gap: 12, marginTop: 4 }}>
        <span>── active</span>
        <span style={{ color: 'rgba(255,71,87,0.6)' }}>╌╌ deprecated</span>
      </div>
    </div>
  )
}
