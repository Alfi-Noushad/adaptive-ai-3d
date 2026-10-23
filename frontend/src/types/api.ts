export interface ApiEnvelope<T> {
  status: 'success' | 'error'
  message: string
  data: T
  error: string | Record<string, unknown> | null
  timestamp: string
}

export interface ProjectSummary {
  id: string
  name?: string
  status?: string
  created_at?: string
  thumbnail_url?: string
}

export interface BackendProjectSummary {
  id?: string | number
  project_id?: string | number
  name?: string
  title?: string
  status?: string
  created_at?: string
  thumbnail_url?: string
}

export interface ProjectReport {
  full_report?: ProjectReport
  project?: ProjectSummary
  original_image_url?: string
  mesh_url?: string
  optimized_mesh_url?: string
  ai_evaluation_report?: Record<string, unknown>
  mesh_quality_report?: Record<string, unknown>
  [key: string]: unknown
}

export interface AuthData {
  access_token?: string
  refresh_token?: string
  token_type?: string
  user?: { id: string; name?: string; email: string; role?: string }
}

export interface UploadData {
  project_id?: string | number
  id?: string | number
  project?: BackendProjectSummary
}
