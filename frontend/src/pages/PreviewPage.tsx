import { lazy, Suspense, useEffect, useRef, useState } from 'react'
import { FiBox, FiCheckCircle, FiUploadCloud, FiX } from 'react-icons/fi'
import { Button } from '../components/ui/Button'

const ModelViewer = lazy(() => import('../viewer/ModelViewer'))
const maxFileSize = 100 * 1024 * 1024

export default function PreviewPage() {
  const [file, setFile] = useState<File | null>(null)
  const [error, setError] = useState('')
  const [dragging, setDragging] = useState(false)
  const [previewUrl, setPreviewUrl] = useState<string>()
  const inputRef = useRef<HTMLInputElement>(null)

  useEffect(() => {
    if (!file) {
      setPreviewUrl(undefined)
      return
    }
    const objectUrl = URL.createObjectURL(file)
    setPreviewUrl(objectUrl)
    return () => URL.revokeObjectURL(objectUrl)
  }, [file])

  function chooseFile(next?: File) {
    setError('')
    if (!next) return
    if (!next.name.toLowerCase().endsWith('.glb')) {
      setError('Choose a .glb file. This preview accepts binary glTF models.')
      return
    }
    if (next.size > maxFileSize) {
      setError('The model must be 100 MB or smaller.')
      return
    }
    setFile(next)
  }

  function clearFile() {
    setFile(null)
    setError('')
    if (inputRef.current) inputRef.current.value = ''
  }

  return (
    <div className="mx-auto max-w-6xl space-y-6">
      <header>
        <p className="text-sm font-medium text-indigo-600">Model workspace</p>
        <h1 className="mt-1 text-3xl font-semibold">3D Preview</h1>
        <p className="mt-2 max-w-2xl text-muted-foreground">
          Open a GLB model and inspect it in an interactive viewer. Your file is previewed locally in this browser.
        </p>
      </header>

      {!file ? (
        <section
          onDragOver={(event) => { event.preventDefault(); setDragging(true) }}
          onDragLeave={() => setDragging(false)}
          onDrop={(event) => {
            event.preventDefault()
            setDragging(false)
            chooseFile(event.dataTransfer.files[0])
          }}
          className={`rounded-2xl border-2 border-dashed p-8 text-center transition-colors sm:p-14 ${dragging ? 'border-primary bg-indigo-50' : 'border-border bg-card'}`}
        >
          <span className="mx-auto grid h-14 w-14 place-items-center rounded-2xl bg-indigo-50 text-indigo-600">
            <FiBox className="h-7 w-7" />
          </span>
          <h2 className="mt-5 text-lg font-semibold">Choose a 3D model</h2>
          <p className="mt-1 text-sm text-muted-foreground">Drop a .glb file here or select it from your device. Maximum size: 100 MB.</p>
          <Button className="mt-5" variant="outline" onClick={() => inputRef.current?.click()}>
            <FiUploadCloud /> Select GLB file
          </Button>
          <input
            ref={inputRef}
            type="file"
            accept=".glb,model/gltf-binary"
            className="hidden"
            onChange={(event) => {
              const selected = event.target.files?.[0]
              event.target.value = ''
              chooseFile(selected)
            }}
          />
          {error && <p role="alert" className="mx-auto mt-4 max-w-xl rounded-md bg-red-50 p-3 text-sm text-red-700">{error}</p>}
        </section>
      ) : (
        <>
          <section className="flex flex-wrap items-center justify-between gap-3 rounded-xl border border-border bg-card p-4">
            <div className="flex min-w-0 items-center gap-3">
              <span className="grid h-10 w-10 shrink-0 place-items-center rounded-lg bg-emerald-50 text-emerald-700"><FiCheckCircle /></span>
              <div className="min-w-0">
                <p className="truncate text-sm font-medium">{file.name}</p>
                <p className="text-xs text-muted-foreground">{(file.size / 1024 / 1024).toFixed(2)} MB · GLB model</p>
              </div>
            </div>
            <div className="flex gap-2">
              <Button variant="outline" onClick={() => inputRef.current?.click()}>Choose another</Button>
              <Button variant="ghost" size="icon" onClick={clearFile} aria-label="Remove model"><FiX /></Button>
            </div>
            <input
              ref={inputRef}
              type="file"
              accept=".glb,model/gltf-binary"
              className="hidden"
              onChange={(event) => {
                const selected = event.target.files?.[0]
                event.target.value = ''
                chooseFile(selected)
              }}
            />
          </section>
          {error && <p role="alert" className="rounded-md bg-red-50 p-3 text-sm text-red-700">{error}</p>}
          <Suspense fallback={<div className="grid h-[420px] place-items-center rounded-xl border border-border bg-card text-sm text-muted-foreground">Loading 3D model…</div>}>
            <ModelViewer key={previewUrl} url={previewUrl} />
          </Suspense>
        </>
      )}
    </div>
  )
}
