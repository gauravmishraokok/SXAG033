import { useEffect, useRef } from "react";
import { useCourtQueue } from "../../hooks/useCourtQueue";
import { ContradictionCard } from "./ContradictionCard";

export function CourtDashboard() {
  const { queue } = useCourtQueue();
  const lastCount = useRef(0);
  const pulse = useRef(false);

  useEffect(() => {
    pulse.current = lastCount.current === 0 && queue.length > 0;
    lastCount.current = queue.length;
  }, [queue.length]);

  const resolve = async (quarantineId: string, resolution: string, mergedContent = "") => {
    await fetch(`/api/court/resolve/${quarantineId}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ resolution, merged_content: mergedContent }),
    });
  };

  return (
    <section style={{ border: pulse.current ? "1px solid var(--color-accent)" : "1px solid var(--color-border)", padding: 12, overflow: "auto" }}>
      <h3>MEMORY COURT ⚠ {queue.length} Pending</h3>
      {queue.length === 0 ? <p>All memories approved ✓</p> : queue.map((item) => <ContradictionCard key={item.quarantine_id} item={item} onResolve={resolve} />)}
    </section>
  );
}
