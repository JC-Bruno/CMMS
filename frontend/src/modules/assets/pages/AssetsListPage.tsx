import { useCallback } from "react";

import { PermissionGate } from "@modules/auth/components/PermissionGate";
import { listAssets } from "@modules/assets/services/assetsApi";
import {
  EmptyState,
  ErrorState,
  LoadingState,
  PageHeader,
  StatusBadge,
} from "@shared/components";
import { useApiData } from "@shared/hooks/useApiData";
import { humanizeValue } from "@shared/utils/format";

function getAssetStatusVariant(status?: string) {
  if (status === "active") {
    return "success";
  }

  if (status === "in_maintenance") {
    return "warning";
  }

  if (status === "out_of_service" || status === "retired") {
    return "danger";
  }

  return "neutral";
}

export function AssetsListPage() {
  const loadAssets = useCallback(() => listAssets(), []);
  const { data: assets, error, isLoading, reload } = useApiData(loadAssets);

  return (
    <section className="page">
      <PageHeader
        eyebrow="Activos"
        title="Equipos e infraestructura"
        description="Listado real de equipos, infraestructura y ubicaciones técnicas desde la API."
        actions={
          <PermissionGate permission="assets.create_asset">
            <button className="button button--primary">Nuevo activo</button>
          </PermissionGate>
        }
      />

      {isLoading ? (
        <LoadingState message="Cargando activos..." />
      ) : error ? (
        <ErrorState description={error} onRetry={reload} />
      ) : assets && assets.length > 0 ? (
        <article className="panel">
          <div className="table-shell">
            <table className="data-table">
              <thead>
                <tr>
                  <th>Código</th>
                  <th>Nombre</th>
                  <th>Tipo</th>
                  <th>Ubicación</th>
                  <th>Criticidad</th>
                  <th>Estado</th>
                </tr>
              </thead>
              <tbody>
                {assets.map((asset) => (
                  <tr key={asset.id}>
                    <td>{asset.code}</td>
                    <td>{asset.name}</td>
                    <td>{humanizeValue(asset.asset_type)}</td>
                    <td>
                      {asset.location_code ||
                        asset.location_name ||
                        "Sin ubicación"}
                    </td>
                    <td>{humanizeValue(asset.criticality)}</td>
                    <td>
                      <StatusBadge
                        label={humanizeValue(asset.status)}
                        variant={getAssetStatusVariant(asset.status)}
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
          title="Sin activos registrados"
          description="Todavía no hay activos disponibles para este cliente."
        />
      )}
    </section>
  );
}