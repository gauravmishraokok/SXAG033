import { api } from './client'

export function getGraphNodes() {
  return api.get('/graph/nodes')
}

export function getGraphEdges() {
  return api.get('/graph/edges')
}
