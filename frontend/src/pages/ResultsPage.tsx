import { lazy, Suspense, useCallback, useEffect, useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import { FiArrowLeft, FiBox, FiExternalLink, FiImage } from 'react-icons/fi'
import { Button } from '../components/ui/Button'
import PromptEditPanel from '../components/results/PromptEditPanel'
import ExportActions from '../components/results/ExportActions'
import { projectService } from '../services/projectService'
import type { ProjectReport } from '../types/api'

const ModelViewer = lazy(() => import('../viewer/ModelViewer'))

function findString(source: unknown, keys: string[]): string | undefined {
  if (!source || typeof source !== 'object') return undefined
  for (const key of keys) { const value = (source as Record<string, unknown>)[key]; if (typeof value === 'string' && value) return value }
}
function ReportCard({ title, data }: { title: string; data?: Record<string, unknown> }) {
  if (!data) return <section className="rounded-xl border border-border bg-card p-5"><h2 className="font-semibold">{title}</h2><p className="mt-2 text-sm text-muted-foreground">Not included in this project report.</p></section>
  const entries = Object.entries(data).filter(([, value]) => ['string', 'number', 'boolean'].includes(typeof value)).slice(0, 8)
  return <section className="rounded-xl border border-border bg-card p-5"><h2 className="font-semibold">{title}</h2><dl className="mt-4 space-y-3">{entries.length ? entries.map(([key, value]) => <div key={key} className="flex justify-between gap-4 text-sm"><dt className="capitalize text-muted-foreground">{key.replaceAll('_', ' ')}</dt><dd className="text-right font-medium">{String(value)}</dd></div>) : <p className="text-sm text-muted-foreground">No summary metrics provided.</p>}</dl></section>
}

export default function ResultsPage() {
  const { id = '' } = useParams()
  const [report, setReport] = useState<ProjectReport>()
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(true)
  const [loadedId, setLoadedId] = useState('')
  const [refresh, setRefresh] = useState(0)
  const refreshReport = useCallback(() => { setLoading(true); setError(''); setRefresh((value) => value + 1) }, [])
  useEffect(() => { let active = true; projectService.getReport(id).then((result) => { if (active) { setReport(result.full_report || result); setLoadedId(id) } }).catch((cause: unknown) => { if (active) { setError(cause instanceof Error ? cause.message : 'Could not load this report.'); setLoadedId(id) } }).finally(() => { if (active) setLoading(false) }); return () => { active = false } }, [id, refresh])
  const isLoading = loading || loadedId !== id
  const meshUrl = findString(report, ['optimized_mesh_url', 'mesh_url', 'glb_url'])
  const imageUrl = findString(report, ['original_image_url', 'image_url', 'source_image_url'])
  const ai = report?.ai_evaluation_report as Record<string, unknown> | undefined
  const mesh = report?.mesh_quality_report as Record<string, unknown> | undefined
  return <div className="space-y-6"><Link to="/history" className="inline-flex items-center gap-2 text-sm text-muted-foreground hover:text-foreground"><FiArrowLeft /> Project history</Link><div className="flex flex-wrap items-end justify-between gap-3"><div><p className="text-sm font-medium text-indigo-600">Project {id}</p><h1 className="mt-1 text-3xl font-semibold">Reconstruction results</h1></div><Link to={`/ar/${encodeURIComponent(id)}`}><Button variant="outline">Open AR preview</Button></Link></div>
    {isLoading && <p className="rounded-lg border border-border bg-card p-5 text-sm text-muted-foreground">Loading full report…</p>}
    {error && <p role="alert" className="rounded-lg bg-red-50 p-4 text-sm text-red-700">{error}</p>}
    {report && loadedId === id && <><div className="grid gap-5 xl:grid-cols-[minmax(0,1.6fr)_minmax(280px,0.8fr)]"><Suspense fallback={<div className="grid h-[420px] place-items-center rounded-xl border border-border bg-card text-sm text-muted-foreground">Loading 3D viewer…</div>}><ModelViewer url={meshUrl} /></Suspense><div className="space-y-4">{imageUrl ? <section className="overflow-hidden rounded-xl border border-border bg-card"><div className="flex items-center gap-2 border-b border-border p-4 text-sm font-medium"><FiImage /> Source image</div><img src={imageUrl} alt="Uploaded source" className="max-h-64 w-full object-contain p-3" /></section> : <section className="rounded-xl border border-border bg-card p-5"><h2 className="flex items-center gap-2 font-semibold"><FiImage /> Source image</h2><p className="mt-2 text-sm text-muted-foreground">No source image URL in the report.</p></section>}<ReportCard title="Reconstruction confidence evaluation" data={ai} /><ReportCard title="Mesh quality evaluation" data={mesh} /></div></div>
      <div className="grid gap-5 lg:grid-cols-2"><PromptEditPanel projectId={id} onUpdated={refreshReport} /><ExportActions projectId={id} /></div>
      <section className="rounded-xl border border-border bg-card p-5"><h2 className="flex items-center gap-2 font-semibold"><FiBox /> Full report fields</h2><p className="mt-1 text-sm text-muted-foreground">This page reads the merged <code>full_report</code> returned by the backend contract.</p>{report.project?.status && <p className="mt-3 text-sm">Project status: <strong>{report.project.status}</strong></p>}{meshUrl && <a className="mt-3 inline-flex items-center gap-2 text-sm text-indigo-600" href={meshUrl} target="_blank" rel="noreferrer">Open mesh asset <FiExternalLink /></a>}</section></>}
  </div>
}
