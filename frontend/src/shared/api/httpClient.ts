const DEFAULT_API_BASE_URL = "http://127.0.0.1:8000/api";

export const API_BASE_URL = (
  import.meta.env.VITE_API_BASE_URL || DEFAULT_API_BASE_URL
).replace(/\/$/, "");

export type ApiRequestOptions = {
  method?: "GET" | "POST" | "PUT" | "PATCH" | "DELETE";
  body?: unknown;
  headers?: Record<string, string>;
};

type HttpClientAuthGetters = {
  getAccessToken: () => string | null;
  getTenantCode: () => string | null;
};

let authGetters: HttpClientAuthGetters = {
  getAccessToken: () => null,
  getTenantCode: () => null,
};

export function configureHttpClientAuth(getters: HttpClientAuthGetters) {
  authGetters = getters;
}

export async function apiRequest<T>(
  path: string,
  options: ApiRequestOptions = {},
): Promise<T> {
  const headers = new Headers(options.headers);

  if (!(options.body instanceof FormData)) {
    headers.set("Content-Type", "application/json");
  }

  const accessToken = authGetters.getAccessToken();
  const tenantCode = authGetters.getTenantCode();

  if (accessToken) {
    headers.set("Authorization", `Bearer ${accessToken}`);
  }

  if (tenantCode) {
    headers.set("X-CMMS-Tenant-Code", tenantCode);
  }

  const response = await fetch(`${API_BASE_URL}${path}`, {
    method: options.method || "GET",
    headers,
    body:
      options.body instanceof FormData
        ? options.body
        : options.body
          ? JSON.stringify(options.body)
          : undefined,
  });

  if (!response.ok) {
    const errorText = await response.text();

    throw new Error(
      `API request failed with status ${response.status}: ${errorText}`,
    );
  }

  if (response.status === 204) {
    return undefined as T;
  }

  const contentType = response.headers.get("content-type") || "";

  if (!contentType.includes("application/json")) {
    return undefined as T;
  }

  return response.json() as Promise<T>;
}