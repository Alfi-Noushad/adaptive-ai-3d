import { api, unwrap } from './api'
import type { ApiEnvelope, ProjectReport, ProjectSummary, UploadData } from '../types/api'

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
    return unwrap((await api.get<ApiEnvelope<ProjectSummary[]>>('/projects')).data)
  },
  async getReport(id: string) {
    return unwrap((await api.get<ApiEnvelope<ProjectReport>>(`/projects/${encodeURIComponent(id)}/report`)).data)
  },
  async get(id: string) {
    return unwrap((await api.get<ApiEnvelope<ProjectSummary>>(`/projects/${encodeURIComponent(id)}`)).data)
  },
  async promptEdit(projectId: string, prompt: string) {
    return unwrap((await api.post<ApiEnvelope<Record<string, unknown>>>('/prompt-edit', { project_id: projectId, prompt })).data)
  },
  async recommendations(projectId: string) {
    return unwrap((await api.get<ApiEnvelope<unknown>>(`/recommendations/${encodeURIComponent(projectId)}`)).data)
  },
  async history() {
    return unwrap((await api.get<ApiEnvelope<ProjectSummary[]>>('/history')).data)
  },
}
