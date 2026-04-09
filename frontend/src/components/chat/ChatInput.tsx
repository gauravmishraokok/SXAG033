import React, { useRef, useState, useCallback } from 'react'
import { useChat } from '../../hooks/useChat'
import { useChatStore } from '../../store'

export function ChatInput() {
  const [text, setText] = useState('')
  const { sendMessage, isStreaming } = useChat()
  const textareaRef = useRef<HTMLTextAreaElement>(null)

  function adjustHeight() {
    const el = textareaRef.current
    if (!el) return
    el.style.height = 'auto'
    const lineH = 22
    const maxLines = 5
    el.style.height = Math.min(el.scrollHeight, lineH * maxLines) + 'px'
  }

  function handleChange(e: React.ChangeEvent<HTMLTextAreaElement>) {
    setText(e.target.value)
    adjustHeight()
  }

  async function handleSend() {
    const trimmed = text.trim()
    if (!trimmed || isStreaming) return
    setText('')
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto'
    }
    await sendMessage(trimmed)
  }

  function handleKeyDown(e: React.KeyboardEvent) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  return (
    <div style={{
      padding: '10px 16px 14px',
      borderTop: '1px solid var(--border-dim)',
      background: 'var(--bg-surface)',
      flexShrink: 0,
    }}>
      <div style={{
        border: '1px solid var(--border-base)',
        borderRadius: 8,
        background: 'var(--bg-surface-2)',
        overflow: 'hidden',
        transition: 'border-color 0.15s',
      }}
        onFocusCapture={(e) => (e.currentTarget.style.borderColor = 'var(--accent-blue)')}
        onBlurCapture={(e) => (e.currentTarget.style.borderColor = 'var(--border-base)')}
      >
        <textarea
          ref={textareaRef}
          value={text}
          onChange={handleChange}
          onKeyDown={handleKeyDown}
          placeholder="Message MEMORA..."
          rows={1}
          style={{
            width: '100%',
            background: 'transparent',
            border: 'none',
            outline: 'none',
            resize: 'none',
            padding: '10px 14px',
            color: 'var(--text-primary)',
            fontFamily: 'var(--font-body)',
            fontSize: 14,
            lineHeight: '22px',
            minHeight: 42,
          }}
        />
        <div style={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          padding: '6px 14px 8px',
          borderTop: '1px solid var(--border-dim)',
        }}>
          <button
            onClick={handleSend}
            disabled={isStreaming || !text.trim()}
            style={{
              background: isStreaming || !text.trim() ? 'var(--bg-surface-3)' : 'var(--accent-blue)',
              border: 'none',
              borderRadius: 6,
              color: isStreaming || !text.trim() ? 'var(--text-dim)' : '#fff',
              fontFamily: 'var(--font-display)',
              fontSize: 12,
              fontWeight: 600,
              padding: '5px 14px',
              cursor: isStreaming || !text.trim() ? 'default' : 'pointer',
              display: 'flex',
              alignItems: 'center',
              gap: 6,
              transition: 'background 0.15s',
            }}
          >
            {isStreaming ? (
              <span style={{ display: 'inline-block', animation: 'spin 1s linear infinite', fontSize: 12 }}>◌</span>
            ) : '↑'} Send
          </button>
          <span style={{ fontFamily: 'var(--font-mono)', fontSize: 10, color: 'var(--text-dim)' }}>
            Shift+Enter for newline
          </span>
        </div>
      </div>
    </div>
  )
}
