import { create } from 'zustand'

interface CourtState {
  pendingCount: number
  hasAlert: boolean
  activeResolutionId: string | null
  setPendingCount: (n: number) => void
  setAlert: (v: boolean) => void
  setActiveResolution: (id: string | null) => void
}

export const useCourtStore = create<CourtState>((set) => ({
  pendingCount: 0,
  hasAlert: false,
  activeResolutionId: null,
  setPendingCount: (n) => set({ pendingCount: n }),
  setAlert: (v) => set({ hasAlert: v }),
  setActiveResolution: (id) => set({ activeResolutionId: id }),
}))
