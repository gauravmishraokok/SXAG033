import React, { useEffect } from 'react'
import { TopBar } from './TopBar'
import { LeftPanel } from './LeftPanel'
import { CenterPanel } from './CenterPanel'
import { RightPanel } from './RightPanel'
import { BottomBar } from './BottomBar'
import { useChatStore } from '../../store'
import { createSession } from '../../api/chat'

export function Shell() {
  const { sessionId, setSession } = useChatStore()

  useEffect(() => {
    if (sessionId) return
    const stored = localStorage.getItem('memora_session_id')
    if (stored) {
      setSession(stored)
      return
    }
    createSession()
      .then((res) => {
        const id = res.session_id ?? res.id ?? crypto.randomUUID()
        setSession(id)
        localStorage.setItem('memora_session_id', id)
      })
      .catch(() => {
        const id = crypto.randomUUID()
        setSession(id)
        localStorage.setItem('memora_session_id', id)
      })
  }, [])

  return (
    <div className="shell">
      <TopBar />
      <div className="main-grid">
        <LeftPanel />
        <CenterPanel />
        <RightPanel />
      </div>
      <BottomBar />
    </div>
  )
}
