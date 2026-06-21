import {
  createContext,
  useCallback,
  useEffect,
  useMemo,
  useState,
  type ReactNode,
} from "react";

import { configureHttpClientAuth } from "@shared/api";

import { fetchCurrentUserApi, loginApi, logoutApi } from "../services/authApi";
import {
  clearAuthSession,
  getStoredAccessToken,
  getStoredRefreshToken,
  getStoredTenantCode,
  getStoredTokens,
  saveAuthSession,
} from "../services/authStorage";
import type { CurrentUser, LoginPayload } from "../types";

type AuthContextValue = {
  user: CurrentUser | null;
  tenantCode: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (payload: LoginPayload) => Promise<void>;
  logout: () => Promise<void>;
  hasPermission: (permissionCode: string) => boolean;
};

export const AuthContext = createContext<AuthContextValue | null>(null);

type AuthProviderProps = {
  children: ReactNode;
};

configureHttpClientAuth({
  getAccessToken: getStoredAccessToken,
  getTenantCode: getStoredTenantCode,
});

export function AuthProvider({ children }: AuthProviderProps) {
  const [user, setUser] = useState<CurrentUser | null>(null);
  const [tenantCode, setTenantCode] = useState<string | null>(
    getStoredTenantCode(),
  );
  const [isLoading, setIsLoading] = useState(true);

  const restoreSession = useCallback(async () => {
    const tokens = getStoredTokens();
    const storedTenantCode = getStoredTenantCode();

    if (!tokens || !storedTenantCode) {
      clearAuthSession();
      setUser(null);
      setTenantCode(null);
      setIsLoading(false);
      return;
    }

    try {
      const currentUser = await fetchCurrentUserApi();
      setUser(currentUser);
      setTenantCode(storedTenantCode);
    } catch {
      clearAuthSession();
      setUser(null);
      setTenantCode(null);
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    void restoreSession();
  }, [restoreSession]);

  const login = useCallback(async (payload: LoginPayload) => {
    const tokens = await loginApi({
      username: payload.username,
      password: payload.password,
    });

    saveAuthSession(tokens, payload.tenantCode.trim());

    const currentUser = await fetchCurrentUserApi();

    setUser(currentUser);
    setTenantCode(payload.tenantCode.trim());
  }, []);

  const logout = useCallback(async () => {
    const refreshToken = getStoredRefreshToken();

    try {
      if (refreshToken) {
        await logoutApi(refreshToken);
      }
    } finally {
      clearAuthSession();
      setUser(null);
      setTenantCode(null);
    }
  }, []);

  const hasPermission = useCallback(
    (permissionCode: string) => {
      if (!user) {
        return false;
      }

      if (user.is_superuser) {
        return true;
      }

      return (
        user.permissions.includes("*") ||
        user.permissions.includes(permissionCode)
      );
    },
    [user],
  );

  const value = useMemo<AuthContextValue>(
    () => ({
      user,
      tenantCode,
      isAuthenticated: Boolean(user),
      isLoading,
      login,
      logout,
      hasPermission,
    }),
    [hasPermission, isLoading, login, logout, tenantCode, user],
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}