import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { FiArrowUpRight, FiBox, FiClock, FiPlus, FiTrendingUp } from 'react-icons/fi'
import { Button } from '../components/ui/Button'
import { Card, CardContent } from '../components/ui/Card'
import { projectService } from '../services/projectService'
import type { ProjectSummary } from '../types/api'

export default function DashboardPage() {
  const [projects, setProjects] = useState<ProjectSummary[]>([])
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(true)
  useEffect(() => { projectService.list().then(setProjects).catch((cause: unknown) => setError(cause instanceof Error ? cause.message : 'Could not load projects.')).finally(() => setLoading(false)) }, [])
  const stats = [
    { label: 'Total projects', value: loading ? '—' : projects.length, icon: FiBox },
    { label: 'Completed', value: loading ? '—' : projects.filter((project) => project.status?.toLowerCase() === 'completed').length, icon: FiTrendingUp },
    { label: 'In progress', value: loading ? '—' : projects.filter((project) => ['running', 'processing', 'pending'].includes(project.status?.toLowerCase() || '')).length, icon: FiClock },
  ]
  return <div className="space-y-8"><div className="flex flex-wrap items-end justify-between gap-4"><div><p className="text-sm font-medium text-indigo-600">Workspace</p><h1 className="mt-1 text-3xl font-semibold">Dashboard</h1><p className="mt-2 text-muted-foreground">Your reconstruction projects at a glance.</p></div><Link to="/upload"><Button><FiPlus /> New project</Button></Link></div>
    <div className="grid gap-4 sm:grid-cols-3">{stats.map(({ label, value, icon: Icon }) => <Card key={label}><CardContent className="flex items-center justify-between p-5"><div><p className="text-sm text-muted-foreground">{label}</p><p className="mt-2 text-3xl font-semibold">{value}</p></div><span className="rounded-lg bg-indigo-50 p-3 text-indigo-600"><Icon /></span></CardContent></Card>)}</div>
    <section><div className="mb-4 flex items-center justify-between"><h2 className="text-lg font-semibold">Recent projects</h2><Link to="/history" className="flex items-center gap-1 text-sm text-indigo-600">View history <FiArrowUpRight /></Link></div>
      {error && <p role="alert" className="rounded-lg bg-red-50 p-4 text-sm text-red-700">{error}</p>}
      {!error && !loading && projects.length === 0 && <Card><CardContent className="py-12 text-center"><FiBox className="mx-auto h-8 w-8 text-muted-foreground" /><h3 className="mt-3 font-medium">No projects yet</h3><p className="mt-1 text-sm text-muted-foreground">Upload an image to start your first reconstruction.</p><Link to="/upload"><Button className="mt-4"><FiPlus /> Create project</Button></Link></CardContent></Card>}
      <div className="grid gap-3 md:grid-cols-2">{projects.slice(0, 6).map((project) => <Link key={project.id} to={`/results/${encodeURIComponent(project.id)}`}><Card className="transition hover:border-indigo-300"><CardContent className="flex items-center gap-4 p-4">{project.thumbnail_url ? <img src={project.thumbnail_url} alt="" className="h-14 w-14 rounded-lg object-cover" /> : <span className="grid h-14 w-14 place-items-center rounded-lg bg-muted"><FiBox /></span>}<span className="min-w-0 flex-1"><span className="block truncate font-medium">{project.name || `Project ${project.id}`}</span><span className="mt-1 block text-xs text-muted-foreground">{project.status || 'Status unavailable'}</span></span><FiArrowUpRight /></CardContent></Card></Link>)}</div>
    </section>
    <Card><CardContent className="flex flex-wrap items-center justify-between gap-4 p-5"><div><h2 className="font-semibold">Recommended pipeline</h2><p className="mt-1 text-sm text-muted-foreground">Upload an image to begin classification and model selection.</p></div><Link to="/upload"><Button variant="outline">Upload an image <FiArrowUpRight /></Button></Link></CardContent></Card>
  </div>
}
