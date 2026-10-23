import { useState } from 'react'
import { FiLoader, FiSend } from 'react-icons/fi'
import { Button } from '../ui/Button'
import { projectService } from '../../services/projectService'

export default function PromptEditPanel({ projectId, onUpdated }: { projectId: string; onUpdated: () => void }) {
  const [prompt, setPrompt] = useState('')
  const [busy, setBusy] = useState(false)
  const [message, setMessage] = useState('')
  const [error, setError] = useState('')
  async function submit(event: React.FormEvent) {
    event.preventDefault()
    if (!prompt.trim()) return
    setBusy(true); setError(''); setMessage('')
    try {
      const result = await projectService.promptEdit(projectId, prompt.trim())
      setMessage(String(result.message || 'Edit request completed. Refresh the project to view its updated mesh.'))
      onUpdated()
      setPrompt('')
    } catch (cause) { setError(cause instanceof Error ? cause.message : 'Could not edit this project.') }
    finally { setBusy(false) }
  }
  return <section className="rounded-xl border border-border bg-card p-5"><h2 className="font-semibold">Prompt editing</h2><p className="mt-1 text-sm text-muted-foreground">Describe a material or geometry adjustment for this mesh.</p>
    <div className="mt-3 flex flex-wrap gap-2">{['Make metallic', 'Increase smoothness', 'Wood texture'].map((suggestion) => <button key={suggestion} type="button" onClick={() => setPrompt(suggestion)} className="rounded-full border border-border px-3 py-1 text-xs hover:bg-muted">{suggestion}</button>)}</div>
    <form className="mt-4 flex gap-2" onSubmit={submit}><input value={prompt} onChange={(event) => setPrompt(event.target.value)} className="min-w-0 flex-1 rounded-md border border-border bg-background px-3 py-2 text-sm" placeholder="Describe the edit…" maxLength={500} /><Button type="submit" disabled={busy || !prompt.trim()}>{busy ? <FiLoader className="animate-spin" /> : <FiSend />} Apply</Button></form>
    {error && <p role="alert" className="mt-3 text-sm text-red-600">{error}</p>}{message && <p role="status" className="mt-3 text-sm text-emerald-700">{message}</p>}
  </section>
}
