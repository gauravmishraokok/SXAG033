import { api } from './client'

export function getCourtQueue() {
  return api.get('/court/queue')
}

export function resolveCourtItem(id: string, resolution: string, mergedContent?: string) {
  return api.post(`/court/resolve/${id}`, {
    resolution,
    ...(mergedContent ? { merged_content: mergedContent } : {}),
  })
}
