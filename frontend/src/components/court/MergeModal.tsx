import React, { useState } from 'react'

interface Props {
  suggestedContent?: string
  onConfirm: (merged: string) => void
  onCancel: () => void
}

export function MergeModal({ suggestedContent = '', onConfirm, onCancel }: Props) {
  const [text, setText] = useState(suggestedContent)

  return (
    <div style={{
      position: 'fixed',
      inset: 0,
      background: 'rgba(5,5,7,0.85)',
      backdropFilter: 'blur(8px)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      zIndex: 1000,
      animation: 'fadeIn 0.2s ease',
    }}>
      <div style={{
        background: 'var(--bg-surface)',
        border: '1px solid var(--border-base)',
        borderRadius: 8,
        padding: '20px 24px',
        width: 480,
        maxWidth: '90vw',
      }}>
        <div style={{
          fontFamily: 'var(--font-display)',
          fontSize: 14,
          fontWeight: 700,
          letterSpacing: '0.1em',
          color: 'var(--accent-amber)',
          marginBottom: 12,
        }}>⟳ MERGE MEMORIES</div>

        <div style={{
          fontFamily: 'var(--font-body)',
          fontSize: 12,
          color: 'var(--text-secondary)',
          marginBottom: 8,
        }}>Edit the merged version:</div>

        <textarea
          value={text}
          onChange={(e) => setText(e.target.value)}
          rows={4}
          style={{
            width: '100%',
            background: 'var(--bg-surface-2)',
            border: '1px solid var(--border-base)',
            borderRadius: 4,
            color: 'var(--text-primary)',
            fontFamily: 'var(--font-mono)',
            fontSize: 12,
            padding: '8px 10px',
            resize: 'vertical',
            marginBottom: 14,
          }}
        />

        <div style={{ display: 'flex', justifyContent: 'flex-end', gap: 10 }}>
          <button
            onClick={onCancel}
            style={{
              background: 'transparent',
              border: '1px solid var(--border-base)',
              borderRadius: 6,
              color: 'var(--text-secondary)',
              fontFamily: 'var(--font-display)',
              fontSize: 12,
              padding: '6px 16px',
              cursor: 'pointer',
            }}
          >Cancel</button>
          <button
            onClick={() => onConfirm(text)}
            style={{
              background: 'rgba(245,166,35,0.15)',
              border: '1px solid var(--accent-amber)',
              borderRadius: 6,
              color: 'var(--accent-amber)',
              fontFamily: 'var(--font-display)',
              fontSize: 12,
              padding: '6px 16px',
              cursor: 'pointer',
            }}
          >Confirm Merge ⟳</button>
        </div>
      </div>
    </div>
  )
}
