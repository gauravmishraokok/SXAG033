import React from 'react'

interface Props {
  node: any
  x: number
  y: number
}

export function NodeTooltip({ node, x, y }: Props) {
  const type = node.type ?? node.memory_type ?? 'episodic'
  const tier = node.tier ?? 'cold'
  const extra = node.extra ?? {}
  const title = (node.label ?? extra.label ?? extra.title ?? node.content ?? node.id ?? '') as string
  const detail = (extra.detail as string | undefined) || (node.content as string) || ''
  const tags: string[] = node.tags ?? []

  return (
    <div style={{
      position: 'absolute',
      left: x + 14,
      top: y - 10,
      background: 'var(--bg-surface-3)',
      border: '1px solid var(--border-base)',
      borderRadius: 6,
      padding: '8px 12px',
      fontFamily: 'var(--font-mono)',
      fontSize: 10,
      color: 'var(--text-secondary)',
      pointerEvents: 'none',
      zIndex: 50,
      maxWidth: 220,
      lineHeight: 1.6,
      boxShadow: '0 4px 20px rgba(0,0,0,0.5)',
    }}>
      <div style={{ fontFamily: 'var(--font-display)', fontSize: 11, fontWeight: 700, color: 'var(--text-primary)', marginBottom: 4 }}>
        {String(title).slice(0, 48)}{String(title).length > 48 ? '…' : ''}
      </div>
      {detail && detail !== title && (
        <div style={{ fontSize: 10, color: 'var(--text-dim)', marginBottom: 6, lineHeight: 1.45 }}>
          {String(detail).slice(0, 120)}{String(detail).length > 120 ? '…' : ''}
        </div>
      )}
      <div>type: <span style={{ color: 'var(--text-primary)' }}>{type}</span></div>
      <div>tier: <span style={{ color: 'var(--text-primary)' }}>{tier}</span></div>
      <div>access: <span style={{ color: 'var(--text-primary)' }}>{node.access_count ?? 0}</span></div>
      {tags.length > 0 && (
        <div>tags: <span style={{ color: 'var(--accent-blue)' }}>{tags.join(', ')}</span></div>
      )}
    </div>
  )
}
