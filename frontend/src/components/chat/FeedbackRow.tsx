import React, { useState } from 'react'
import { useUIStore, useChatStore } from '../../store'

interface Props {
  memoriesUsed: string[]
  onFeedback: (text: string) => void
  sourceTable?: Array<{ cube_id: string; type: string; score: number; tier: string }>
}

export function FeedbackRow({ memoriesUsed, onFeedback, sourceTable }: Props) {
  const { flashMemories } = useUIStore()
  const [mode, setMode] = useState<null | 'flag' | 'trace'>(null)
  const [feedbackText, setFeedbackText] = useState('')
  const [submitted, setSubmitted] = useState(false)

  function handleFlag() {
    setMode(mode === 'flag' ? null : 'flag')
  }

  function handleSubmit() {
    flashMemories(memoriesUsed)
    onFeedback(feedbackText)
    setSubmitted(true)
    setMode(null)
  }

  const btnStyle = {
    background: 'transparent',
    border: 'none',
    color: 'var(--text-dim)',
    fontFamily: 'var(--font-body)',
    fontSize: 11,
    cursor: 'pointer',
    padding: '2px 6px',
    borderRadius: 3,
    transition: 'color 0.15s',
  }

  return (
    <div style={{ marginTop: 6 }}>
      <div style={{ display: 'flex', gap: 4, alignItems: 'center' }}>
        <button style={btnStyle} onMouseEnter={(e) => (e.currentTarget.style.color = 'var(--accent-green)')} onMouseLeave={(e) => (e.currentTarget.style.color = 'var(--text-dim)')}>👍 Good</button>
        <button style={btnStyle} onClick={handleFlag} onMouseEnter={(e) => (e.currentTarget.style.color = 'var(--accent-red)')} onMouseLeave={(e) => (e.currentTarget.style.color = 'var(--text-dim)')}>
          {submitted ? '✓ Logged' : '👎 Flag as wrong'}
        </button>
        <button style={btnStyle} onClick={() => setMode(mode === 'trace' ? null : 'trace')} onMouseEnter={(e) => (e.currentTarget.style.color = 'var(--accent-blue)')} onMouseLeave={(e) => (e.currentTarget.style.color = 'var(--text-dim)')}>🔗 Trace sources</button>
      </div>

      {mode === 'flag' && (
        <div style={{ marginTop: 6, display: 'flex', gap: 6 }}>
          <input
            value={feedbackText}
            onChange={(e) => setFeedbackText(e.target.value)}
            placeholder="What was wrong?"
            style={{
              flex: 1,
              background: 'var(--bg-surface-3)',
              border: '1px solid var(--border-base)',
              borderRadius: 4,
              color: 'var(--text-primary)',
              fontFamily: 'var(--font-body)',
              fontSize: 11,
              padding: '4px 8px',
            }}
          />
          <button
            onClick={handleSubmit}
            style={{
              background: 'rgba(255,71,87,0.15)',
              border: '1px solid var(--accent-red)',
              borderRadius: 4,
              color: 'var(--accent-red)',
              fontFamily: 'var(--font-display)',
              fontSize: 11,
              padding: '4px 10px',
              cursor: 'pointer',
            }}
          >Submit</button>
        </div>
      )}

      {mode === 'trace' && sourceTable && sourceTable.length > 0 && (
        <div style={{ marginTop: 6, overflow: 'auto' }}>
          <table style={{
            width: '100%',
            fontFamily: 'var(--font-mono)',
            fontSize: 10,
            color: 'var(--text-secondary)',
            borderCollapse: 'collapse',
          }}>
            <thead>
              <tr style={{ color: 'var(--text-dim)' }}>
                <th style={{ textAlign: 'left', padding: '2px 8px 4px 0' }}>cube_id</th>
                <th style={{ textAlign: 'left', padding: '2px 8px 4px 0' }}>type</th>
                <th style={{ textAlign: 'left', padding: '2px 8px 4px 0' }}>score</th>
                <th style={{ textAlign: 'left', padding: '2px 0 4px 0' }}>tier</th>
              </tr>
            </thead>
            <tbody>
              {sourceTable.map((row) => (
                <tr key={row.cube_id}>
                  <td style={{ padding: '2px 8px 2px 0' }}>{row.cube_id.slice(0, 6)}</td>
                  <td style={{ padding: '2px 8px 2px 0' }}>{row.type}</td>
                  <td style={{ padding: '2px 8px 2px 0' }}>{row.score.toFixed(2)}</td>
                  <td style={{ padding: '2px 0' }}>{row.tier}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  )
}
