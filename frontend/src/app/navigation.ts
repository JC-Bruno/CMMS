export type NavigationItem = {
  to: string;
  label: string;
  description: string;
  icon: string;
  end?: boolean;
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
  },
  {
    to: "/maintenance-requests",
    label: "Solicitudes",
    description: "Reportes de falla",
    icon: "!",
  },
  {
    to: "/work-orders",
    label: "Órdenes de trabajo",
    description: "Ejecución técnica",
    icon: "✓",
  },
  {
    to: "/inventory",
    label: "Inventario",
    description: "Repuestos y almacenes",
    icon: "▤",
  },
  {
    to: "/settings",
    label: "Configuración",
    description: "Parámetros del sistema",
    icon: "⚙",
  },
];