import { create } from "zustand";

interface UIState {
  activePanel: "graph" | "timeline" | "health";
  isBottomPanelOpen: boolean;
  selectedNodeId: string | null;
  setActivePanel: (panel: UIState["activePanel"]) => void;
  toggleBottomPanel: () => void;
  selectNode: (id: string | null) => void;
}

export const useUIStore = create<UIState>((set) => ({
  activePanel: "graph",
  isBottomPanelOpen: true,
  selectedNodeId: null,
  setActivePanel: (panel) => set({ activePanel: panel }),
  toggleBottomPanel: () => set((s) => ({ isBottomPanelOpen: !s.isBottomPanelOpen })),
  selectNode: (id) => set({ selectedNodeId: id }),
}));
