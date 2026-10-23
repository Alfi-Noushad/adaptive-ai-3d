import { FiMenu, FiLogOut } from 'react-icons/fi'
import { useNavigate } from 'react-router-dom'
import { useAuthStore } from '../../store/authStore'
import { Button } from '../ui/Button'
import ThemeToggle from '../ThemeToggle'
import { authService } from '../../services/authService'

interface NavbarProps {
  onMenuClick: () => void
}

export default function Navbar({ onMenuClick }: NavbarProps) {
  const user = useAuthStore((state) => state.user)
  const logout = useAuthStore((state) => state.logout)
  const navigate = useNavigate()

  const handleLogout = async () => {
    try { await authService.logout() } catch { /* Local credentials are cleared even if the server is unavailable. */ }
    await logout()
    navigate('/login')
  }

  return (
    <header className="sticky top-0 z-20 flex h-16 items-center justify-between border-b border-border bg-background/95 px-4 backdrop-blur md:px-8">
      <div className="flex items-center gap-3">
        <Button variant="ghost" size="icon" className="md:hidden" onClick={onMenuClick} aria-label="Open navigation">
          <FiMenu className="h-5 w-5" />
        </Button>
        <span className="font-semibold">Adaptive AI 3D</span>
      </div>
      <div className="flex items-center gap-2">
        {user && <span className="hidden text-sm text-muted-foreground sm:inline">{user.name}</span>}
        <ThemeToggle />
        <Button variant="ghost" size="icon" onClick={handleLogout} aria-label="Sign out">
          <FiLogOut className="h-4 w-4" />
        </Button>
      </div>
    </header>
  )
}
