export type NavigationItem = {
  to: string;
  label: string;
  description: string;
  icon: string;
  end?: boolean;
  requiredPermission?: string;
};

export const navigationItems: NavigationItem[] = [
  {
    to: "/",
    label: "Dashboard",
    description: "Resumen operativo",
    icon: "⌂",
    end: true,
  },
  {
    to: "/assets",
    label: "Activos",
    description: "Equipos e infraestructura",
    icon: "▣",
    requiredPermission: "assets.view_asset",
  },
  {
    to: "/maintenance-requests",
    label: "Solicitudes",
    description: "Reportes de falla",
    icon: "!",
    requiredPermission: "maintenance_requests.view_request",
  },
  {
    to: "/work-orders",
    label: "Órdenes de trabajo",
    description: "Ejecución técnica",
    icon: "✓",
    requiredPermission: "work_orders.view_work_order",
  },
  {
    to: "/inventory",
    label: "Inventario",
    description: "Repuestos y almacenes",
    icon: "▤",
    requiredPermission: "inventory.view_spare_part",
  },
  {
    to: "/settings",
    label: "Configuración",
    description: "Parámetros del sistema",
    icon: "⚙",
    requiredPermission: "accounts.manage_user",
  },
];