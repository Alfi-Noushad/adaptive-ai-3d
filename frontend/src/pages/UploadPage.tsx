import { useRef, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { FiImage, FiLoader, FiUploadCloud, FiX } from 'react-icons/fi'
import { Button } from '../components/ui/Button'
import { projectService } from '../services/projectService'

const maxBytes = 15 * 1024 * 1024
const accepted = ['image/png', 'image/jpeg', 'image/webp']
export default function UploadPage() {
  const [file, setFile] = useState<File | null>(null)
  const [error, setError] = useState('')
  const [busy, setBusy] = useState(false)
  const [progress, setProgress] = useState(0)
  const [dragging, setDragging] = useState(false)
  const input = useRef<HTMLInputElement>(null)
  const navigate = useNavigate()
  function selectFile(next?: File) {
    setError('')
    if (!next) return
    if (!accepted.includes(next.type)) return setError('Choose a PNG, JPG, or WebP image.')
    if (next.size > maxBytes) return setError('Image must be 15 MB or smaller.')
    setFile(next)
  }
  async function upload() {
    if (!file) return
    setBusy(true); setError('')
    try {
      const result = await projectService.upload(file, setProgress)
      const id = result.project_id || result.id || result.project?.id
      if (!id) throw new Error('The upload succeeded but the response did not include a project ID.')
      navigate(`/processing?project_id=${encodeURIComponent(id)}`)
    } catch (cause) { setError(cause instanceof Error ? cause.message : 'Upload failed.') }
    finally { setBusy(false) }
  }
  return <div className="mx-auto max-w-3xl"><p className="text-sm font-medium text-indigo-600">New project</p><h1 className="mt-1 text-3xl font-semibold">Upload an image</h1><p className="mt-2 text-muted-foreground">Start a reconstruction with one clear image of your object.</p>
    <div onDragOver={(event) => { event.preventDefault(); setDragging(true) }} onDragLeave={() => setDragging(false)} onDrop={(event) => { event.preventDefault(); setDragging(false); selectFile(event.dataTransfer.files[0]) }} className={`mt-8 rounded-2xl border-2 border-dashed p-8 text-center transition-colors sm:p-14 ${dragging ? 'border-primary bg-indigo-50' : 'border-border bg-card'}`}>
      {file ? <div className="mx-auto max-w-md"><div className="mx-auto grid h-16 w-16 place-items-center rounded-xl bg-muted text-primary"><FiImage className="h-7 w-7" /></div><p className="mt-4 truncate font-medium">{file.name}</p><p className="mt-1 text-sm text-muted-foreground">{(file.size / 1024 / 1024).toFixed(2)} MB · {file.type}</p><button onClick={() => { setFile(null); if (input.current) input.current.value = '' }} className="mt-3 inline-flex items-center gap-1 text-sm text-muted-foreground hover:text-foreground"><FiX /> Remove image</button></div> : <><FiUploadCloud className="mx-auto h-10 w-10 text-indigo-500" /><h2 className="mt-4 text-lg font-semibold">Drop your image here</h2><p className="mt-1 text-sm text-muted-foreground">PNG, JPG, or WebP · up to 15 MB</p><Button className="mt-5" variant="outline" onClick={() => input.current?.click()}>Browse files</Button></>}
      <input ref={input} type="file" accept="image/png,image/jpeg,image/webp" className="hidden" onChange={(event) => selectFile(event.target.files?.[0])} />
    </div>
    {error && <p role="alert" className="mt-4 rounded-md bg-red-50 p-3 text-sm text-red-700">{error}</p>}
    {busy && <div className="mt-5" role="status"><div className="mb-1 flex justify-between text-xs text-muted-foreground"><span>Upload progress</span><span>{progress}%</span></div><div className="h-2 overflow-hidden rounded-full bg-muted"><div className="h-full rounded-full bg-primary transition-[width]" style={{ width: `${progress}%` }} /></div></div>}
    <div className="mt-5 flex justify-end"><Button onClick={upload} disabled={!file || busy}>{busy && <FiLoader className="animate-spin" />}{busy ? 'Uploading…' : 'Upload and continue'}</Button></div>
  </div>
}
