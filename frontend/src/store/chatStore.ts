import { create } from 'zustand'

export interface ChatMessage {
  id: string
  role: 'user' | 'assistant'
  text: string
  memoriesUsed?: string[]
  timestamp: Date
}

interface ChatState {
  messages: ChatMessage[]
  sessionId: string | null
  isStreaming: boolean
  agentThoughts: string
  lastUsedMemoryIds: string[]
  addMessage: (msg: Omit<ChatMessage, 'id' | 'timestamp'>) => void
  setSession: (id: string) => void
  setStreaming: (v: boolean) => void
  setThoughts: (t: string) => void
  setLastUsedMemoryIds: (ids: string[]) => void
  clear: () => void
}

export const useChatStore = create<ChatState>((set) => ({
  messages: [],
  sessionId: null,
  isStreaming: false,
  agentThoughts: '',
  lastUsedMemoryIds: [],

  addMessage: (msg) =>
    set((s) => ({
      messages: [
        ...s.messages,
        { ...msg, id: crypto.randomUUID(), timestamp: new Date() },
      ],
    })),

  setSession: (id) => set({ sessionId: id }),
  setStreaming: (v) => set({ isStreaming: v }),
  setThoughts: (t) => set({ agentThoughts: t }),
  setLastUsedMemoryIds: (ids) => set({ lastUsedMemoryIds: ids }),

  clear: () =>
    set({ messages: [], isStreaming: false, agentThoughts: '', lastUsedMemoryIds: [] }),
}))
