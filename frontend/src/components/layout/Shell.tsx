import { ChatPanel } from "../chat/ChatPanel";
import { CourtDashboard } from "../court/CourtDashboard";
import { KnowledgeGraph } from "../graph/KnowledgeGraph";
import { MemoryTimeline } from "../timeline/MemoryTimeline";
import { HealthPanel } from "../health/HealthPanel";
import { TopBar } from "./TopBar";
import { useUIStore } from "../../store/uiStore";
import { useGraphData } from "../../hooks/useGraphData";

export function Shell() {
  const { isBottomPanelOpen, toggleBottomPanel, selectNode } = useUIStore();
  const { nodes, edges } = useGraphData();

  return (
    <div style={{ height: "100vh", display: "grid", gridTemplateRows: "56px 1fr auto" }}>
      <TopBar />
      <main style={{ display: "grid", gridTemplateColumns: "30% 40% 30%", gap: 8, padding: 8, minHeight: 0 }}>
        <section style={{ overflow: "auto", border: "1px solid var(--color-border)" }}>
          <KnowledgeGraph nodes={nodes} edges={edges} onNodeClick={selectNode} />
        </section>
        <section style={{ minHeight: 0 }}>
          <ChatPanel />
        </section>
        <section style={{ overflow: "auto" }}>
          <CourtDashboard />
        </section>
      </main>
      <section style={{ height: isBottomPanelOpen ? 200 : 40, overflow: "hidden", borderTop: "1px solid var(--color-border)", padding: 8 }}>
        <button onClick={toggleBottomPanel}>{isBottomPanelOpen ? "Collapse" : "Expand"}</button>
        {isBottomPanelOpen ? (
          <div style={{ display: "grid", gridTemplateColumns: "60% 40%", gap: 8 }}>
            <MemoryTimeline />
            <HealthPanel />
          </div>
        ) : null}
      </section>
    </div>
  );
}
