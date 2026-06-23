import { useCallback } from "react";

import { PermissionGate } from "@modules/auth/components/PermissionGate";
import { listMaintenanceRequests } from "@modules/maintenance-requests/services/maintenanceRequestsApi";
import {
  EmptyState,
  ErrorState,
  LoadingState,
  PageHeader,
  StatusBadge,
} from "@shared/components";
import { useApiData } from "@shared/hooks/useApiData";
import { humanizeValue } from "@shared/utils/format";

function getRequestStatusVariant(status?: string) {
  if (status === "created") {
    return "neutral";
  }

  if (status === "received" || status === "converted_to_work_order") {
    return "info";
  }

  if (status === "rejected" || status === "cancelled") {
    return "danger";
  }

  return "neutral";
}

export function MaintenanceRequestsListPage() {
  const loadRequests = useCallback(() => listMaintenanceRequests(), []);
  const {
    data: requests,
    error,
    isLoading,
    reload,
  } = useApiData(loadRequests);

  return (
    <section className="page">
      <PageHeader
        eyebrow="Solicitudes"
        title="Reportes de falla"
        description="Solicitudes reales creadas por usuarios con permiso de reportar."
        actions={
          <PermissionGate permission="maintenance_requests.create_request">
            <button className="button button--primary">Nueva solicitud</button>
          </PermissionGate>
        }
      />

      {isLoading ? (
        <LoadingState message="Cargando solicitudes..." />
      ) : error ? (
        <ErrorState description={error} onRetry={reload} />
      ) : requests && requests.length > 0 ? (
        <article className="panel">
          <div className="table-shell">
            <table className="data-table">
              <thead>
                <tr>
                  <th>Solicitud</th>
                  <th>Activo</th>
                  <th>Descripción</th>
                  <th>Prioridad</th>
                  <th>Estado</th>
                </tr>
              </thead>
              <tbody>
                {requests.map((request) => (
                  <tr key={request.id}>
                    <td>{request.request_number}</td>
                    <td>
                      {request.asset_code || request.asset_name || "Sin activo"}
                    </td>
                    <td>{request.title}</td>
                    <td>{humanizeValue(request.perceived_priority)}</td>
                    <td>
                      <StatusBadge
                        label={humanizeValue(request.status)}
                        variant={getRequestStatusVariant(request.status)}
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
          title="Sin solicitudes registradas"
          description="Cuando se reporten fallas, aparecerán en esta pantalla."
        />
      )}
    </section>
  );
}