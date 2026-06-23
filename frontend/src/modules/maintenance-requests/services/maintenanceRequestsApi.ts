import {
  apiRequest,
  getApiResponseItems,
  type ApiListResponse,
} from "@shared/api";

import type { MaintenanceRequestListItem } from "../types";

export async function listMaintenanceRequests(): Promise<
  MaintenanceRequestListItem[]
> {
  const response =
    await apiRequest<ApiListResponse<MaintenanceRequestListItem>>(
      "/maintenance-requests/requests/",
    );

  return getApiResponseItems(response);
}