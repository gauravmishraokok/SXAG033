const BASE = import.meta.env.VITE_API_URL ?? 'http://localhost:8000'

export const api = {
  get: (path: string) =>
    fetch(`${BASE}${path}`).then((r) => {
      if (!r.ok) throw r
      return r.json()
    }),
  post: (path: string, body: unknown) =>
    fetch(`${BASE}${path}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    }).then((r) => {
      if (!r.ok) throw r
      return r.json()
    }),
  delete: (path: string) =>
    fetch(`${BASE}${path}`, { method: 'DELETE' }).then((r) => r.json()),
}
