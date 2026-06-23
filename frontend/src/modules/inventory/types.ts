export type InventoryStockListItem = {
  id: string;
  spare_part_code?: string;
  spare_part_name?: string;
  location_code?: string;
  location_name?: string;
  quantity_on_hand?: string;
  reserved_quantity?: string;
  available_quantity?: string;
  average_unit_cost?: string;
};