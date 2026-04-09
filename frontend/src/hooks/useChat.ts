import { useState } from 'react'
import { postChat, createSession } from '../api/chat'
import { useChatStore } from '../store'

function sleep(ms: number) {
  return new Promise((r) => setTimeout(r, ms))
}

export function useChat() {
  const { addMessage, sessionId, setStreaming, setThoughts, setLastUsedMemoryIds, isStreaming } =
    useChatStore()
  const [error, setError] = useState<string | null>(null)

  async function sendMessage(text: string, feedback?: string) {
    if (isStreaming) return
    setError(null)
    setStreaming(true)
    addMessage({ role: 'user', text })

    setThoughts('Searching memory vault...')
    const chatPromise = postChat(text, sessionId, feedback).catch((e) => { throw e })

    await sleep(500)
    setThoughts('Building context...')
    await sleep(500)
    setThoughts('Calling Groq / Llama3...')

    try {
      const response = await chatPromise
      const memoriesUsed: string[] = response.memories_used ?? []
      addMessage({ role: 'assistant', text: response.text ?? response.message ?? '', memoriesUsed })
      setLastUsedMemoryIds(memoriesUsed)
      setThoughts('Storing episode to memory vault...')
      await sleep(1500)
      setThoughts('')
    } catch (e) {
      setThoughts('')
      setError('Failed to get response. Is the backend running?')
    } finally {
      setStreaming(false)
    }
  }

  return { sendMessage, error, isStreaming }
}
