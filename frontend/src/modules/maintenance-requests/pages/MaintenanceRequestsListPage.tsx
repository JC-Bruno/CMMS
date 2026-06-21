import { PageHeader, StatusBadge } from "@shared/components";

const requests = [
  {
    number: "MR-20260620-0001",
    asset: "CNC Plasma 01",
    title: "Ruido anormal en eje",
    priority: "Alta",
    status: "Creada",
  },
  {
    number: "MR-20260620-0002",
    asset: "Compresor principal",
    title: "Baja presión de aire",
    priority: "Urgente",
    status: "Recibida",
  },
];

export function MaintenanceRequestsListPage() {
  return (
    <section className="page">
      <PageHeader
        eyebrow="Solicitudes"
        title="Reportes de falla"
        description="Vista para solicitudes creadas por supervisores o usuarios con permiso de reportar."
        actions={<button className="button button--primary">Nueva solicitud</button>}
      />

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
                <tr key={request.number}>
                  <td>{request.number}</td>
                  <td>{request.asset}</td>
                  <td>{request.title}</td>
                  <td>{request.priority}</td>
                  <td>
                    <StatusBadge
                      label={request.status}
                      variant={request.status === "Recibida" ? "info" : "neutral"}
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