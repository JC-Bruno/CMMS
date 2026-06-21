import { EmptyState, PageHeader, StatusBadge } from "@shared/components";

const assets = [
  {
    code: "PLASMA-01",
    name: "CNC Plasma 01",
    location: "Planta Opico / Área de corte",
    status: "Activo",
    criticality: "Alta",
  },
  {
    code: "GRUA-10T-01",
    name: "Grúa puente 10 toneladas",
    location: "Nave principal",
    status: "Activo",
    criticality: "Crítica",
  },
];

export function AssetsListPage() {
  return (
    <section className="page">
      <PageHeader
        eyebrow="Activos"
        title="Equipos e infraestructura"
        description="Listado base para equipos, infraestructura y ubicaciones técnicas."
        actions={<button className="button button--primary">Nuevo activo</button>}
      />

      {assets.length > 0 ? (
        <article className="panel">
          <div className="table-shell">
            <table className="data-table">
              <thead>
                <tr>
                  <th>Código</th>
                  <th>Nombre</th>
                  <th>Ubicación</th>
                  <th>Criticidad</th>
                  <th>Estado</th>
                </tr>
              </thead>
              <tbody>
                {assets.map((asset) => (
                  <tr key={asset.code}>
                    <td>{asset.code}</td>
                    <td>{asset.name}</td>
                    <td>{asset.location}</td>
                    <td>{asset.criticality}</td>
                    <td>
                      <StatusBadge label={asset.status} variant="success" />
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
          description="Cuando conectemos la API, aquí se mostrarán los activos del cliente."
        />
      )}
    </section>
  );
}