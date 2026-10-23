import axios, { AxiosError } from 'axios'
import type { ApiEnvelope } from '../types/api'

export const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000',
  timeout: 30_000,
})

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token')
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

api.interceptors.response.use(
  (response) => response,
  (error: AxiosError<ApiEnvelope<unknown>>) => {
    if (!error.response) {
      const baseURL = error.config?.baseURL || api.defaults.baseURL || 'the configured API URL'
      return Promise.reject(new Error(error.code === 'ECONNABORTED'
        ? `The API at ${baseURL} timed out. Please try again.`
        : `Cannot reach the API at ${baseURL}. Start the backend and check VITE_API_BASE_URL.`))
    }
    const payload = error.response.data
    const detail = (payload as unknown as { detail?: string })?.detail
    const message = payload?.message || (typeof payload?.error === 'string' ? payload.error : undefined) || detail
    return Promise.reject(new Error(message || `Request failed (${error.response.status}). Please try again.`))
  },
)

export function unwrap<T>(payload: ApiEnvelope<T>): T {
  if (payload.status !== 'success') throw new Error(payload.message || 'The request failed.')
  return payload.data
}
