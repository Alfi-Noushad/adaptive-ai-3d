import { api, unwrap } from './api'
import type { ApiEnvelope, BackendProjectSummary, ProjectReport, ProjectSummary, UploadData } from '../types/api'

function normalizeProject(project: BackendProjectSummary): ProjectSummary {
  const id = project.id ?? project.project_id
  return {
    id: id === undefined ? '' : String(id),
    name: project.name || project.title,
    status: project.status,
    created_at: project.created_at,
    thumbnail_url: project.thumbnail_url,
  }
}

export const projectService = {
  async upload(file: File, onProgress?: (percent: number) => void) {
    const form = new FormData()
    form.append('file', file)
    return unwrap((await api.post<ApiEnvelope<UploadData>>('/upload', form, {
      headers: { 'Content-Type': 'multipart/form-data' },
      onUploadProgress: (event) => { if (event.total) onProgress?.(Math.round((event.loaded / event.total) * 100)) },
    })).data)
  },
  async list() {
    return unwrap((await api.get<ApiEnvelope<BackendProjectSummary[]>>('/projects')).data).map(normalizeProject)
  },
  async getReport(id: string) {
    return unwrap((await api.get<ApiEnvelope<ProjectReport>>(`/projects/${encodeURIComponent(id)}/report`)).data)
  },
  async get(id: string) {
    return normalizeProject(unwrap((await api.get<ApiEnvelope<BackendProjectSummary>>(`/projects/${encodeURIComponent(id)}`)).data))
  },
  async promptEdit(projectId: string, prompt: string) {
    return unwrap((await api.post<ApiEnvelope<Record<string, unknown>>>('/prompt-edit', { project_id: projectId, prompt })).data)
  },
  async recommendations(projectId: string) {
    return unwrap((await api.get<ApiEnvelope<unknown>>(`/recommendations/${encodeURIComponent(projectId)}`)).data)
  },
  async history() {
    return unwrap((await api.get<ApiEnvelope<BackendProjectSummary[]>>('/history')).data).map(normalizeProject)
  },
}
