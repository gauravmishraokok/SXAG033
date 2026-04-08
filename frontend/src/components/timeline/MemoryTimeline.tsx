import { useTimeline } from "../../hooks/useTimeline";
import { useChatStore } from "../../store/chatStore";
import { useUIStore } from "../../store/uiStore";

const COLORS: Record<string, string> = {
  created: "var(--color-success)",
  updated: "var(--color-accent)",
  quarantined: "var(--color-warn)",
  resolved: "var(--color-success)",
  evicted: "var(--color-text-dim)",
};

export function MemoryTimeline() {
  const { sessionId } = useChatStore();
  const { selectNode } = useUIStore();
  const { data } = useTimeline(sessionId);
  const events = data?.events ?? [];

  return (
    <section style={{ overflowX: "auto", whiteSpace: "nowrap", padding: 8, border: "1px solid var(--color-border)" }}>
      {events.map((event: any) => (
        <button key={event.id} onClick={() => selectNode(event.cube_id)} style={{ marginRight: 12, border: "none", background: "none", color: COLORS[event.event_type] ?? "var(--color-text-secondary)" }}>
          ● {event.event_type}
        </button>
      ))}
    </section>
  );
}
