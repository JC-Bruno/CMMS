import type { ReactNode } from "react";

import { useAuth } from "../hooks/useAuth";

type PermissionGateProps = {
  permission: string;
  fallback?: ReactNode;
  children: ReactNode;
};

export function PermissionGate({
  permission,
  fallback = null,
  children,
}: PermissionGateProps) {
  const { hasPermission } = useAuth();

  if (!hasPermission(permission)) {
    return <>{fallback}</>;
  }

  return <>{children}</>;
}