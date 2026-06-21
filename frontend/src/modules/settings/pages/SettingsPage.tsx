import { PageHeader } from "../../../shared/components/PageHeader";

const settingsBlocks = [
  {
    title: "Usuarios y permisos",
    description: "Administración de roles, permisos operativos y usuarios por cliente.",
  },
  {
    title: "Parámetros de mantenimiento",
    description: "Configuración de prioridades, estados, tipos de OT y reglas operativas.",
  },
  {
    title: "Datos del cliente",
    description: "Información de empresa, sedes, moneda y parámetros generales.",
  },
];

export function SettingsPage() {
  return (
    <section className="page">
      <PageHeader
        eyebrow="Configuración"
        title="Parámetros del sistema"
        description="Base visual para configuración general del CMMS."
      />

      <div className="cards-grid">
        {settingsBlocks.map((block) => (
          <article className="panel" key={block.title}>
            <h3 className="panel__title">{block.title}</h3>
            <p className="panel__description">{block.description}</p>
            <button className="button button--secondary">Configurar</button>
          </article>
        ))}
      </div>
    </section>
  );
}