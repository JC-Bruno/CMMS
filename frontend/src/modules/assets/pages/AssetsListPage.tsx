import { useCallback } from "react";

import { PermissionGate } from "@modules/auth/components/PermissionGate";
import { AssetStructureTree } from "@modules/assets/components/AssetStructureTree";
import {
  listAssets,
  listAssetStructureNodes,
} from "@modules/assets/services/assetsApi";
import {
  EmptyState,
  ErrorState,
  LoadingState,
  PageHeader,
  StatusBadge,
} from "@shared/components";
import { useApiData } from "@shared/hooks/useApiData";
import { humanizeValue } from "@shared/utils/format";

type AssetsPageData = {
  assets: Awaited<ReturnType<typeof listAssets>>;
  structureNodes: Awaited<ReturnType<typeof listAssetStructureNodes>>;
};

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
  const loadAssetsPageData = useCallback(async (): Promise<AssetsPageData> => {
    const [assets, structureNodes] = await Promise.all([
      listAssets(),
      listAssetStructureNodes(),
    ]);

    return {
      assets,
      structureNodes,
    };
  }, []);

  const { data, error, isLoading, reload } = useApiData(loadAssetsPageData);

  return (
    <section className="page">
      <PageHeader
        eyebrow="Activos"
        title="Equipos e infraestructura"
        description="Listado real de equipos y estructura técnica del activo."
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
      ) : data ? (
        <>
          {data.assets.length > 0 ? (
            <article className="panel">
              <div className="panel__header">
                <div>
                  <h3 className="panel__title">Activos registrados</h3>
                  <p className="panel__description">
                    Equipos e infraestructura disponibles para este cliente.
                  </p>
                </div>
              </div>

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
                    {data.assets.map((asset) => (
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

          <article className="panel">
            <div className="panel__header">
              <div>
                <h3 className="panel__title">Estructura técnica de activos</h3>
                <p className="panel__description">
                  Subsistemas, componentes y puntos mantenibles asociados a cada
                  activo.
                </p>
              </div>
            </div>

            {data.structureNodes.length > 0 ? (
              <AssetStructureTree nodes={data.structureNodes} />
            ) : (
              <EmptyState
                title="Sin estructura técnica"
                description="Cuando se registren subsistemas, componentes o puntos mantenibles, aparecerán aquí."
              />
            )}
          </article>
        </>
      ) : null}
    </section>
  );
}