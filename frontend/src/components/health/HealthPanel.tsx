import React from 'react'
import { useHealth } from '../../hooks/useHealth'
import { MetricCard } from './MetricCard'
import { TierBar } from './TierBar'

export function HealthPanel() {
  const { data, isLoading, isError } = useHealth()
  const h = data ?? {}

  const total = h.total_memories ?? h.memory_count ?? 0
  const p50 = h.retrieval_p50 ?? h.latency_p50 ?? '—'
  const p99 = h.retrieval_p99 ?? h.latency_p99 ?? '—'
  const pending = h.court_pending ?? h.pending_contradictions ?? 0
  const avgScore = h.avg_contradiction_score ?? h.avg_score ?? '—'
  const hot = h.hot_count ?? h.tier_hot ?? 0
  const warm = h.warm_count ?? h.tier_warm ?? 0
  const cold = h.cold_count ?? h.tier_cold ?? 0
  const penalized = h.penalized_memories ?? h.failure_count ?? 0
  const newPenalized = h.new_failures_today ?? 0
  const contextUsed = h.context_tokens_used ?? h.context_used ?? 0
  const contextMax = h.context_max_tokens ?? h.context_max ?? 8000

  const contextPct = contextMax > 0 ? (contextUsed / contextMax) * 100 : 0
  const contextColor = contextPct >= 90 ? 'var(--accent-red)' : contextPct >= 70 ? 'var(--accent-amber)' : 'var(--accent-green)'

  if (isError) {
    return (
      <div style={{ padding: 16, fontFamily: 'var(--font-mono)', fontSize: 11, color: 'var(--accent-red)' }}>
        ⚠ Cannot reach /health endpoint
      </div>
    )
  }

  return (
    <div style={{
      height: '100%',
      overflow: 'auto',
      padding: '10px 14px',
      display: 'grid',
      gridTemplateColumns: 'repeat(3, 1fr)',
      gridTemplateRows: 'repeat(2, auto)',
      gap: 10,
      alignContent: 'start',
    }}>
      <MetricCard
        label="Total Memories"
        value={isLoading ? '—' : total}
        sub={h.new_today != null ? `+${h.new_today} today` : undefined}
      />

      <MetricCard
        label="Retrieval Latency"
        value={isLoading ? '—' : `${p50}ms`}
        sub={`p50: ${p50}ms / p99: ${p99}ms`}
      />

      <MetricCard
        label="Court Status"
        value={isLoading ? '—' : `${pending} pending`}
        sub={`avg score: ${typeof avgScore === 'number' ? avgScore.toFixed(2) : avgScore}`}
      />

      <MetricCard label="Tier Distribution" value="">
        <TierBar hot={hot} warm={warm} cold={cold} />
      </MetricCard>

      <MetricCard
        label="Failure Patterns"
        value={isLoading ? '—' : penalized}
        sub={`memories penalized · ${newPenalized} new today`}
      />

      <MetricCard label="Context Budget" value={isLoading ? '—' : `${contextUsed} / ${contextMax}`} sub="tokens">
        <div style={{ marginTop: 4, height: 8, background: 'var(--bg-surface-3)', borderRadius: 4, overflow: 'hidden' }}>
          <div style={{
            height: '100%',
            width: `${Math.min(contextPct, 100)}%`,
            background: contextColor,
            borderRadius: 4,
            transition: 'width 0.4s ease',
          }} />
        </div>
      </MetricCard>
    </div>
  )
}
