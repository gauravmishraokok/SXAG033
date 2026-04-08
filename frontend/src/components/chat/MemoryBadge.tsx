interface MemoryBadgeProps {
  cubeId: string;
  memoryType: "episodic" | "semantic" | "kg_node";
  content?: string;
}

const COLOR_MAP: Record<MemoryBadgeProps["memoryType"], string> = {
  episodic: "var(--color-episodic)",
  semantic: "var(--color-semantic)",
  kg_node: "var(--color-kg-node)",
};

export function MemoryBadge({ cubeId, memoryType, content }: MemoryBadgeProps) {
  return (
    <span title={content ?? cubeId} style={{ border: `1px solid ${COLOR_MAP[memoryType]}`, color: COLOR_MAP[memoryType], borderRadius: 999, padding: "2px 8px", fontSize: 12 }}>
      [{memoryType}] {cubeId}
    </span>
  );
}
