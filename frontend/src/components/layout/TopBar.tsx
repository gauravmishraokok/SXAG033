import React, { useState } from 'react'
import { useChatStore, useCourtStore } from '../../store'
import { createSession } from '../../api/chat'

export function TopBar() {
  const { sessionId, setSession, clear } = useChatStore()
  const { pendingCount } = useCourtStore()
  const isStreaming = useChatStore((s) => s.isStreaming)
  const [copied, setCopied] = useState(false)

  const turnCount = useChatStore((s) => s.messages.filter((m) => m.role === 'user').length)
  const memoriesCount = 0 // will be overridden by memory hook via prop drilling or separate context

  const shortId = sessionId ? sessionId.slice(0, 8) : '--------'

  function copySession() {
    if (!sessionId) return
    navigator.clipboard.writeText(sessionId)
    setCopied(true)
    setTimeout(() => setCopied(false), 1500)
  }

  async function handleNewSession() {
    try {
      const res = await createSession()
      const newId = res.session_id ?? res.id ?? crypto.randomUUID()
      setSession(newId)
      localStorage.setItem('memora_session_id', newId)
      clear()
    } catch {
      const newId = crypto.randomUUID()
      setSession(newId)
      localStorage.setItem('memora_session_id', newId)
      clear()
    }
  }

  const statusColor = isStreaming ? 'var(--accent-cyan)' : 'var(--accent-green)'
  const statusAnim = isStreaming ? 'pulse-glow 0.8s infinite' : 'none'
  const statusLabel = isStreaming ? 'Processing' : 'Active'

  return (
    <div style={{
      height: 56,
      background: 'var(--bg-surface)',
      borderBottom: '1px solid var(--border-dim)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      padding: '0 20px',
      flexShrink: 0,
    }}>
      {/* Left: Branding */}
      <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
        <div style={{
          width: 8, height: 8, borderRadius: '50%',
          background: 'var(--accent-cyan)',
          animation: 'pulse-glow 2s infinite',
          flexShrink: 0,
        }} />
        <div>
          <div style={{
            fontFamily: 'var(--font-display)',
            fontWeight: 800,
            fontSize: 17,
            letterSpacing: '0.12em',
            color: 'var(--text-primary)',
          }}>MEMORA</div>
          <div style={{
            fontFamily: 'var(--font-mono)',
            fontSize: 10,
            color: 'var(--text-dim)',
            marginTop: -2,
          }}>v0.1 · neural-os</div>
        </div>
      </div>

      {/* Center: Session status */}
      <div style={{
        display: 'flex', alignItems: 'center', gap: 12,
        fontFamily: 'var(--font-mono)', fontSize: 11,
        color: 'var(--text-secondary)',
      }}>
        <span>SESSION</span>
        <span
          title={sessionId ?? ''}
          onClick={copySession}
          style={{ cursor: 'pointer', color: 'var(--accent-blue)', textDecoration: copied ? 'underline' : 'none' }}
        >
          {copied ? 'Copied!' : shortId}
        </span>
        <span style={{ color: 'var(--text-ghost)' }}>·</span>
        <span>Turn {turnCount}</span>
        <span style={{ color: 'var(--text-ghost)' }}>·</span>
        <span style={{ display: 'flex', alignItems: 'center', gap: 5 }}>
          <span style={{
            width: 7, height: 7, borderRadius: '50%',
            background: statusColor,
            display: 'inline-block',
            animation: statusAnim,
          }} />
          {statusLabel}
        </span>
      </div>

      {/* Right: Counters + New Session */}
      <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
        {pendingCount > 0 && (
          <div style={{
            display: 'flex', alignItems: 'center', gap: 5,
            padding: '3px 10px',
            border: '1px solid var(--accent-amber)',
            borderRadius: 4,
            background: 'rgba(245,166,35,0.15)',
            color: 'var(--accent-amber)',
            fontFamily: 'var(--font-mono)',
            fontSize: 11,
            animation: 'pulse-glow 1s infinite',
          }}>
            ⚠ {pendingCount}
          </div>
        )}

        <button
          onClick={handleNewSession}
          style={{
            fontFamily: 'var(--font-display)',
            fontSize: 11,
            fontWeight: 600,
            letterSpacing: '0.06em',
            border: '1px solid var(--border-base)',
            borderRadius: 4,
            background: 'transparent',
            color: 'var(--text-secondary)',
            padding: '5px 12px',
            cursor: 'pointer',
            transition: 'background 0.15s',
          }}
          onMouseEnter={(e) => (e.currentTarget.style.background = 'var(--bg-surface-3)')}
          onMouseLeave={(e) => (e.currentTarget.style.background = 'transparent')}
        >
          ≡ New Session
        </button>
      </div>
    </div>
  )
}
