import {
  apiRequest,
  getApiResponseItems,
  type ApiListResponse,
} from "@shared/api";

import type { AssetListItem } from "../types";

export async function listAssets(): Promise<AssetListItem[]> {
  const response = await apiRequest<ApiListResponse<AssetListItem>>(
    "/assets/items/",
  );

  return getApiResponseItems(response);
}