import React from 'react'
import { ChatMessage } from '../../store/chatStore'
import { MemoryBadge } from './MemoryBadge'
import { FeedbackRow } from './FeedbackRow'
import { useChat } from '../../hooks/useChat'

interface Props {
  message: ChatMessage
  isStreaming?: boolean
}

export function MessageBubble({ message, isStreaming }: Props) {
  const { sendMessage } = useChat()
  const isUser = message.role === 'user'

  function handleFeedback(text: string) {
    sendMessage(text, text)
  }

  if (isUser) {
    return (
      <div style={{ display: 'flex', justifyContent: 'flex-end', marginBottom: 12 }}>
        <div style={{
          maxWidth: '70%',
          background: 'var(--bg-surface-3)',
          border: '1px solid var(--border-base)',
          borderRadius: '12px 12px 2px 12px',
          padding: '10px 14px',
          fontFamily: 'var(--font-body)',
          fontSize: 14,
          color: 'var(--text-primary)',
          lineHeight: 1.5,
        }}>
          {message.text}
        </div>
      </div>
    )
  }

  return (
    <div style={{ display: 'flex', justifyContent: 'flex-start', marginBottom: 12 }}>
      <div style={{ maxWidth: '78%' }}>
        <div style={{
          background: 'linear-gradient(135deg, var(--bg-surface) 0%, var(--bg-surface-2) 100%)',
          border: '1px solid var(--border-dim)',
          borderRadius: '2px 12px 12px 12px',
          padding: '12px 16px',
          fontFamily: 'var(--font-body)',
          fontSize: 14,
          color: 'var(--text-primary)',
          lineHeight: 1.6,
        }} className={isStreaming ? 'streaming' : ''}>
          {message.text}
        </div>

        {/* Memory badges */}
        {message.memoriesUsed && message.memoriesUsed.length > 0 && (
          <div style={{ marginTop: 6, display: 'flex', flexWrap: 'wrap', gap: 4, paddingLeft: 4 }}>
            <span style={{ fontFamily: 'var(--font-body)', fontSize: 11, color: 'var(--text-dim)', marginRight: 4 }}>Used:</span>
            {message.memoriesUsed.map((id) => (
              <MemoryBadge key={id} cubeId={id} type="episodic" />
            ))}
          </div>
        )}

        {/* Feedback */}
        <div style={{ paddingLeft: 4 }}>
          <FeedbackRow
            memoriesUsed={message.memoriesUsed ?? []}
            onFeedback={handleFeedback}
          />
        </div>
      </div>
    </div>
  )
}
