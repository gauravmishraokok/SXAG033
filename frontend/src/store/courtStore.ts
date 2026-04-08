import { create } from "zustand";

interface CourtState {
  activeResolutionId: string | null;
  setActiveResolution: (id: string | null) => void;
}

export const useCourtStore = create<CourtState>((set) => ({
  activeResolutionId: null,
  setActiveResolution: (id) => set({ activeResolutionId: id }),
}));
