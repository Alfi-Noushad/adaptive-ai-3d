import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom'
import ProtectedRoute from './components/ProtectedRoute'
import AppLayout from './components/layout/AppLayout'
import { Button } from './components/ui/Button'
import { useThemeSync } from './hooks/useThemeSync'
import LoginPage from './pages/auth/Loginpage'
import RegisterPage from './pages/auth/RegisterPage'
import ForgotPasswordPage from './pages/auth/ForgotPasswordPage'
import DashboardPage from './pages/DashboardPage'
import PreviewPage from './pages/PreviewPage'
import UploadPage from './pages/UploadPage'
import ProcessingPage from './pages/ProcessingPage'
import ResultsPage from './pages/ResultsPage'
import HistoryPage from './pages/HistoryPage'
import ProfilePage from './pages/ProfilePage'
import ARPage from './pages/ARPage'

function LandingPage() {
  return <main className="grid min-h-screen place-items-center bg-background px-6"><div className="max-w-2xl text-center"><p className="text-sm font-medium uppercase tracking-widest text-indigo-600">Adaptive AI 3D</p><h1 className="mt-4 text-4xl font-semibold tracking-tight sm:text-5xl">From a single image to a reviewable 3D project.</h1><p className="mt-5 text-lg text-muted-foreground">Upload, inspect reconstruction reports, and export your generated asset.</p><div className="mt-8 flex justify-center gap-3"><a href="/login"><Button>Sign in</Button></a><a href="/register"><Button variant="outline">Create account</Button></a></div><p className="mt-8 text-xs text-muted-foreground">Adaptive AI Framework for Intelligent Multi-Model 2D-to-3D Asset Generation, Optimization and Visualization</p></div></main>
}

function NotFound() {
  return <main className="grid min-h-screen place-items-center px-6 text-center"><div><p className="text-sm font-medium text-indigo-600">404</p><h1 className="mt-2 text-3xl font-semibold">Page not found</h1><a href="/"><Button className="mt-5">Return home</Button></a></div></main>
}

export default function App() {
  useThemeSync()
  return <BrowserRouter><Routes>
    <Route path="/" element={<LandingPage />} />
    <Route path="/login" element={<LoginPage />} />
    <Route path="/register" element={<RegisterPage />} />
    <Route path="/forgot-password" element={<ForgotPasswordPage />} />
    <Route element={<ProtectedRoute />}><Route element={<AppLayout />}>
      <Route path="/dashboard" element={<DashboardPage />} />
      <Route path="/preview" element={<PreviewPage />} />
      <Route path="/upload" element={<UploadPage />} />
      <Route path="/processing" element={<ProcessingPage />} />
      <Route path="/results/:id" element={<ResultsPage />} />
      <Route path="/ar/:id" element={<ARPage />} />
      <Route path="/history" element={<HistoryPage />} />
      <Route path="/profile" element={<ProfilePage />} />
      <Route path="/settings" element={<Navigate to="/profile" replace />} />
    </Route></Route>
    <Route path="/about" element={<LandingPage />} />
    <Route path="*" element={<NotFound />} />
  </Routes></BrowserRouter>
}
