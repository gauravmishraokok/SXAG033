import { useState } from "react";

interface ResolveModalProps {
  initialContent: string;
  onCancel: () => void;
  onConfirm: (content: string) => void;
}

export function ResolveModal({ initialContent, onCancel, onConfirm }: ResolveModalProps) {
  const [value, setValue] = useState(initialContent);
  return (
    <div style={{ position: "fixed", inset: 0, background: "#000a", display: "grid", placeItems: "center" }}>
      <div style={{ background: "var(--color-surface)", border: "1px solid var(--color-border)", padding: 16, width: 420 }}>
        <h4>Merge Memories</h4>
        <textarea value={value} onChange={(e) => setValue(e.target.value)} style={{ width: "100%", minHeight: 120 }} />
        <div style={{ display: "flex", gap: 8, justifyContent: "flex-end" }}>
          <button onClick={onCancel}>Cancel</button>
          <button onClick={() => onConfirm(value)}>Confirm Merge</button>
        </div>
      </div>
    </div>
  );
}
