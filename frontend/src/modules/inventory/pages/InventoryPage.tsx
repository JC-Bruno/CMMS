import { useCallback } from "react";

import { PermissionGate } from "@modules/auth/components/PermissionGate";
import { listInventoryStock } from "@modules/inventory/services/inventoryApi";
import {
  EmptyState,
  ErrorState,
  LoadingState,
  PageHeader,
  StatusBadge,
} from "@shared/components";
import { useApiData } from "@shared/hooks/useApiData";
import { formatQuantity } from "@shared/utils/format";

function getStockStatus(quantity?: string) {
  const quantityValue = Number(quantity ?? 0);

  if (Number.isNaN(quantityValue) || quantityValue <= 0) {
    return {
      label: "Sin stock",
      variant: "danger" as const,
    };
  }

  return {
    label: "Disponible",
    variant: "success" as const,
  };
}

export function InventoryPage() {
  const loadStock = useCallback(() => listInventoryStock(), []);
  const { data: stockItems, error, isLoading, reload } = useApiData(loadStock);

  return (
    <section className="page">
      <PageHeader
        eyebrow="Inventario"
        title="Repuestos y existencias"
        description="Existencias reales de repuestos por ubicación."
        actions={
          <PermissionGate permission="inventory.create_spare_part">
            <button className="button button--primary">Nuevo repuesto</button>
          </PermissionGate>
        }
      />

      {isLoading ? (
        <LoadingState message="Cargando inventario..." />
      ) : error ? (
        <ErrorState description={error} onRetry={reload} />
      ) : stockItems && stockItems.length > 0 ? (
        <article className="panel">
          <div className="table-shell">
            <table className="data-table">
              <thead>
                <tr>
                  <th>Código</th>
                  <th>Repuesto</th>
                  <th>Ubicación</th>
                  <th>Existencia</th>
                  <th>Disponible</th>
                  <th>Estado</th>
                </tr>
              </thead>
              <tbody>
                {stockItems.map((stockItem) => {
                  const stockStatus = getStockStatus(
                    stockItem.available_quantity ?? stockItem.quantity_on_hand,
                  );

                  return (
                    <tr key={stockItem.id}>
                      <td>{stockItem.spare_part_code || "Sin código"}</td>
                      <td>{stockItem.spare_part_name || "Sin nombre"}</td>
                      <td>
                        {stockItem.location_code ||
                          stockItem.location_name ||
                          "Sin ubicación"}
                      </td>
                      <td>{formatQuantity(stockItem.quantity_on_hand)}</td>
                      <td>
                        {formatQuantity(
                          stockItem.available_quantity ??
                            stockItem.quantity_on_hand,
                        )}
                      </td>
                      <td>
                        <StatusBadge
                          label={stockStatus.label}
                          variant={stockStatus.variant}
                        />
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </article>
      ) : (
        <EmptyState
          title="Sin existencias registradas"
          description="Cuando se registren repuestos y stock, aparecerán en esta pantalla."
        />
      )}
    </section>
  );
}