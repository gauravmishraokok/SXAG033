import React, { useEffect, useRef, useState } from 'react'
import * as d3 from 'd3'
import { NodeTooltip } from './NodeTooltip'

interface GraphNode {
  id: string
  type?: string
  memory_type?: string
  tier?: string
  label?: string
  content?: string
  tags?: string[]
  access_count?: number
  x?: number
  y?: number
  fx?: number | null
  fy?: number | null
}

interface GraphEdge {
  source: string | GraphNode
  target: string | GraphNode
  status?: string
}

interface Props {
  nodes: GraphNode[]
  edges: GraphEdge[]
  width: number
  height: number
  selectedNodeId: string | null
  onNodeClick: (id: string | null) => void
}

function nodeRadius(node: GraphNode) {
  const tier = (node.tier ?? 'cold').toLowerCase()
  if (tier === 'hot') return 14
  if (tier === 'warm') return 10
  return 7
}

function nodeColor(node: GraphNode) {
  const type = (node.type ?? node.memory_type ?? 'episodic').toLowerCase()
  if (type === 'episodic') return 'var(--accent-purple)'
  if (type === 'semantic') return 'var(--accent-teal)'
  return 'var(--accent-orange)'
}

const TYPE_COLORS: Record<string, string> = {
  episodic: '#a855f7',
  semantic: '#14b8a6',
  kg_node: '#fb923c',
}

function getColor(node: GraphNode) {
  const type = (node.type ?? node.memory_type ?? 'episodic').toLowerCase()
  return TYPE_COLORS[type] ?? '#a855f7'
}

export function GraphCanvas({ nodes, edges, width, height, selectedNodeId, onNodeClick }: Props) {
  const svgRef = useRef<SVGSVGElement>(null)
  const simRef = useRef<d3.Simulation<GraphNode, GraphEdge> | null>(null)
  const [tooltip, setTooltip] = useState<{ node: GraphNode; x: number; y: number } | null>(null)

  useEffect(() => {
    if (!svgRef.current || width === 0 || height === 0) return

    const svg = d3.select(svgRef.current)
    svg.selectAll('*').remove()

    const g = svg.append('g')

    // Zoom + pan
    const zoom = d3.zoom<SVGSVGElement, unknown>()
      .scaleExtent([0.25, 6])
      .on('zoom', (event) => g.attr('transform', event.transform))
    svg.call(zoom as any)

    // Defs: arrowhead
    const defs = svg.append('defs')
    defs.append('marker')
      .attr('id', 'arrow')
      .attr('viewBox', '0 -5 10 10')
      .attr('refX', 20)
      .attr('markerWidth', 6)
      .attr('markerHeight', 6)
      .attr('orient', 'auto')
      .append('path')
      .attr('d', 'M0,-5L10,0L0,5')
      .attr('fill', '#3a3d4d')

    const nodeData = nodes.map((n) => ({ ...n }))
    const nodeById = new Map(nodeData.map((n) => [n.id, n]))
    const edgeData = edges.map((e) => ({
      ...e,
      source: typeof e.source === 'string' ? (nodeById.get(e.source) ?? e.source) : e.source,
      target: typeof e.target === 'string' ? (nodeById.get(e.target) ?? e.target) : e.target,
    }))

    // Edges
    const link = g.append('g').attr('class', 'links').selectAll('line')
      .data(edgeData)
      .enter().append('line')
      .attr('stroke', (d: any) => d.status === 'deprecated' ? 'rgba(255,71,87,0.4)' : 'rgba(58,61,77,0.9)')
      .attr('stroke-width', 1)
      .attr('stroke-dasharray', (d: any) => d.status === 'deprecated' ? '4 3' : null)

    // Nodes
    const nodeG = g.append('g').attr('class', 'nodes').selectAll('g')
      .data(nodeData)
      .enter().append('g')
      .style('cursor', 'pointer')
      .call(d3.drag<SVGGElement, GraphNode>()
        .on('start', (event, d) => {
          if (!event.active) sim.alphaTarget(0.3).restart()
          d.fx = d.x; d.fy = d.y
        })
        .on('drag', (event, d) => { d.fx = event.x; d.fy = event.y })
        .on('end', (event, d) => {
          if (!event.active) sim.alphaTarget(0)
          d.fx = null; d.fy = null
        }) as any)
      .on('click', (_event, d) => onNodeClick(d.id === selectedNodeId ? null : d.id))
      .on('mouseenter', (event, d) => {
        const rect = svgRef.current!.getBoundingClientRect()
        setTooltip({ node: d, x: event.clientX - rect.left, y: event.clientY - rect.top })
      })
      .on('mouseleave', () => setTooltip(null))

    nodeG.append('circle')
      .attr('r', nodeRadius)
      .attr('fill', (d) => getColor(d))
      .attr('opacity', (d) => {
        if (!selectedNodeId) return 0.9
        return d.id === selectedNodeId ? 1 : 0.2
      })
      .attr('filter', (d) => (d.tier ?? '').toLowerCase() === 'hot' ? 'url(#hotglow)' : null)

    // Hot glow filter
    const filter = defs.append('filter').attr('id', 'hotglow')
    filter.append('feGaussianBlur').attr('stdDeviation', 3).attr('result', 'coloredBlur')
    const merge = filter.append('feMerge')
    merge.append('feMergeNode').attr('in', 'coloredBlur')
    merge.append('feMergeNode').attr('in', 'SourceGraphic')

    // Labels
    nodeG.append('text')
      .attr('dy', (d) => nodeRadius(d) + 12)
      .attr('text-anchor', 'middle')
      .attr('fill', '#9098b4')
      .attr('font-size', 9)
      .attr('font-family', 'DM Sans, sans-serif')
      .text((d) => {
        const label = d.label ?? d.content ?? d.id
        return label.slice(0, 20)
      })

    // Simulation
    const sim = d3.forceSimulation<GraphNode>(nodeData)
      .force('link', d3.forceLink<GraphNode, GraphEdge>(edgeData as any).id((d) => d.id).distance(90).strength(0.8))
      .force('charge', d3.forceManyBody().strength(-200))
      .force('center', d3.forceCenter(width / 2, height / 2))
      .force('collision', d3.forceCollide<GraphNode>().radius((d) => nodeRadius(d) + 6))
      .alphaDecay(0.03)
      .on('tick', () => {
        link
          .attr('x1', (d: any) => d.source.x ?? 0)
          .attr('y1', (d: any) => d.source.y ?? 0)
          .attr('x2', (d: any) => d.target.x ?? 0)
          .attr('y2', (d: any) => d.target.y ?? 0)
        nodeG.attr('transform', (d: any) => `translate(${d.x ?? 0},${d.y ?? 0})`)
      })

    simRef.current = sim as any

    return () => { sim.stop() }
  }, [nodes, edges, width, height, selectedNodeId])

  return (
    <div style={{ position: 'relative', width, height }}>
      <svg
        ref={svgRef}
        width={width}
        height={height}
        style={{ background: 'var(--bg-void)', display: 'block' }}
      />
      {tooltip && (
        <NodeTooltip node={tooltip.node} x={tooltip.x} y={tooltip.y} />
      )}
    </div>
  )
}
