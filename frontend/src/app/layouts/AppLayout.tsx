import { NavLink, Outlet } from "react-router-dom";

import { navigationItems } from "../navigation";

export function AppLayout() {
  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="sidebar__brand">
          <div className="sidebar__logo">CM</div>
          <div>
            <p className="sidebar__brand-name">CMMS Enterprise</p>
            <p className="sidebar__brand-subtitle">Mantenimiento industrial</p>
          </div>
        </div>

        <nav className="sidebar__nav" aria-label="Navegación principal">
          {navigationItems.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              end={item.end}
              className={({ isActive }) =>
                isActive
                  ? "sidebar__link sidebar__link--active"
                  : "sidebar__link"
              }
            >
              <span className="sidebar__link-icon">{item.icon}</span>
              <span>
                <span className="sidebar__link-label">{item.label}</span>
                <span className="sidebar__link-description">
                  {item.description}
                </span>
              </span>
            </NavLink>
          ))}
        </nav>

        <div className="sidebar__footer">
          <p className="sidebar__footer-label">Cliente activo</p>
          <p className="sidebar__footer-value">Plantilla cliente</p>
        </div>
      </aside>

      <div className="main-area">
        <header className="topbar">
          <div>
            <p className="topbar__eyebrow">Sistema CMMS</p>
            <h1 className="topbar__title">Panel operativo</h1>
          </div>

          <div className="topbar__actions">
            <input
              className="topbar__search"
              type="search"
              placeholder="Buscar activo, solicitud u OT..."
              aria-label="Buscar"
            />

            <div className="topbar__user">
              <div className="topbar__avatar">JB</div>
              <div>
                <p className="topbar__user-name">Julio Bruno</p>
                <p className="topbar__user-role">Mantenimiento</p>
              </div>
            </div>
          </div>
        </header>

        <main className="content">
          <Outlet />
        </main>
      </div>
    </div>
  );
}