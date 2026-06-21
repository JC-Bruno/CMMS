export type AuthTokens = {
  access: string;
  refresh: string;
};

export type AuthTenant = {
  id: string;
  code: string;
  name: string;
  status: string;
  is_active: boolean;
};

export type CurrentUser = {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  is_superuser: boolean;
  tenant: AuthTenant | null;
  permissions: string[];
};

export type LoginPayload = {
  username: string;
  password: string;
  tenantCode: string;
};