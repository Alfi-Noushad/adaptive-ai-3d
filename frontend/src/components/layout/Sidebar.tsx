import { NavLink } from 'react-router-dom'
import { FiActivity, FiBox, FiClock, FiFolder, FiSettings, FiUser, FiUpload, FiX } from 'react-icons/fi'
import { cn } from '../../utils/cn'
import { Button } from '../ui/Button'

const links = [
  { to: '/dashboard', label: 'Dashboard', icon: FiActivity },
  { to: '/preview', label: '3D Preview', icon: FiBox },
  { to: '/upload', label: 'Upload', icon: FiUpload },
  { to: '/history', label: 'History', icon: FiClock },
  { to: '/profile', label: 'Profile', icon: FiUser },
  { to: '/settings', label: 'Settings', icon: FiSettings },
]

interface SidebarProps {
  open: boolean
  onClose: () => void
}

export default function Sidebar({ open, onClose }: SidebarProps) {
  return (
    <>
      {open && <button className="fixed inset-0 z-30 bg-black/40 md:hidden" onClick={onClose} aria-label="Close navigation" />}
      <aside className={cn('fixed inset-y-0 left-0 z-40 flex w-64 flex-col border-r border-border bg-card p-4 transition-transform md:static md:translate-x-0', open ? 'translate-x-0' : '-translate-x-full')}>
        <div className="mb-8 flex h-12 items-center justify-between px-2">
          <span className="text-lg font-bold">Adaptive AI 3D</span>
          <Button variant="ghost" size="icon" className="md:hidden" onClick={onClose} aria-label="Close navigation"><FiX /></Button>
        </div>
        <nav className="flex flex-1 flex-col gap-1">
          {links.map(({ to, label, icon: Icon }) => (
            <NavLink key={to} to={to} onClick={onClose} className={({ isActive }) => cn('flex items-center gap-3 rounded-md px-3 py-2 text-sm font-medium text-muted-foreground hover:bg-muted hover:text-foreground', isActive && 'bg-muted text-foreground')}>
              <Icon className="h-4 w-4" />{label}
            </NavLink>
          ))}
        </nav>
        <div className="flex items-center gap-2 px-3 py-2 text-xs text-muted-foreground"><FiFolder className="h-4 w-4" /> Research workspace</div>
      </aside>
    </>
  )
}
