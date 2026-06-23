import {
  apiRequest,
  getApiResponseItems,
  type ApiListResponse,
} from "@shared/api";

import type { AssetListItem, AssetStructureNodeListItem } from "../types";

export async function listAssets(): Promise<AssetListItem[]> {
  const response = await apiRequest<ApiListResponse<AssetListItem>>(
    "/assets/items/",
  );

  return getApiResponseItems(response);
}

export async function listAssetStructureNodes(): Promise<
  AssetStructureNodeListItem[]
> {
  const response = await apiRequest<ApiListResponse<AssetStructureNodeListItem>>(
    "/assets/structure-nodes/",
  );

  return getApiResponseItems(response);
}