import { PageHeader, StatusBadge } from "@shared/components";
import { PermissionGate } from "@modules/auth/components/PermissionGate";

const spareParts = [
  {
    code: "BRG-6205",
    name: "Rodamiento 6205",
    location: "Almacén principal",
    stock: "4.00",
    status: "Disponible",
  },
  {
    code: "FUSE-10A",
    name: "Fusible 10A",
    location: "Rack eléctrico",
    stock: "1.00",
    status: "Bajo mínimo",
  },
];

export function InventoryPage() {
  return (
    <section className="page">
      <PageHeader
        eyebrow="Inventario"
        title="Repuestos y existencias"
        description="Base visual para repuestos, almacenes, existencias y movimientos."
       actions={
        <PermissionGate permission="inventory.create_spare_part">
          <button className="button button--primary">Nuevo repuesto</button>
        </PermissionGate>
        }
      />

      <article className="panel">
        <div className="table-shell">
          <table className="data-table">
            <thead>
              <tr>
                <th>Código</th>
                <th>Repuesto</th>
                <th>Ubicación</th>
                <th>Existencia</th>
                <th>Estado</th>
              </tr>
            </thead>
            <tbody>
              {spareParts.map((part) => (
                <tr key={part.code}>
                  <td>{part.code}</td>
                  <td>{part.name}</td>
                  <td>{part.location}</td>
                  <td>{part.stock}</td>
                  <td>
                    <StatusBadge
                      label={part.status}
                      variant={part.status === "Bajo mínimo" ? "danger" : "success"}
                    />
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </article>
    </section>
  );
}