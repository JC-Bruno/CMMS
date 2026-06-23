import { useCallback } from "react";

import { PermissionGate } from "@modules/auth/components/PermissionGate";
import { listAssets } from "@modules/assets/services/assetsApi";
import { listInventoryStock } from "@modules/inventory/services/inventoryApi";
import { listMaintenanceRequests } from "@modules/maintenance-requests/services/maintenanceRequestsApi";
import { listWorkOrders } from "@modules/work-orders/services/workOrdersApi";
import {
  EmptyState,
  ErrorState,
  LoadingState,
  PageHeader,
  StatCard,
  StatusBadge,
} from "@shared/components";
import { useApiData } from "@shared/hooks/useApiData";
import { humanizeValue } from "@shared/utils/format";

type DashboardData = {
  assetsCount: number;
  maintenanceRequestsCount: number;
  workOrdersCount: number;
  stockBelowMinimumCount: number;
  recentWorkOrders: Awaited<ReturnType<typeof listWorkOrders>>;
};

function getWorkOrderStatusVariant(status?: string) {
  if (status === "in_progress") {
    return "info";
  }

  if (status === "assigned" || status === "on_hold") {
    return "warning";
  }

  if (status === "cancelled") {
    return "danger";
  }

  if (status === "closed" || status === "technically_closed") {
    return "success";
  }

  return "neutral";
}

export function DashboardPage() {
  const loadDashboardData = useCallback(async (): Promise<DashboardData> => {
    const [assets, maintenanceRequests, workOrders, stockItems] =
      await Promise.all([
        listAssets(),
        listMaintenanceRequests(),
        listWorkOrders(),
        listInventoryStock(),
      ]);

    const stockBelowMinimumCount = stockItems.filter((item) => {
      const availableQuantity = Number(item.available_quantity ?? item.quantity_on_hand ?? 0);

      return !Number.isNaN(availableQuantity) && availableQuantity <= 0;
    }).length;

    return {
      assetsCount: assets.length,
      maintenanceRequestsCount: maintenanceRequests.length,
      workOrdersCount: workOrders.length,
      stockBelowMinimumCount,
      recentWorkOrders: workOrders.slice(0, 8),
    };
  }, []);

  const { data, error, isLoading, reload } = useApiData(loadDashboardData);

  return (
    <section className="page">
      <PageHeader
        eyebrow="Dashboard"
        title="Resumen general de mantenimiento"
        description="Vista inicial del estado operativo del CMMS alimentada desde la API real."
        actions={
          <PermissionGate permission="maintenance_requests.create_request">
            <button className="button button--primary">Nueva solicitud</button>
          </PermissionGate>
        }
      />

      {isLoading ? (
        <LoadingState message="Cargando resumen operativo..." />
      ) : error ? (
        <ErrorState description={error} onRetry={reload} />
      ) : data ? (
        <>
          <div className="stats-grid">
            <StatCard
              label="Órdenes abiertas"
              value={String(data.workOrdersCount)}
              helper="Registros encontrados"
            />
            <StatCard
              label="Solicitudes"
              value={String(data.maintenanceRequestsCount)}
              helper="Reportes registrados"
            />
            <StatCard
              label="Activos"
              value={String(data.assetsCount)}
              helper="Equipos e infraestructura"
            />
            <StatCard
              label="Stock en cero"
              value={String(data.stockBelowMinimumCount)}
              helper="Repuestos sin disponibilidad"
            />
          </div>

          <div className="content-grid content-grid--single">
            <article className="panel panel--wide">
              <div className="panel__header">
                <div>
                  <h3 className="panel__title">Órdenes recientes</h3>
                  <p className="panel__description">
                    Últimas órdenes de trabajo consultadas desde el backend.
                  </p>
                </div>
              </div>

              {data.recentWorkOrders.length > 0 ? (
                <div className="table-shell">
                  <table className="data-table">
                    <thead>
                      <tr>
                        <th>OT</th>
                        <th>Activo</th>
                        <th>Trabajo</th>
                        <th>Prioridad</th>
                        <th>Estado</th>
                      </tr>
                    </thead>
                    <tbody>
                      {data.recentWorkOrders.map((workOrder) => (
                        <tr key={workOrder.id}>
                          <td>{workOrder.work_order_number}</td>
                          <td>
                            {workOrder.asset_code ||
                              workOrder.asset_name ||
                              "Sin activo"}
                          </td>
                          <td>{workOrder.title}</td>
                          <td>{humanizeValue(workOrder.priority)}</td>
                          <td>
                            <StatusBadge
                              label={humanizeValue(workOrder.status)}
                              variant={getWorkOrderStatusVariant(workOrder.status)}
                            />
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              ) : (
                <EmptyState
                  title="Sin órdenes de trabajo"
                  description="Cuando existan órdenes de trabajo, aparecerán en esta sección."
                />
              )}
            </article>
          </div>
        </>
      ) : null}
    </section>
  );
}