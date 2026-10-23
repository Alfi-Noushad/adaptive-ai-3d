import { useEffect } from 'react'
import { useThemeStore } from '../store/themeStore'

export function useThemeSync() {
  const theme = useThemeStore((state) => state.theme)

  useEffect(() => {
    document.documentElement.classList.toggle('dark', theme === 'dark')
    window.localStorage.setItem('theme', theme)
  }, [theme])
}
