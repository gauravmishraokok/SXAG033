import { api } from './client'

export function getTimeline(sessionId: string | null, limit = 100) {
  const params = new URLSearchParams()
  if (sessionId) params.set('session_id', sessionId)
  params.set('limit', String(limit))
  return api.get(`/timeline?${params}`)
}
