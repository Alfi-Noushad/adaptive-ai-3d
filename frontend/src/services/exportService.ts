import { api, unwrap } from './api'
import type { ApiEnvelope } from '../types/api'

export type ExportFormat = 'obj' | 'glb' | 'fbx' | 'ply' | 'stl' | 'blender'

export async function requestExport(format: ExportFormat, projectId: string) {
  const response = await api.post<ApiEnvelope<{ job_id?: string; download_url?: string }>>(`/export/${format}`, { project_id: projectId })
  return unwrap(response.data)
}
