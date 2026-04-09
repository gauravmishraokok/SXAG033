import React, { useEffect, useRef } from 'react'
import { useChatStore } from '../../store'
import { AgentThoughtsBar } from './AgentThoughtsBar'
import { MessageBubble } from './MessageBubble'
import { ChatInput } from './ChatInput'

export function ChatPanel() {
  const { messages, isStreaming } = useChatStore()
  const bottomRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  return (
    <>
      <div className="panel-header">
        <span>Conversation</span>
        <span style={{ fontFamily: 'var(--font-mono)', fontSize: 9, color: 'var(--text-dim)' }}>
          {messages.length} msg{messages.length !== 1 ? 's' : ''}
        </span>
      </div>

      <AgentThoughtsBar />

      {/* Messages */}
      <div style={{ flex: 1, overflow: 'auto', padding: '16px 16px 8px' }}>
        {messages.length === 0 && (
          <div style={{
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            justifyContent: 'center',
            height: '100%',
            gap: 12,
          }}>
            <div style={{
              fontFamily: 'var(--font-display)',
              fontSize: 28,
              fontWeight: 800,
              letterSpacing: '0.12em',
              color: 'var(--text-ghost)',
            }}>MEMORA</div>
            <div style={{
              fontFamily: 'var(--font-mono)',
              fontSize: 11,
              color: 'var(--text-ghost)',
            }}>Neural memory OS — start a conversation</div>
          </div>
        )}

        {messages.map((msg, i) => (
          <MessageBubble
            key={msg.id}
            message={msg}
            isStreaming={isStreaming && i === messages.length - 1 && msg.role === 'assistant'}
          />
        ))}
        <div ref={bottomRef} />
      </div>

      <ChatInput />
    </>
  )
}
