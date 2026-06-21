import type { AuthTokens } from "../types";

const TOKENS_KEY = "cmms.auth.tokens";
const TENANT_CODE_KEY = "cmms.auth.tenantCode";

export function saveAuthSession(tokens: AuthTokens, tenantCode: string) {
  localStorage.setItem(TOKENS_KEY, JSON.stringify(tokens));
  localStorage.setItem(TENANT_CODE_KEY, tenantCode);
}

export function getStoredTokens(): AuthTokens | null {
  const rawTokens = localStorage.getItem(TOKENS_KEY);

  if (!rawTokens) {
    return null;
  }

  try {
    return JSON.parse(rawTokens) as AuthTokens;
  } catch {
    clearAuthSession();
    return null;
  }
}

export function getStoredAccessToken() {
  return getStoredTokens()?.access || null;
}

export function getStoredRefreshToken() {
  return getStoredTokens()?.refresh || null;
}

export function getStoredTenantCode() {
  return localStorage.getItem(TENANT_CODE_KEY);
}

export function clearAuthSession() {
  localStorage.removeItem(TOKENS_KEY);
  localStorage.removeItem(TENANT_CODE_KEY);
}