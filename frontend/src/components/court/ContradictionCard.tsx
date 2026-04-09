import React, { useState } from 'react'
import { useQueryClient } from '@tanstack/react-query'
import { resolveCourtItem } from '../../api/court'
import { ScoreBar } from './ScoreBar'
import { MergeModal } from './MergeModal'

interface QuarantineItem {
  id?: string
  quarantine_id?: string
  incoming_content?: string
  conflicting_content?: string
  incoming_memory?: { content?: string; cube_id?: string }
  conflicting_memory?: { content?: string; cube_id?: string }
  incoming?: { content?: string }
  conflicting?: { content?: string }
  contradiction_score?: number
  score?: number
  judge_reasoning?: string
  reasoning?: string
  suggested_resolution?: string
  suggested?: string
  created_at?: string
  timestamp?: string
}

interface Props {
  item: QuarantineItem
  onResolved: () => void
}

export function ContradictionCard({ item, onResolved }: Props) {
  const queryClient = useQueryClient()
  const [resolving, setResolving] = useState(false)
  const [showMerge, setShowMerge] = useState(false)
  const [fading, setFading] = useState(false)

  const id = item.id ?? item.quarantine_id ?? ''
  const incomingContent =
    item.incoming_content ??
    item.incoming_memory?.content ??
    item.incoming?.content ??
    '—'
  const conflictContent =
    item.conflicting_content ??
    item.conflicting_memory?.content ??
    item.conflicting?.content ??
    '—'
  const score = item.contradiction_score ?? item.score ?? 0
  const reasoning = item.judge_reasoning ?? item.reasoning ?? '—'
  const suggested = item.suggested_resolution ?? item.suggested ?? 'reject'
  const timestamp = item.created_at ?? item.timestamp ?? ''

  async function resolve(resolution: string, mergedContent?: string) {
    if (resolving) return
    setResolving(true)
    try {
      await resolveCourtItem(id, resolution, mergedContent)
      queryClient.invalidateQueries({ queryKey: ['court-queue'] })
    } catch {
      // ignore — optimistic UI
    }
    setFading(true)
    setTimeout(onResolved, 300)
  }

  return (
    <>
      {showMerge && (
        <MergeModal
          suggestedContent={`${incomingContent} [MERGED] ${conflictContent}`}
          onConfirm={(merged) => { setShowMerge(false); resolve('merge', merged) }}
          onCancel={() => setShowMerge(false)}
        />
      )}
      <div style={{
        margin: '8px 10px',
        border: '1px solid var(--border-base)',
        borderRadius: 6,
        background: 'var(--bg-surface-2)',
        overflow: 'hidden',
        opacity: fading ? 0 : 1,
        transition: 'opacity 0.3s ease',
      }}>
        {/* Header */}
        <div style={{
          padding: '10px 14px',
          borderBottom: '1px solid var(--border-dim)',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
        }}>
          <span style={{
            fontFamily: 'var(--font-display)',
            fontSize: 11,
            fontWeight: 700,
            letterSpacing: '0.1em',
            color: 'var(--accent-amber)',
          }}>CONTRADICTION DETECTED</span>
          <div style={{ display: 'flex', gap: 10, fontFamily: 'var(--font-mono)', fontSize: 10, color: 'var(--text-dim)' }}>
            <span>#{id.slice(0, 7)}</span>
            <span>{timestamp ? new Date(timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) : ''}</span>
          </div>
        </div>

        <div style={{ padding: '12px 14px', display: 'flex', flexDirection: 'column', gap: 10 }}>
          {/* Incoming */}
          <div>
            <div style={{ fontFamily: 'var(--font-display)', fontSize: 9, fontWeight: 700, letterSpacing: '0.12em', color: 'var(--accent-cyan)', marginBottom: 6 }}>
              INCOMING MEMORY
            </div>
            <div style={{
              border: '1px solid rgba(0,210,255,0.4)',
              background: 'rgba(0,210,255,0.04)',
              borderRadius: 4,
              padding: '8px 10px',
              fontFamily: 'var(--font-mono)',
              fontSize: 12,
              color: 'var(--text-secondary)',
              lineHeight: 1.5,
            }}>
              "{incomingContent}"
            </div>
          </div>

          {/* Conflicting */}
          <div>
            <div style={{ fontFamily: 'var(--font-display)', fontSize: 9, fontWeight: 700, letterSpacing: '0.12em', color: 'var(--accent-red)', marginBottom: 6 }}>
              CONFLICTS WITH
            </div>
            <div style={{
              border: '1px solid rgba(255,71,87,0.4)',
              background: 'rgba(255,71,87,0.04)',
              borderRadius: 4,
              padding: '8px 10px',
              fontFamily: 'var(--font-mono)',
              fontSize: 12,
              color: 'var(--text-secondary)',
              lineHeight: 1.5,
            }}>
              "{conflictContent}"
            </div>
          </div>

          {/* Score */}
          <div style={{ paddingTop: 4, paddingBottom: 8 }}>
            <ScoreBar score={score} />
          </div>

          {/* Reasoning */}
          <div>
            <div style={{ fontFamily: 'var(--font-display)', fontSize: 9, fontWeight: 700, letterSpacing: '0.12em', color: 'var(--text-dim)', marginBottom: 6 }}>
              JUDGE REASONING
            </div>
            <div style={{
              fontFamily: 'var(--font-body)',
              fontSize: 12,
              color: 'var(--text-secondary)',
              lineHeight: 1.5,
              fontStyle: 'italic',
            }}>
              "{reasoning}"
            </div>
          </div>

          {/* Suggestion */}
          <div style={{ fontFamily: 'var(--font-mono)', fontSize: 11, color: 'var(--text-dim)' }}>
            SUGGESTED: <span style={{ color: 'var(--text-primary)' }}>{suggested}</span>
          </div>

          {/* Action buttons */}
          <div style={{ display: 'flex', gap: 8, paddingTop: 4 }}>
            <button
              onClick={() => resolve('accept')}
              disabled={resolving}
              style={{
                fontFamily: 'var(--font-display)',
                fontSize: 12,
                fontWeight: 600,
                padding: '7px 16px',
                borderRadius: 6,
                border: '1px solid var(--accent-green)',
                background: 'transparent',
                color: 'var(--accent-green)',
                cursor: 'pointer',
                transition: 'background 0.15s',
              }}
              onMouseEnter={(e) => (e.currentTarget.style.background = 'rgba(0,229,160,0.15)')}
              onMouseLeave={(e) => (e.currentTarget.style.background = 'transparent')}
            >✓ Accept</button>

            <button
              onClick={() => resolve('reject')}
              disabled={resolving}
              style={{
                fontFamily: 'var(--font-display)',
                fontSize: 12,
                fontWeight: 600,
                padding: '7px 16px',
                borderRadius: 6,
                border: '1px solid var(--accent-red)',
                background: 'transparent',
                color: 'var(--accent-red)',
                cursor: 'pointer',
                transition: 'background 0.15s',
              }}
              onMouseEnter={(e) => (e.currentTarget.style.background = 'rgba(255,71,87,0.15)')}
              onMouseLeave={(e) => (e.currentTarget.style.background = 'transparent')}
            >✗ Reject</button>

            <button
              onClick={() => setShowMerge(true)}
              disabled={resolving}
              style={{
                fontFamily: 'var(--font-display)',
                fontSize: 12,
                fontWeight: 600,
                padding: '7px 16px',
                borderRadius: 6,
                border: '1px solid var(--accent-amber)',
                background: 'transparent',
                color: 'var(--accent-amber)',
                cursor: 'pointer',
                transition: 'background 0.15s',
              }}
              onMouseEnter={(e) => (e.currentTarget.style.background = 'rgba(245,166,35,0.15)')}
              onMouseLeave={(e) => (e.currentTarget.style.background = 'transparent')}
            >⟳ Merge...</button>
          </div>
        </div>
      </div>
    </>
  )
}
