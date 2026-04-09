import React from 'react'

interface Props {
  hot: number
  warm: number
  cold: number
}

export function TierBar({ hot, warm, cold }: Props) {
  const total = hot + warm + cold || 1
  const hotPct  = (hot  / total) * 100
  const warmPct = (warm / total) * 100
  const coldPct = (cold / total) * 100

  return (
    <div>
      <div style={{ height: 8, borderRadius: 4, overflow: 'hidden', display: 'flex', marginBottom: 4 }}>
        <div style={{ width: `${hotPct}%`, background: 'var(--tier-hot)', transition: 'width 0.4s ease' }} />
        <div style={{ width: `${warmPct}%`, background: 'var(--tier-warm)', transition: 'width 0.4s ease' }} />
        <div style={{ width: `${coldPct}%`, background: 'var(--tier-cold)', transition: 'width 0.4s ease' }} />
      </div>
      <div style={{ display: 'flex', gap: 10, fontFamily: 'var(--font-mono)', fontSize: 9 }}>
        <span style={{ color: 'var(--tier-hot)' }}>HOT {hot}</span>
        <span style={{ color: 'var(--tier-warm)' }}>WARM {warm}</span>
        <span style={{ color: 'var(--tier-cold)' }}>COLD {cold}</span>
      </div>
    </div>
  )
}
