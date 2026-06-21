import { PageHeader, StatusBadge } from "@shared/components";
import { PermissionGate } from "@modules/auth/components/PermissionGate";

const workOrders = [
  {
    number: "WO-20260620-0001",
    asset: "CNC Plasma 01",
    title: "Revisión de eje por ruido anormal",
    technician: "Técnico asignado",
    status: "En proceso",
  },
  {
    number: "WO-20260620-0002",
    asset: "Grúa puente 10T",
    title: "Inspección de polipasto",
    technician: "Pendiente",
    status: "Asignada",
  },
];

export function WorkOrdersListPage() {
  return (
    <section className="page">
      <PageHeader
        eyebrow="Órdenes de trabajo"
        title="Ejecución y seguimiento técnico"
        description="Base visual para creación, asignación, inicio, cierre técnico y cierre final de OT."
        actions={
          <PermissionGate permission="work_orders.create_work_order">
            <button className="button button--primary">Nueva OT</button>
          </PermissionGate>
        }
      />

      <article className="panel">
        <div className="table-shell">
          <table className="data-table">
            <thead>
              <tr>
                <th>OT</th>
                <th>Activo</th>
                <th>Trabajo</th>
                <th>Técnico</th>
                <th>Estado</th>
              </tr>
            </thead>
            <tbody>
              {workOrders.map((workOrder) => (
                <tr key={workOrder.number}>
                  <td>{workOrder.number}</td>
                  <td>{workOrder.asset}</td>
                  <td>{workOrder.title}</td>
                  <td>{workOrder.technician}</td>
                  <td>
                    <StatusBadge
                      label={workOrder.status}
                      variant={
                        workOrder.status === "En proceso" ? "info" : "warning"
                      }
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