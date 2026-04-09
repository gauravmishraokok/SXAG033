import { api } from './client'

export function postChat(message: string, sessionId: string | null, feedback?: string | null) {
  return api.post('/chat', { message, session_id: sessionId, feedback: feedback ?? null })
}

export function createSession() {
  return api.post('/chat/session', {})
}
