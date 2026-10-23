import { useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import { FiArrowLeft, FiMove, FiRotateCw, FiZoomIn } from 'react-icons/fi'
import { Button } from '../components/ui/Button'

export default function ARPage() {
  const { id = '' } = useParams()
  const [scale, setScale] = useState(1)
  const [rotation, setRotation] = useState(0)
  const [placed, setPlaced] = useState(false)
  return <div className="mx-auto max-w-3xl"><Link to={`/results/${encodeURIComponent(id)}`} className="inline-flex items-center gap-2 text-sm text-muted-foreground"><FiArrowLeft /> Results</Link><h1 className="mt-4 text-3xl font-semibold">AR preview</h1><p className="mt-2 text-muted-foreground">WebXR placement can be connected when the backend and target device are ready.</p><div className="mt-6 grid min-h-80 place-items-center rounded-2xl border border-dashed border-border bg-slate-100"><div className="text-center"><div className="mx-auto grid h-28 w-28 place-items-center rounded-3xl bg-indigo-500 text-white shadow-xl" style={{ transform: `scale(${scale}) rotate(${rotation}deg)` }}><FiMove className="h-12 w-12" /></div><p className="mt-5 text-sm font-medium">{placed ? 'Model placed in preview' : 'AR placement preview'}</p><p className="mt-1 text-xs text-muted-foreground">Project {id}</p></div></div><div className="mt-4 flex flex-wrap justify-center gap-2"><Button variant="outline" onClick={() => setPlaced((value) => !value)}>{placed ? 'Reset placement' : 'Place model'}</Button><Button variant="outline" onClick={() => setRotation((value) => value + 15)}><FiRotateCw /> Rotate</Button><Button variant="outline" onClick={() => setScale((value) => Math.min(1.6, value + 0.1))}><FiZoomIn /> Scale</Button></div><p className="mt-4 text-center text-xs text-muted-foreground">Move, rotate, and scale controls are local preview controls; this page does not claim a live WebXR session.</p></div>
}
