export type WorkOrderListItem = {
  id: string;
  work_order_number: string;
  asset_code?: string;
  asset_name?: string;
  title: string;
  description?: string;
  type?: string;
  priority?: string;
  status?: string;
  created_at?: string;
};