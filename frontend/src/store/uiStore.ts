import { create } from 'zustand'

interface UIState {
  bottomTab: 'graph' | 'timeline' | 'health'
  isBottomOpen: boolean
  memoryFilter: Set<string>
  selectedNodeId: string | null
  flashedMemoryIds: string[]
  setBottomTab: (t: UIState['bottomTab']) => void
  toggleBottom: () => void
  toggleFilter: (type: string) => void
  selectNode: (id: string | null) => void
  flashMemories: (ids: string[]) => void
}

export const useUIStore = create<UIState>((set) => ({
  bottomTab: 'graph',
  isBottomOpen: true,
  memoryFilter: new Set<string>(),
  selectedNodeId: null,
  flashedMemoryIds: [],

  setBottomTab: (t) => set({ bottomTab: t }),
  toggleBottom: () => set((s) => ({ isBottomOpen: !s.isBottomOpen })),

  toggleFilter: (type) =>
    set((s) => {
      const next = new Set(s.memoryFilter)
      if (next.has(type)) next.delete(type)
      else next.add(type)
      return { memoryFilter: next }
    }),

  selectNode: (id) => set({ selectedNodeId: id }),

  flashMemories: (ids) => {
    set({ flashedMemoryIds: ids })
    setTimeout(() => set({ flashedMemoryIds: [] }), 2000)
  },
}))
