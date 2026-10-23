import { useState } from 'react'
import { FiDownload, FiLoader } from 'react-icons/fi'
import { Button } from '../ui/Button'
import { api, unwrap } from '../../services/api'
import { requestExport, type ExportFormat } from '../../services/exportService'
import type { ApiEnvelope } from '../../types/api'

export default function ExportActions({ projectId }: { projectId: string }) {
  const [busy, setBusy] = useState<ExportFormat | null>(null)
  const [message, setMessage] = useState('')
  const [error, setError] = useState('')
  async function exportModel(format: ExportFormat) {
    setBusy(format); setError(''); setMessage('')
    try {
      const result = await requestExport(format, projectId)
      let url = result.download_url
      if (!url && result.job_id) {
        for (let attempt = 0; attempt < 15; attempt++) {
          await new Promise((resolve) => window.setTimeout(resolve, 2000))
          const status = unwrap((await api.get<ApiEnvelope<{ status?: string; download_url?: string }>>(`/export/${encodeURIComponent(result.job_id)}/status`)).data)
          if (status.download_url) { url = status.download_url; break }
          if (status.status === 'failed' || status.status === 'error') throw new Error('The export job failed.')
        }
      }
      if (!url) { setMessage('Export requested. Check the export job status in a moment.'); return }
      const link = document.createElement('a'); link.href = url; link.download = `${projectId}.${format}`; link.target = '_blank'; link.rel = 'noreferrer'; link.click()
      setMessage(`${format.toUpperCase()} export is ready.`)
    } catch (cause) { setError(cause instanceof Error ? cause.message : 'Export could not be created.') }
    finally { setBusy(null) }
  }
  return <section className="rounded-xl border border-border bg-card p-5"><h2 className="font-semibold">Export model</h2><p className="mt-1 text-sm text-muted-foreground">Download the generated asset.</p><div className="mt-4 flex flex-wrap gap-2"><Button variant="outline" disabled={Boolean(busy)} onClick={() => exportModel('glb')}>{busy === 'glb' ? <FiLoader className="animate-spin" /> : <FiDownload />} Export GLB</Button><Button variant="ghost" disabled={Boolean(busy)} onClick={() => exportModel('obj')}>OBJ</Button></div>{message && <p role="status" className="mt-3 text-sm text-emerald-700">{message}</p>}{error && <p role="alert" className="mt-3 text-sm text-red-600">{error}</p>}</section>
}
