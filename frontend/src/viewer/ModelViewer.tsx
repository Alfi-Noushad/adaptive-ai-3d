import { Suspense, useState } from 'react'
import { Canvas } from '@react-three/fiber'
import { Bounds, Center, ContactShadows, Environment, OrbitControls, useGLTF } from '@react-three/drei'
import { FiBox, FiMaximize2, FiRotateCcw } from 'react-icons/fi'
import { Button } from '../components/ui/Button'

function Model({ url, wireframe }: { url: string; wireframe: boolean }) {
  const gltf = useGLTF(url)
  gltf.scene.traverse((child) => {
    if ('material' in child && child.material) {
      const materials = Array.isArray(child.material) ? child.material : [child.material]
      materials.forEach((material) => { if ('wireframe' in material) material.wireframe = wireframe })
    }
  })
  return <primitive object={gltf.scene} />
}

export default function ModelViewer({ url }: { url?: string }) {
  const [wireframe, setWireframe] = useState(false)
  const [resetKey, setResetKey] = useState(0)
  const [fullscreen, setFullscreen] = useState(false)
  return (
    <section className={fullscreen ? 'fixed inset-3 z-50 rounded-xl border border-border bg-card p-3 shadow-2xl' : 'overflow-hidden rounded-xl border border-border bg-card'}>
      <div className="flex items-center justify-between border-b border-border px-4 py-3">
        <div className="flex items-center gap-2 text-sm font-medium"><FiBox /> 3D preview</div>
        <div className="flex gap-1">
          <Button size="sm" variant={wireframe ? 'secondary' : 'ghost'} onClick={() => setWireframe((value) => !value)}>Wireframe</Button>
          <Button size="icon" variant="ghost" onClick={() => setResetKey((value) => value + 1)} aria-label="Reset camera"><FiRotateCcw /></Button>
          <Button size="icon" variant="ghost" onClick={() => setFullscreen((value) => !value)} aria-label={fullscreen ? 'Exit fullscreen' : 'Fullscreen'}><FiMaximize2 /></Button>
        </div>
      </div>
      <div className={fullscreen ? 'h-[calc(100%-3.5rem)]' : 'h-[420px]'}>
        <Canvas camera={{ position: [3, 2.4, 4], fov: 45 }} dpr={[1, 2]}>
          <color attach="background" args={['#f1f5f9']} />
          <ambientLight intensity={0.65} /><directionalLight position={[4, 5, 4]} intensity={2} />
          <Suspense fallback={null}>
            {url ? <Bounds fit clip observe><Center><Model url={url} wireframe={wireframe} /></Center></Bounds> : <mesh><icosahedronGeometry args={[1, 1]} /><meshStandardMaterial color="#6366f1" wireframe={wireframe} /></mesh>}
            <Environment preset="city" /><ContactShadows position={[0, -1.1, 0]} opacity={0.25} scale={6} blur={2.5} />
          </Suspense>
          <OrbitControls key={resetKey} makeDefault enableDamping />
          <gridHelper args={[10, 10, '#cbd5e1', '#e2e8f0']} />
        </Canvas>
      </div>
      {!url && <p className="border-t border-border px-4 py-2 text-xs text-muted-foreground">A generated mesh will appear here when the project report includes a mesh URL.</p>}
    </section>
  )
}
