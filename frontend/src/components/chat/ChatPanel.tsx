import { FormEvent, KeyboardEvent, useMemo, useRef } from "react";
import { MemoryBadge } from "./MemoryBadge";
import { useChatStore } from "../../store/chatStore";

export function ChatPanel() {
  const { messages, inputValue, setInputValue, addMessage, isLoading, setLoading, sessionId, setSession } = useChatStore();
  const scrollRef = useRef<HTMLDivElement>(null);

  const agentMessages = useMemo(() => messages.filter((m) => m.role === "agent"), [messages]);

  const send = async () => {
    if (!inputValue.trim()) return;
    const userText = inputValue;
    setInputValue("");
    addMessage({ id: crypto.randomUUID(), role: "user", text: userText });
    setLoading(true);
    const resp = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: userText, session_id: sessionId }),
    });
    const data = await resp.json();
    if (!sessionId) setSession(data.session_id);
    addMessage({ id: crypto.randomUUID(), role: "agent", text: data.text, memoriesUsed: data.memories_used });
    setLoading(false);
    scrollRef.current?.scrollTo({ top: scrollRef.current.scrollHeight, behavior: "smooth" });
  };

  const onSubmit = async (e: FormEvent) => {
    e.preventDefault();
    await send();
  };

  const onKeyDown = async (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      await send();
    }
  };

  return (
    <section style={{ padding: 12, height: "100%", display: "grid", gridTemplateRows: "auto 1fr auto", gap: 8 }}>
      <h3>CHAT</h3>
      <div ref={scrollRef} style={{ overflow: "auto", border: "1px solid var(--color-border)", padding: 8 }}>
        {messages.map((msg) => (
          <div key={msg.id} style={{ textAlign: msg.role === "user" ? "left" : "right", marginBottom: 8 }}>
            <div>{msg.text}</div>
            {msg.role === "agent" && msg.memoriesUsed?.length ? (
              <div style={{ display: "flex", gap: 4, justifyContent: "flex-end", marginTop: 4 }}>
                {msg.memoriesUsed.map((id) => <MemoryBadge key={id} cubeId={id} memoryType="semantic" />)}
              </div>
            ) : null}
          </div>
        ))}
        {isLoading ? <div>...</div> : null}
      </div>
      <form onSubmit={onSubmit}>
        <textarea value={inputValue} onChange={(e) => setInputValue(e.target.value)} onKeyDown={onKeyDown} style={{ width: "100%" }} />
        <div style={{ display: "flex", gap: 8, marginTop: 6 }}>
          <button type="submit">Send ▶</button>
          {agentMessages.length > 0 ? (
            <>
              <button type="button">👍 Good</button>
              <button type="button">👎 Bad</button>
            </>
          ) : null}
        </div>
      </form>
    </section>
  );
}
