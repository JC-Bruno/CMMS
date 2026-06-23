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

export type AssetStructureNodeType =
  | "subsystem"
  | "component"
  | "maintainable_point";

export type AssetStructureNodeListItem = {
  id: string;
  asset: string;
  asset_code?: string;
  asset_name?: string;
  parent: string | null;
  parent_code?: string | null;
  parent_name?: string | null;
  node_type: AssetStructureNodeType;
  code: string;
  name: string;
  description?: string;
  is_maintainable: boolean;
  sort_order: number;
};