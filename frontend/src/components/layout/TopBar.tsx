import { useChatStore } from "../../store/chatStore";
import { useCourtQueue } from "../../hooks/useCourtQueue";

export function TopBar() {
  const { sessionId, messages, clear } = useChatStore();
  const { queue } = useCourtQueue();
  const pending = queue.length;
  const statusColor = pending > 0 ? "var(--color-warn)" : "var(--color-success)";
  const shortSession = sessionId ? `${sessionId.slice(0, 8)}...` : "none";

  return (
    <header style={{ height: 56, borderBottom: "1px solid var(--color-border)", display: "flex", alignItems: "center", gap: 16, padding: "0 16px" }}>
      <strong style={{ fontFamily: "var(--font-display)", fontSize: "1.4rem" }}>MEMORA</strong>
      <span style={{ fontFamily: "var(--font-mono)" }}>Session: {shortSession}</span>
      <span style={{ width: 10, height: 10, borderRadius: "50%", background: statusColor, display: "inline-block" }} />
      <span>{messages.length} Memories</span>
      {pending > 0 ? <span style={{ color: "var(--color-warn)" }}>⚠ {pending} Pending</span> : null}
      <button onClick={clear} style={{ marginLeft: "auto" }}>New Session</button>
    </header>
  );
}
