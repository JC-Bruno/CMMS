import { NavLink, Outlet } from "react-router-dom";

import { navigationItems } from "@app/navigation";
import { useAuth } from "@modules/auth/hooks/useAuth";

export function AppLayout() {
  const { user, tenantCode, logout, hasPermission } = useAuth();

  const visibleNavigationItems = navigationItems.filter((item) => {
    if (!item.requiredPermission) {
      return true;
    }

    return hasPermission(item.requiredPermission);
  });

  const displayName =
    [user?.first_name, user?.last_name].filter(Boolean).join(" ") ||
    user?.username ||
    "Usuario";

  const initials = displayName
    .split(" ")
    .map((part) => part[0])
    .join("")
    .slice(0, 2)
    .toUpperCase();

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
          {visibleNavigationItems.map((item) => (
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
          <p className="sidebar__footer-value">
            {user?.tenant?.name || tenantCode || "Sin cliente"}
          </p>
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
              <div className="topbar__avatar">{initials}</div>
              <div>
                <p className="topbar__user-name">{displayName}</p>
                <p className="topbar__user-role">
                  {user?.is_superuser ? "Administrador" : "Usuario CMMS"}
                </p>
              </div>
            </div>

            <button className="button button--secondary" onClick={logout}>
              Salir
            </button>
          </div>
        </header>

        <main className="content">
          <Outlet />
        </main>
      </div>
    </div>
  );
}