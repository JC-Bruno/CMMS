import {
  apiRequest,
  getApiResponseItems,
  type ApiListResponse,
} from "@shared/api";

import type { WorkOrderListItem } from "../types";

export async function listWorkOrders(): Promise<WorkOrderListItem[]> {
  const response = await apiRequest<ApiListResponse<WorkOrderListItem>>(
    "/work-orders/items/",
  );

  return getApiResponseItems(response);
}