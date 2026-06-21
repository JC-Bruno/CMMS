import { API_BASE_URL } from "@shared/api";
import { PageHeader, StatCard, StatusBadge } from "@shared/components"
import { PermissionGate } from "@modules/auth/components/PermissionGate";

const workOrders = [
  {
    number: "WO-20260620-0001",
    asset: "CNC Plasma 01",
    status: "En proceso",
    priority: "Alta",
  },
  {
    number: "WO-20260620-0002",
    asset: "Grúa puente 10T",
    status: "Asignada",
    priority: "Urgente",
  },
  {
    number: "WO-20260620-0003",
    asset: "Compresor principal",
    status: "Creada",
    priority: "Media",
  },
];

export function DashboardPage() {
  return (
    <section className="page">
      <PageHeader
      eyebrow="Reportes"
      title="Dashboard"
      description="Base visual para la creación de reportes"
      actions={
        <PermissionGate permission="maintenance_requests.create_request">
          <button className="button button--primary">Nueva solicitud</button>
        </PermissionGate>
      }
    />

      <div className="stats-grid">
        <StatCard label="Órdenes abiertas" value="18" helper="Pendientes de cierre" />
        <StatCard label="Solicitudes nuevas" value="7" helper="Reportadas hoy" />
        <StatCard label="Activos críticos" value="12" helper="Con criticidad alta" />
        <StatCard label="Repuestos bajo mínimo" value="5" helper="Requieren revisión" />
      </div>

      <div className="content-grid content-grid--single">
        <article className="panel panel--wide">
          <div className="panel__header">
            <div>
              <h3 className="panel__title">Órdenes recientes</h3>
              <p className="panel__description">
                Vista preliminar. Luego se alimentará desde `/api/work-orders/items/`.
              </p>
            </div>
          </div>

          <div className="table-shell">
            <table className="data-table">
              <thead>
                <tr>
                  <th>OT</th>
                  <th>Activo</th>
                  <th>Prioridad</th>
                  <th>Estado</th>
                </tr>
              </thead>
              <tbody>
                {workOrders.map((workOrder) => (
                  <tr key={workOrder.number}>
                    <td>{workOrder.number}</td>
                    <td>{workOrder.asset}</td>
                    <td>{workOrder.priority}</td>
                    <td>
                      <StatusBadge
                        label={workOrder.status}
                        variant={
                          workOrder.status === "En proceso"
                            ? "info"
                            : workOrder.status === "Asignada"
                              ? "warning"
                              : "neutral"
                        }
                      />
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </article>
      </div>
    </section>
  );
}