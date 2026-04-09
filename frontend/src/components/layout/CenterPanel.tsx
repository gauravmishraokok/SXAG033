import React from 'react'
import { ChatPanel } from '../chat/ChatPanel'

export function CenterPanel() {
  return (
    <div className="panel-scroll" style={{ background: 'var(--bg-base)', display: 'flex', flexDirection: 'column' }}>
      <ChatPanel />
    </div>
  )
}
