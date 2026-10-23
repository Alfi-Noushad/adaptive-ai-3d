import { useEffect, useState } from 'react'
import { Link, useSearchParams } from 'react-router-dom'
import { FiCheckCircle, FiClock, FiLoader } from 'react-icons/fi'
import { projectService } from '../services/projectService'
import { Button } from '../components/ui/Button'

const stages = ['Image received', 'Classification', 'Quality assessment', 'Model selection', 'Reconstruction', 'Confidence evaluation', 'Mesh quality evaluation', 'Mesh optimization']
export default function ProcessingPage() {
  const [params] = useSearchParams()
  const id = params.get('project_id') || ''
  const [status, setStatus] = useState(id ? 'Loading project status…' : 'No project ID was provided.')
  const [error, setError] = useState('')
  useEffect(() => {
    if (!id) return
    let active = true
    projectService.get(id).then((project) => { if (active) setStatus(project.status || 'Project accepted. Processing status is not available yet.') }).catch((cause: unknown) => { if (active) setError(cause instanceof Error ? cause.message : 'Could not load project status.') })
    return () => { active = false }
  }, [id])
  return <div className="mx-auto max-w-3xl"><p className="text-sm font-medium text-indigo-600">Project {id || '—'}</p><h1 className="mt-1 text-3xl font-semibold">Processing</h1><p className="mt-2 text-muted-foreground">The project status comes from the backend project record.</p><section className="mt-8 rounded-xl border border-border bg-card p-6"><div className="flex items-center gap-3"><FiLoader className="h-5 w-5 animate-spin text-indigo-600" /><div><h2 className="font-semibold">{status}</h2><p className="mt-1 flex items-center gap-1 text-xs text-muted-foreground"><FiClock /> Stage updates are not exposed by the current frontend API contract.</p></div></div><ol className="mt-7 space-y-4">{stages.map((stage, index) => <li key={stage} className="flex items-center gap-3 text-sm"><span className={`grid h-7 w-7 place-items-center rounded-full ${index === 0 ? 'bg-indigo-100 text-indigo-700' : 'bg-muted text-muted-foreground'}`}>{index === 0 ? <FiCheckCircle /> : index + 1}</span><span className={index === 0 ? 'font-medium' : 'text-muted-foreground'}>{stage}</span></li>)}</ol>{error && <p role="alert" className="mt-5 text-sm text-red-600">{error}</p>}{id && <Link to={`/results/${encodeURIComponent(id)}`}><Button className="mt-6" variant="outline">Open project results</Button></Link>}</section>
  </div>
}
