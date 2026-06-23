export type AssetListItem = {
  id: string;
  code: string;
  name: string;
  asset_type?: string;
  status?: string;
  criticality?: string;
  location_code?: string;
  location_name?: string;
};