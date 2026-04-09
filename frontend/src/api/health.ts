import { api } from './client'

export function getHealth() {
  return api.get('/health')
}
