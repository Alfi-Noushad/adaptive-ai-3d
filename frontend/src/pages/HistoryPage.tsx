import { useEffect, useMemo, useState } from 'react'
import { Link } from 'react-router-dom'
import { FiBox, FiSearch } from 'react-icons/fi'
import { projectService } from '../services/projectService'
import type { ProjectSummary } from '../types/api'
import { Card, CardContent } from '../components/ui/Card'

export default function HistoryPage() {
  const [items, setItems] = useState<ProjectSummary[]>([])
  const [search, setSearch] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(true)
  useEffect(() => { projectService.history().then(setItems).catch((cause: unknown) => setError(cause instanceof Error ? cause.message : 'Could not load project history.')).finally(() => setLoading(false)) }, [])
  const filtered = useMemo(() => items.filter((item) => `${item.name || ''} ${item.id} ${item.status || ''}`.toLowerCase().includes(search.toLowerCase())), [items, search])
  return <div><p className="text-sm font-medium text-indigo-600">Workspace</p><h1 className="mt-1 text-3xl font-semibold">Project history</h1><div className="relative mt-6 max-w-md"><FiSearch className="absolute left-3 top-3 text-muted-foreground" /><input value={search} onChange={(event) => setSearch(event.target.value)} placeholder="Search projects" className="w-full rounded-md border border-border bg-card py-2.5 pl-9 pr-3 text-sm" /></div>
    {loading && <p className="mt-6 text-sm text-muted-foreground">Loading history…</p>}{error && <p role="alert" className="mt-6 rounded-lg bg-red-50 p-4 text-sm text-red-700">{error}</p>}
    {!loading && !error && !filtered.length && <Card className="mt-6"><CardContent className="py-12 text-center"><FiBox className="mx-auto h-8 w-8 text-muted-foreground" /><p className="mt-3 font-medium">No matching projects</p><p className="mt-1 text-sm text-muted-foreground">Uploaded project history will appear here.</p></CardContent></Card>}
    <div className="mt-6 grid gap-3 md:grid-cols-2">{filtered.map((item) => <Link to={`/results/${encodeURIComponent(item.id)}`} key={item.id}><Card className="hover:border-indigo-300"><CardContent className="flex items-center gap-4 p-4">{item.thumbnail_url ? <img src={item.thumbnail_url} alt="" className="h-14 w-14 rounded-lg object-cover" /> : <span className="grid h-14 w-14 place-items-center rounded-lg bg-muted"><FiBox /></span>}<span className="min-w-0 flex-1"><span className="block truncate font-medium">{item.name || `Project ${item.id}`}</span><span className="text-sm text-muted-foreground">{item.status || 'Status unavailable'}{item.created_at ? ` · ${new Date(item.created_at).toLocaleDateString()}` : ''}</span></span></CardContent></Card></Link>)}</div>
  </div>
}
