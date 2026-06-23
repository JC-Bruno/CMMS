import { useCallback } from "react";

import { PermissionGate } from "@modules/auth/components/PermissionGate";
import { listWorkOrders } from "@modules/work-orders/services/workOrdersApi";
import {
  EmptyState,
  ErrorState,
  LoadingState,
  PageHeader,
  StatusBadge,
} from "@shared/components";
import { useApiData } from "@shared/hooks/useApiData";
import { humanizeValue } from "@shared/utils/format";

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

export function WorkOrdersListPage() {
  const loadWorkOrders = useCallback(() => listWorkOrders(), []);
  const {
    data: workOrders,
    error,
    isLoading,
    reload,
  } = useApiData(loadWorkOrders);

  return (
    <section className="page">
      <PageHeader
        eyebrow="Órdenes de trabajo"
        title="Ejecución y seguimiento técnico"
        description="Órdenes de trabajo consultadas desde el backend."
        actions={
          <PermissionGate permission="work_orders.create_work_order">
            <button className="button button--primary">Nueva OT</button>
          </PermissionGate>
        }
      />

      {isLoading ? (
        <LoadingState message="Cargando órdenes de trabajo..." />
      ) : error ? (
        <ErrorState description={error} onRetry={reload} />
      ) : workOrders && workOrders.length > 0 ? (
        <article className="panel">
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
                {workOrders.map((workOrder) => (
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
        </article>
      ) : (
        <EmptyState
          title="Sin órdenes de trabajo"
          description="Cuando existan órdenes de trabajo, aparecerán en esta pantalla."
        />
      )}
    </section>
  );
}