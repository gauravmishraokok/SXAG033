import { create } from "zustand";
import type { Message } from "../types";

interface ChatState {
  messages: Message[];
  sessionId: string | null;
  isLoading: boolean;
  inputValue: string;
  addMessage: (msg: Message) => void;
  setSession: (id: string) => void;
  setLoading: (v: boolean) => void;
  setInputValue: (v: string) => void;
  clear: () => void;
}

export const useChatStore = create<ChatState>((set) => ({
  messages: [],
  sessionId: null,
  isLoading: false,
  inputValue: "",
  addMessage: (msg) => set((s) => ({ messages: [...s.messages, msg] })),
  setSession: (id) => set({ sessionId: id }),
  setLoading: (v) => set({ isLoading: v }),
  setInputValue: (v) => set({ inputValue: v }),
  clear: () => set({ messages: [], sessionId: null, isLoading: false, inputValue: "" }),
}));
