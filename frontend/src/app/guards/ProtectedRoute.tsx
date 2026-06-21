import { Navigate, Outlet } from "react-router-dom";

import { useAuth } from "@modules/auth/hooks/useAuth";

export function ProtectedRoute() {
  const { isAuthenticated, isLoading } = useAuth();

  if (isLoading) {
    return <div className="auth-loading">Validando sesión...</div>;
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  return <Outlet />;
}