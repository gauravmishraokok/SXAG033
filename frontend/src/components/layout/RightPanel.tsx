import React from 'react'
import { CourtPanel } from '../court/CourtPanel'

export function RightPanel() {
  return (
    <div className="panel-scroll" style={{ background: 'var(--bg-surface)' }}>
      <CourtPanel />
    </div>
  )
}
