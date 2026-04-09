import React from 'react'

interface Props {
  score: number
  threshold?: number
}

export function ScoreBar({ score, threshold = 0.75 }: Props) {
  const fillColor = score >= threshold ? 'var(--accent-red)' : 'var(--accent-amber)'
  const fillGlow = score >= threshold ? 'var(--glow-red)' : 'var(--glow-amber)'
  const thresholdPct = threshold * 100

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 4 }}>
        <span style={{ fontFamily: 'var(--font-display)', fontSize: 9, letterSpacing: '0.1em', color: 'var(--text-dim)' }}>
          CONTRADICTION SCORE
        </span>
        <span style={{ fontFamily: 'var(--font-mono)', fontSize: 11, color: fillColor }}>
          {score.toFixed(2)}
        </span>
      </div>

      <div style={{ position: 'relative', height: 6, background: 'var(--bg-surface-3)', borderRadius: 3 }}>
        {/* Fill */}
        <div style={{
          position: 'absolute',
          left: 0, top: 0, bottom: 0,
          width: `${Math.min(score * 100, 100)}%`,
          background: fillColor,
          boxShadow: score >= threshold ? fillGlow : undefined,
          borderRadius: 3,
          transition: 'width 0.4s ease',
        }} />

        {/* Threshold marker */}
        <div style={{
          position: 'absolute',
          left: `${thresholdPct}%`,
          top: -4,
          bottom: -4,
          width: 1,
          background: 'rgba(255,255,255,0.5)',
        }} />
      </div>

      <div style={{ position: 'relative', marginTop: 2 }}>
        <span style={{
          position: 'absolute',
          left: `${thresholdPct}%`,
          transform: 'translateX(-50%)',
          fontFamily: 'var(--font-mono)',
          fontSize: 9,
          color: 'var(--text-dim)',
        }}>▲ threshold {threshold.toFixed(2)}</span>
      </div>
    </div>
  )
}
