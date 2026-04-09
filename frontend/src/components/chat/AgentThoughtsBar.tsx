import React from 'react'
import { useChatStore } from '../../store'

export function AgentThoughtsBar() {
  const { agentThoughts, isStreaming } = useChatStore()
  const text = agentThoughts || 'Stand by for input'
  const active = isStreaming && !!agentThoughts

  return (
    <div style={{
      padding: '8px 16px',
      background: 'var(--bg-surface-2)',
      borderBottom: '1px solid var(--border-dim)',
      display: 'flex',
      alignItems: 'center',
      gap: 10,
      flexShrink: 0,
    }}>
      <span style={{ fontSize: 14 }}>🧠</span>
      <span style={{
        fontFamily: 'var(--font-mono)',
        fontSize: 11,
        color: active ? 'var(--accent-cyan)' : 'var(--text-ghost)',
        flex: 1,
      }}>
        {text}
      </span>
      {active && (
        <span style={{
          fontFamily: 'var(--font-mono)',
          fontSize: 11,
          color: 'var(--accent-cyan)',
          display: 'flex',
          alignItems: 'center',
          gap: 4,
        }}>
          <span style={{
            display: 'inline-block',
            animation: 'spin 1s linear infinite',
            fontSize: 12,
          }}>◌</span>
          active
        </span>
      )}
    </div>
  )
}
