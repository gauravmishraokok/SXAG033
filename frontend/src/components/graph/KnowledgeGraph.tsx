import React, { useRef, useState, useEffect, useMemo } from 'react'
import { useGraphData } from '../../hooks/useGraphData'
import { useUIStore } from '../../store'
import { GraphCanvas } from './GraphCanvas'
import { GraphLegend } from './GraphLegend'

export function KnowledgeGraph() {
  const { data, isLoading, isError } = useGraphData()
  const { selectedNodeId, selectNode } = useUIStore()
  const containerRef = useRef<HTMLDivElement>(null)
  const [dims, setDims] = useState({ width: 0, height: 0 })

  useEffect(() => {
    function measure() {
      if (containerRef.current) {
        setDims({
          width: containerRef.current.clientWidth,
          height: containerRef.current.clientHeight,
        })
      }
    }
    measure()
    const ro = new ResizeObserver(measure)
    if (containerRef.current) ro.observe(containerRef.current)
    return () => ro.disconnect()
  }, [])

  const nodes: any[] = Array.isArray(data?.nodes) ? data.nodes : []
  const edgesRaw: any[] = Array.isArray(data?.edges) ? data.edges : []

  const edges = useMemo(() => {
    if (edgesRaw.length > 0) return edgesRaw
    if (nodes.length < 2) return []
    return nodes.slice(0, -1).map((n, i) => ({
      id: `syn-${String(n.id)}-${String(nodes[i + 1].id)}`,
      source: n.id,
      target: nodes[i + 1].id,
      label: '',
    }))
  }, [edgesRaw, nodes])

  if (isError) {
    return (
      <div style={{ padding: 16, fontFamily: 'var(--font-mono)', fontSize: 11, color: 'var(--accent-red)' }}>
        ⚠ Cannot reach graph endpoints
      </div>
    )
  }

  return (
    <div ref={containerRef} style={{ position: 'relative', flex: 1, width: '100%', height: '100%', overflow: 'hidden' }}>
      {isLoading && nodes.length === 0 ? (
        <div style={{ padding: 16, fontFamily: 'var(--font-mono)', fontSize: 11, color: 'var(--text-ghost)', animation: 'pulse-glow 1.5s infinite' }}>
          Loading graph...
        </div>
      ) : nodes.length === 0 ? (
        <div style={{ padding: 16, fontFamily: 'var(--font-mono)', fontSize: 11, color: 'var(--text-ghost)' }}>
          No graph data — start a conversation to build the knowledge graph
        </div>
      ) : (
        <>
          <GraphCanvas
            nodes={nodes}
            edges={edges}
            width={dims.width}
            height={dims.height}
            selectedNodeId={selectedNodeId}
            onNodeClick={selectNode}
          />
          <GraphLegend />
        </>
      )}
    </div>
  )
}
