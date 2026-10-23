import { Link } from 'react-router-dom'
import { FiArrowRight, FiUser } from 'react-icons/fi'
import { useAuthStore } from '../store/authStore'
import { Card, CardContent } from '../components/ui/Card'

export default function ProfilePage() {
  const user = useAuthStore((state) => state.user)
  return <div className="mx-auto max-w-3xl"><p className="text-sm font-medium text-indigo-600">Account</p><h1 className="mt-1 text-3xl font-semibold">Profile</h1><Card className="mt-6"><CardContent className="flex items-start gap-4 p-6"><span className="grid h-12 w-12 place-items-center rounded-full bg-indigo-100 text-indigo-700"><FiUser /></span><div><h2 className="font-semibold">{user?.name || 'Account user'}</h2><p className="mt-1 text-sm text-muted-foreground">{user?.email || 'User details are not available.'}</p><p className="mt-1 text-xs capitalize text-muted-foreground">{user?.role || 'member'}</p></div></CardContent></Card><div className="mt-4 grid gap-4 sm:grid-cols-2"><Card><CardContent className="p-5"><p className="text-sm text-muted-foreground">Project count</p><p className="mt-2 text-sm">See your current project history.</p><Link to="/history" className="mt-3 inline-flex items-center gap-2 text-sm text-indigo-600">Open history <FiArrowRight /></Link></CardContent></Card><Card><CardContent className="p-5"><p className="text-sm text-muted-foreground">Appearance</p><p className="mt-2 text-sm">Change the workspace theme from the navbar.</p></CardContent></Card></div><p className="mt-5 text-xs text-muted-foreground">Password changes and storage usage are not exposed by the current API contract.</p></div>
}
