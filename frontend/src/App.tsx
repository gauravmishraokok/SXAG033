import { useEffect } from 'react'
import { api } from './api/client'
import { Shell } from './components/layout/Shell'
import { useChatStore } from './store/chatStore'

export default function App() {
  const { sessionId, setSession } = useChatStore()

  useEffect(() => {
    const stored = localStorage.getItem('memora_session_id')
    if (stored) {
      setSession(stored)
      return
    }
    api.post('/chat/session', {}).then((data) => {
      setSession(data.session_id)
      localStorage.setItem('memora_session_id', data.session_id)
    }).catch(() => {
      // Let the UI keep polling hooks while backend comes up.
    })
  }, [setSession])

  if (!sessionId) {
    return (
      <div
        style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          height: '100vh',
          fontFamily: 'var(--font-mono)',
          color: 'var(--text-dim)',
        }}
      >
        Connecting to MEMORA...
      </div>
    )
  }

  return <Shell />
}
