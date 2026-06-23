export type MaintenanceRequestListItem = {
  id: string;
  request_number: string;
  asset_code?: string;
  asset_name?: string;
  title: string;
  description?: string;
  perceived_priority?: string;
  status?: string;
  requester_name?: string;
  created_at?: string;
};