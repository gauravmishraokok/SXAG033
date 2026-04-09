import React from 'react'
import { MemoryStream } from '../memory/MemoryStream'

export function LeftPanel() {
  return (
    <div className="panel-scroll" style={{ background: 'var(--bg-surface)', position: 'relative' }}>
      <MemoryStream />
    </div>
  )
}
