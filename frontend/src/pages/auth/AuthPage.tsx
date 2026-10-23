import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { z } from 'zod'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { FiBox, FiLoader } from 'react-icons/fi'
import { Button } from '../../components/ui/Button'
import { authService } from '../../services/authService'
import { useAuthStore } from '../../store/authStore'
import type { User } from '../../store/authStore'

type Mode = 'login' | 'register' | 'forgot'
const baseSchema = z.object({
  name: z.string().trim().min(2, 'Enter your name').optional(),
  email: z.string().trim().email('Enter a valid email'),
  password: z.string().optional(),
})
type FormValues = z.infer<typeof baseSchema>

function schemaForMode(mode: Mode) {
  return baseSchema.superRefine((values, context) => {
    if (mode === 'register' && !values.name?.trim()) {
      context.addIssue({ code: 'custom', path: ['name'], message: 'Enter your name' })
    }
    if (mode !== 'forgot' && !values.password) {
      context.addIssue({ code: 'custom', path: ['password'], message: 'Password is required' })
    } else if (mode === 'register' && (values.password?.length || 0) < 8) {
      context.addIssue({ code: 'custom', path: ['password'], message: 'Use at least 8 characters' })
    }
  })
}

export default function AuthPage({ mode }: { mode: Mode }) {
  const [error, setError] = useState('')
  const [notice, setNotice] = useState('')
  const navigate = useNavigate()
  const login = useAuthStore((state) => state.login)
  const { register, handleSubmit, formState: { errors, isSubmitting } } = useForm<FormValues>({ resolver: zodResolver(schemaForMode(mode)) })

  const submit = handleSubmit(async (values) => {
    setError(''); setNotice('')
    try {
      if (mode === 'forgot') {
        await authService.forgotPassword(values.email)
        setNotice('If an account exists for this email, password reset instructions have been sent.')
        return
      }
      const result = mode === 'login'
        ? await authService.login(values.email, values.password || '')
        : await (async () => {
          await authService.register(values.name || '', values.email, values.password || '')
          return authService.login(values.email, values.password || '')
        })()
      if (!result.access_token) throw new Error('The server response did not include an access token.')
      const user: User = {
        id: result.user?.id || values.email,
        name: result.user?.name || values.name || values.email.split('@')[0],
        email: result.user?.email || values.email,
        role: result.user?.role || 'user',
      }
      login(user, result.access_token)
      navigate('/dashboard', { replace: true })
    } catch (cause) {
      setError(cause instanceof Error ? cause.message : 'Something went wrong. Please try again.')
    }
  })

  const title = mode === 'login' ? 'Welcome back' : mode === 'register' ? 'Create your account' : 'Reset your password'
  return (
    <main className="grid min-h-screen bg-background lg:grid-cols-2">
      <section className="hidden flex-col justify-between bg-slate-950 p-12 text-white lg:flex">
        <Link to="/" className="flex items-center gap-3 text-lg font-semibold"><FiBox className="text-indigo-300" /> Adaptive AI 3D</Link>
        <div className="max-w-lg"><p className="mb-4 text-sm font-medium uppercase tracking-[0.22em] text-indigo-300">Research workspace</p><h1 className="text-4xl font-semibold leading-tight">Turn a single image into an adaptive 3D workflow.</h1><p className="mt-5 text-slate-300">Upload, evaluate, and inspect reconstruction projects in one place.</p></div>
        <p className="text-xs text-slate-400">Adaptive AI Framework for Intelligent Multi-Model 2D-to-3D Asset Generation, Optimization and Visualization</p>
      </section>
      <section className="flex items-center justify-center p-6 sm:p-10">
        <div className="w-full max-w-md">
          <Link to="/" className="mb-10 flex items-center gap-2 font-semibold lg:hidden"><FiBox /> Adaptive AI 3D</Link>
          <p className="text-sm font-medium text-indigo-600">Your 3D research workspace</p>
          <h2 className="mt-2 text-3xl font-semibold tracking-tight">{title}</h2>
          <p className="mt-2 text-sm text-muted-foreground">{mode === 'login' ? 'Sign in to continue to your projects.' : mode === 'register' ? 'Create an account to start a project.' : 'Enter your email and we’ll send reset instructions.'}</p>
          <form className="mt-8 space-y-5" onSubmit={submit} noValidate>
            {mode === 'register' && <Field label="Name" error={errors.name?.message}><input autoComplete="name" className={inputClass} {...register('name')} /></Field>}
            <Field label="Email" error={errors.email?.message}><input type="email" autoComplete="email" className={inputClass} {...register('email')} /></Field>
            {mode !== 'forgot' && <Field label="Password" error={errors.password?.message}><input type="password" autoComplete={mode === 'login' ? 'current-password' : 'new-password'} className={inputClass} {...register('password')} /></Field>}
            {error && <p role="alert" className="rounded-md bg-red-50 p-3 text-sm text-red-700">{error}</p>}
            {notice && <p role="status" className="rounded-md bg-emerald-50 p-3 text-sm text-emerald-700">{notice}</p>}
            <Button type="submit" className="w-full" disabled={isSubmitting}>{isSubmitting && <FiLoader className="animate-spin" />}{isSubmitting ? 'Please wait…' : mode === 'login' ? 'Sign in' : mode === 'register' ? 'Create account' : 'Send reset instructions'}</Button>
          </form>
          <div className="mt-6 flex justify-between text-sm">
            {mode === 'login' ? <><Link className="text-indigo-600 hover:underline" to="/forgot-password">Forgot password?</Link><Link className="text-indigo-600 hover:underline" to="/register">Create account</Link></> : <Link className="text-indigo-600 hover:underline" to="/login">Back to sign in</Link>}
          </div>
        </div>
      </section>
    </main>
  )
}

const inputClass = 'mt-1 block w-full rounded-md border border-border bg-background px-3 py-2.5 text-sm outline-none focus:ring-2 focus:ring-primary'
function Field({ label, error, children }: { label: string; error?: string; children: React.ReactNode }) {
  return <label className="block text-sm font-medium">{label}{children}{error && <span className="mt-1 block text-xs text-red-600">{error}</span>}</label>
}
