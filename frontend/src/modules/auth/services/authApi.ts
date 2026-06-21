import { apiRequest } from "@shared/api";

import type { AuthTokens, CurrentUser } from "../types";

export async function loginApi(params: {
  username: string;
  password: string;
}) {
  return apiRequest<AuthTokens>("/auth/token/", {
    method: "POST",
    body: {
      username: params.username,
      password: params.password,
    },
  });
}

export async function fetchCurrentUserApi() {
  return apiRequest<CurrentUser>("/auth/me/");
}

export async function logoutApi(refreshToken: string) {
  return apiRequest<void>("/auth/logout/", {
    method: "POST",
    body: {
      refresh: refreshToken,
    },
  });
}