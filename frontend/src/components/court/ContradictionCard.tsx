import { useState } from "react";
import type { QuarantineItemResponse } from "../../types";
import { ResolveModal } from "./ResolveModal";
import { ScoreGauge } from "./ScoreGauge";

interface ContradictionCardProps {
  item: QuarantineItemResponse;
  onResolve: (quarantineId: string, resolution: string, mergedContent?: string) => void;
}

export function ContradictionCard({ item, onResolve }: ContradictionCardProps) {
  const [isMergeOpen, setIsMergeOpen] = useState(false);
  return (
    <article style={{ border: "1px solid var(--color-border)", padding: 12 }}>
      <div style={{ display: "flex", justifyContent: "space-between" }}>
        <ScoreGauge score={item.contradiction_score} threshold={0.75} />
        <span>[Quarantine #{item.quarantine_id}]</span>
      </div>
      <p>{item.incoming_content}</p>
      <p>{item.reasoning}</p>
      <div style={{ display: "flex", gap: 8 }}>
        <button onClick={() => onResolve(item.quarantine_id, "accept")}>✓ Accept</button>
        <button onClick={() => onResolve(item.quarantine_id, "reject")}>✗ Reject</button>
        <button onClick={() => setIsMergeOpen(true)}>⟳ Merge...</button>
      </div>
      {isMergeOpen ? (
        <ResolveModal
          initialContent={item.suggested_resolution ?? ""}
          onCancel={() => setIsMergeOpen(false)}
          onConfirm={(content) => {
            onResolve(item.quarantine_id, "merge", content);
            setIsMergeOpen(false);
          }}
        />
      ) : null}
    </article>
  );
}
