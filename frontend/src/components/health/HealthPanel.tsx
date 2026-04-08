import { useHealth } from "../../hooks/useHealth";

export function HealthPanel() {
  const { data } = useHealth();
  if (!data) return <section>Loading health...</section>;

  return (
    <section style={{ border: "1px solid var(--color-border)", padding: 12 }}>
      <h3>Health</h3>
      <div>Total Memories: {data.total_memories}</div>
      <div>Retrieval Latency: p50: {data.retrieval_latency_p50_ms}ms / p99: {data.retrieval_latency_p99_ms}ms</div>
      <div style={{ color: data.quarantine_pending > 0 ? "var(--color-warn)" : "inherit" }}>Quarantine Pending: {data.quarantine_pending}</div>
      <div>Memory Age: Newest: 2m ago</div>
      <div>
        HOT {data.memories_by_tier.hot}% | WARM {data.memories_by_tier.warm}% | COLD {data.memories_by_tier.cold}%
      </div>
    </section>
  );
}
