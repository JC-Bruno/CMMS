import { Navigate, Outlet } from "react-router-dom";

import { useAuth } from "@modules/auth/hooks/useAuth";

export function GuestRoute() {
  const { isAuthenticated, isLoading } = useAuth();

  if (isLoading) {
    return <div className="auth-loading">Validando sesión...</div>;
  }

  if (isAuthenticated) {
    return <Navigate to="/" replace />;
  }

  return <Outlet />;
}