import { useQuery } from '@tanstack/react-query'
import { getGraphNodes, getGraphEdges } from '../api/graph'

export function useGraphData() {
  return useQuery({
    queryKey: ['graph'],
    queryFn: () => Promise.all([getGraphNodes(), getGraphEdges()]).then(([nodes, edges]) => ({ nodes, edges })),
    refetchInterval: 5000,
    refetchOnWindowFocus: true,
    placeholderData: (prev) => prev,
  })
}
