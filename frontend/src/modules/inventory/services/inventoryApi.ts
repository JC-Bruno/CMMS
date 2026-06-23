import { apiRequest, getApiResponseItems, type ApiListResponse } from "@shared/api";

import type { InventoryStockListItem } from "../types";

export async function listInventoryStock() {
  const response = await apiRequest<ApiListResponse<InventoryStockListItem>>(
    "/inventory/stock/",
  );

  return getApiResponseItems(response);
}