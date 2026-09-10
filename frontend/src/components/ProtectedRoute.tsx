import { Navigate, Outlet } from 'react-router-dom';

export default function ProtectedRoute() {
  // Dynamically check the browser's local storage for a session
  const isAuthenticated = localStorage.getItem('nexus_auth') === 'true';
  
  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  return <Outlet />;
}